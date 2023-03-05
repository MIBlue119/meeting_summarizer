"""Defines the summarizer class."""
from pathlib import Path
from tqdm import tqdm
from meeting_summarizer.utils import breakup_text_into_chunks,get_model_selection,generate_openai_completion,parse_text_response, count_tokens

class Summarizer:
    def __init__(self, config, prompter_class, loader,streamlit_progress_bar=None, streamlit_progress_message=None):
        """Initializes the summarizer class."""
        self.config = config
        self.text_engine = self.config.TEXT_ENGINE
        self.prompter = prompter_class(language=self.config.LANGUAGE)
        self.loader = loader
        self.loaded_text = None
        self.chunks = None
        self.chunk_responses = []
        self.meeting_summary = None
        self.streamlit_progress_bar = streamlit_progress_bar
        self.streamlit_progress_message = streamlit_progress_message
    
    def load_data(self, file_path):
        """Loads data from file."""
        self.loaded_text = self.loader.load_data(file_path)

    def breakup_text_into_chunks(self, max_tokens, overlap_size):
        """Breaks up the text into chunks of size max_tokens with overlap of overlap_size."""
        self.chunks = breakup_text_into_chunks(self.loaded_text, max_tokens, overlap_size)
    def summarize_chunks(self):
        """Summarizes the text."""
        progress_bar_max = self.config.TEST_NUM if self.config.IS_TEST else len(self.chunks)
        progress_bar = tqdm(total=progress_bar_max)

        index = 0
        if self.streamlit_progress_message is not None:
            self.streamlit_progress_message.markdown("Summarizing per chunks...") 
        for i, chunk in enumerate(self.chunks):
            progress_bar.update(index)
            chunk_prompt = self.prompter.get_chunk_prompt(chunk, text_engine=self.text_engine)
            api_settings ={
                **get_model_selection(self.text_engine),
                **chunk_prompt,
                "n": 1, 
                "max_tokens" :100,               
                "temperature": self.config.TEXT_ENGINE_TEMPERATURE,
                "presence_penalty" : 2

            }
            response = generate_openai_completion(text_engine=self.text_engine, api_settings=api_settings)
            chunk_text =  parse_text_response(response, text_engine=self.text_engine)
            if chunk_text =="" or chunk_text == "\n":
                continue
            print([chunk_text])
            index += 1
            if self.streamlit_progress_bar is not None:
                if index/progress_bar_max > 1:
                    self.streamlit_progress_bar.progress(1)
                else:
                    self.streamlit_progress_bar.progress(index/progress_bar_max)
            self.chunk_responses.append(chunk_text)
            if self.config.IS_TEST and i == self.config.TEST_NUM:
                break
        
        num_tokens = count_tokens(' '.join(self.chunk_responses))
        if (num_tokens+self.config.FINAL_SUMMARY_TOKENS) > 3800:
            # If the total number of tokens is greater than 3800, then we need to reduce the number of tokens in the final summary.
            # We would like to summarize again with a smaller number of tokens.
            # Replace the loaded text with the chunk responses and then summarize again
            self.loaded_text = ' '.join(self.chunk_responses)
            # Clean the chunk responses
            self.chunk_responses = []
            self.breakup_text_into_chunks(max_tokens=1000, overlap_size=200)
            self.summarize_chunks()
        else:
            return
    def summarize_all(self):
        """Summarizes all chunks responses to get final summary and keytakeaways."""
        if self.streamlit_progress_message is not None:
            self.streamlit_progress_message.markdown("Summarizes all chunks responses to get final summary and keytakeaways.")
        consolidated_prompt = self.prompter.get_consolidated_prompt(self.chunk_responses, text_engine=self.text_engine)
        if self.streamlit_progress_bar is not None:
            self.streamlit_progress_bar.progress(0)
        api_settings = {
            **get_model_selection(self.text_engine),
            **consolidated_prompt,
            "n": 1,
            "max_tokens" : self.config.FINAL_SUMMARY_TOKENS,
            "temperature": self.config.TEXT_ENGINE_TEMPERATURE,
            "presence_penalty" : 0
        }
        response =  generate_openai_completion(text_engine=self.text_engine, api_settings=api_settings)
        self.meeting_summary = parse_text_response(response, text_engine=self.text_engine)
        if self.streamlit_progress_bar is not None:
            self.streamlit_progress_bar.progress(100)        
        return self.meeting_summary

    def write_summary_to_file(self,file_path):
        """Writes the summary to a file."""
        if self.streamlit_progress_message is not None:
            self.streamlit_progress_message.markdown("Writing summary to file...")
        if self.streamlit_progress_bar is not None:
            self.streamlit_progress_bar.progress(0)            
        with open(file_path, "w") as f:
            f.write(self.meeting_summary)
        if self.streamlit_progress_bar is not None:
            self.streamlit_progress_bar.progress(100) 
        if self.streamlit_progress_message is not None:
            self.streamlit_progress_message.markdown("Finished writing summary to file.")                       
    def make_summary(self, file_path, export_dir: str = None):
        """Makes the summary."""     
        # Extract file name
        file_name = Path(file_path).stem
        # Load data from file    
        self.load_data(file_path)
        # Break up the text into chunks
        self.breakup_text_into_chunks(max_tokens=self.config.MAX_TOKENS, overlap_size=self.config.OVERLAP_SIZE)
        # Summarize the chunks
        self.summarize_chunks()
        # Summarize all chunks responses to get final summary and keytakeaways
        meeting_summary = self.summarize_all()
        # Write the summary to a file
        if export_dir is None:
            export_dir = Path(file_path).parent
        else:
            export_dir = Path(export_dir)
        export_file_path = Path(export_dir) / f"{file_name}.summary.txt"
        self.write_summary_to_file(export_file_path)
        print("\n Results:\n"+meeting_summary)