import openai
from meeting_summarizer.fileloader.webvtt_loader import WebVttLoader
from meeting_summarizer.prompter import SummarizerPrompter
from meeting_summarizer.utils import (
    text2token,   
    token2text,
    count_tokens,
    breakup_text_into_chunks
)

# Load data from file
file_path = "/Users/weirenlan/Desktop/self_practice/meeting_summarizer/examples/EP108_humanosis_Podcast.vtt"

# Initialize the WebVTTLoader class
webvtt_loader = WebVttLoader()

# Initialize the SummarizerPrompter class
summarizer_prompter = SummarizerPrompter(language="zh-tw")

# Load data from file
text = webvtt_loader.load_data(file_path)

max_tokens = 2000
overlap_size = 100
text_engine = "text-davinci-003"

# Set the OpenAI API key
import os 
openai.api_key = os.getenv("OPENAI_API_KEY")

# Iterate through the chunks of text to summarize
chunk_responses = []
chunks = breakup_text_into_chunks(text, max_tokens, overlap_size)
for i, chunk in enumerate(chunks):
    chunk_prompt = summarizer_prompter.get_chunk_prompt(chunk)
    response =  openai.Completion.create(
        model = text_engine,
        prompt = chunk_prompt,
        temperature = 0.5,
        max_tokens = 500,
        top_p = 1,
        frequency_penalty = 0,
        presence_penalty = 0,
    )
    chunk_text = response["choices"][0]["text"].strip()
    print(chunk_text)
    chunk_responses.append(chunk_text)

# Consolidate the response by calling the api again
consolidated_prompt = summarizer_prompter.get_consolidated_prompt(chunk_responses)
response =  openai.Completion.create(
    model = text_engine,
    prompt = consolidated_prompt,
    temperature = 0.5,
    max_tokens = 1000,
    top_p = 1,
    frequency_penalty = 0,
    presence_penalty = 0,
)

meeting_summary = response["choices"][0]["text"].strip()
print(meeting_summary)

