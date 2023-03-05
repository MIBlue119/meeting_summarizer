import os 
import openai
from meeting_summarizer.fileloader.webvtt_loader import WebVttLoader
from meeting_summarizer.prompter import SummarizerPrompter
from meeting_summarizer.utils import (
    text2token,   
    token2text,
    count_tokens,
    breakup_text_into_chunks,
    parse_text_response,
    get_model_selection,
    get_engine_method,
    generate_openai_completion
)
from meeting_summarizer.config import (TEXT_ENGINE, 
                                       TEXT_ENGINE_TEMPERATURE, 
                                       LANGUAGE, 
                                       IS_TEST, 
                                       TEST_NUM,
                                       MAX_TOKENS,
                                       OVERLAP_SIZE)
# Set the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
# Load data from file
file_path = "/Users/weirenlan/Desktop/self_practice/meeting_summarizer/examples/EP108_humanosis_Podcast.vtt"

# Initialize the WebVTTLoader class
webvtt_loader = WebVttLoader()

# Initialize the SummarizerPrompter class
summarizer_prompter = SummarizerPrompter(language=LANGUAGE)

# Load data from file
text = webvtt_loader.load_data(file_path)

# Iterate through the chunks of text to summarize
chunk_responses = []
chunks = breakup_text_into_chunks(text, MAX_TOKENS, OVERLAP_SIZE)
for i, chunk in enumerate(chunks):
    chunk_prompt = summarizer_prompter.get_chunk_prompt(chunk, text_engine=TEXT_ENGINE)
    api_settings ={
        **get_model_selection(TEXT_ENGINE),
        **chunk_prompt,
        "n": 1, 
        "max_tokens" :100,               
        "temperature": TEXT_ENGINE_TEMPERATURE,
        "presence_penalty" : 2


    }
    response = generate_openai_completion(text_engine=TEXT_ENGINE, api_settings=api_settings)
    chunk_text =  parse_text_response(response, text_engine=TEXT_ENGINE)
    if chunk_text =="" or chunk_text == "\n":
        continue
    print([chunk_text])
    chunk_responses.append(chunk_text)
    if IS_TEST and i == TEST_NUM:
        break

# Consolidate the response by calling the api again
consolidated_prompt = summarizer_prompter.get_consolidated_prompt(chunk_responses, text_engine=TEXT_ENGINE)
api_settings = {
    **get_model_selection(TEXT_ENGINE),
    **consolidated_prompt,
    "n": 1,
    "max_tokens" : 2000,
    "temperature": TEXT_ENGINE_TEMPERATURE,
    "presence_penalty" : 0

}
response =  generate_openai_completion(text_engine=TEXT_ENGINE, api_settings=api_settings)
meeting_summary = parse_text_response(response, text_engine=TEXT_ENGINE)
print("\n\n"+meeting_summary)

