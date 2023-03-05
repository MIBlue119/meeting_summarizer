import os
import argparse
from pathlib import Path

import openai
from tqdm import tqdm

from meeting_summarizer.fileloader import WebVttLoader, SrtLoader
from meeting_summarizer.prompter import SummarizerPrompter
from meeting_summarizer.config import AppConfig
from meeting_summarizer.summarizer import Summarizer
from meeting_summarizer.utils import LANGUAGES, TO_LANGUAGE_CODE

def main(args):
    # Set the OpenAI API key
    openai.api_key = os.getenv("OPENAI_API_KEY")         
    file_path = args.file_path
    # Check the file is .vtt or .srt file
    file_extension = Path(file_path).suffix
    if file_extension not in [".vtt", ".srt"]:
        raise ValueError("File must be a .vtt /.srt file")
    # Initialize the loader class
    if file_extension == ".vtt":
        data_loader = WebVttLoader()
    elif file_extension == ".srt":
        data_loader = SrtLoader()
    # Initialize the config class
    config = AppConfig()
    config.set_text_engine(args.text_engine)
    config.LANGUAGE = args.language
    if args.test:
        config.IS_TEST = True
        config.TEST_NUM = args.test_num
    else:
        config.IS_TEST = False
    # Initialize the Summarizer class
    summarizer = Summarizer(config,SummarizerPrompter, data_loader)
    summarizer.make_summary(file_path)        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_path", dest="file_path", type=str, help="Path to the file to be summarized.")
    parser.add_argument(
        "--text_engine", 
        dest="text_engine",
        type=str,default="gpt-3.5-turbo",
        choices=["gpt-3.5-turbo","text-davinci-003"],
        help="Text engine to be used for summarization.")
    parser.add_argument(
        "--language",
        type=str,
        choices=sorted(LANGUAGES.keys())
        + sorted([k.title() for k in TO_LANGUAGE_CODE.keys()]),
        default="zh-hant",
        help="language to translate to",
    )    
    parser.add_argument(
        "--test",
        dest="test",
        action="store_true",
        help="If test we only summarize 4 contents you can easily check",
    )
    parser.add_argument(
        "--test_num",
        dest="test_num",
        type=int,
        default=4,
        help="test num for the test",
    )        
    args = parser.parse_args()
    main(args)