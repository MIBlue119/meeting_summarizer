import os 
import openai
from meeting_summarizer.fileloader.webvtt_loader import WebVttLoader
from meeting_summarizer.prompter import SummarizerPrompter
from meeting_summarizer.config import AppConfig
from meeting_summarizer.summarizer import Summarizer


# Set the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
# Initialize the WebVTTLoader class
webvtt_loader = WebVttLoader()
# Initialize the Summarizer class
summarizer = Summarizer(SummarizerPrompter, webvtt_loader)
# Load data from file
file_path = "/Users/weirenlan/Desktop/self_practice/meeting_summarizer/examples/EP108_humanosis_Podcast.vtt"
summarizer.load_data(file_path)
# Break up the text into chunks
summarizer.breakup_text_into_chunks(max_tokens=AppConfig.MAX_TOKENS, overlap_size=AppConfig.OVERLAP_SIZE)
# Summarize the chunks
summarizer.summarize_chunks()
# Summarize all chunks responses to get final summary and keytakeaways
meeting_summary = summarizer.summarize_all()
print(meeting_summary)