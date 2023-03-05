"""Defines the summarizer class."""
from pathlib import Path
from tqdm import tqdm
from meeting_summarizer.utils import breakup_text_into_chunks,get_model_selection,generate_openai_completion,parse_text_response

class Summarizer:
    def __init__(self, config, prompter_class, loader):
        """Initializes the summarizer class."""
        self.config = config
        self.text_engine = self.config.TEXT_ENGINE
        self.prompter = prompter_class(language=self.config.LANGUAGE)
        self.loader = loader
        self.loaded_text = None
        self.chunks = None
        self.chunk_responses = []
        self.meeting_summary = None
    
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
            self.chunk_responses.append(chunk_text)
            if self.config.IS_TEST and i == self.config.TEST_NUM:
                break
    def summarize_all(self):
        """Summarizes all chunks responses to get final summary anf keytakeaways."""
        consolidated_prompt = self.prompter.get_consolidated_prompt(self.chunk_responses, text_engine=self.text_engine)
        api_settings = {
            **get_model_selection(self.text_engine),
            **consolidated_prompt,
            "n": 1,
            "max_tokens" : 2000,
            "temperature": self.config.TEXT_ENGINE_TEMPERATURE,
            "presence_penalty" : 0
        }
        response =  generate_openai_completion(text_engine=self.text_engine, api_settings=api_settings)
        self.meeting_summary = parse_text_response(response, text_engine=self.text_engine)
        return self.meeting_summary

    def write_summary_to_file(self,file_path):
        """Writes the summary to a file."""
        with open(file_path, "w") as f:
            f.write(self.meeting_summary)
    def make_summary(self, file_path):
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
        self.write_summary_to_file(f"{file_name}.summary.txt")
        print(meeting_summary)