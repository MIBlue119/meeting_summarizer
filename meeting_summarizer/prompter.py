"""Defines the prompter class for the summarizer."""
class SummarizerPrompter:
    def __init__(self, language):
        self.language = language

    def get_chunk_prompt(self, chunk, text_engine="text-davinci-003"):
        chunk_prompt = f"#Input\n{chunk}\n#lang:{self.language}#Instuctions:TL;DR:"
        if "text" in text_engine:
            return {
                "prompt": chunk_prompt,
            }
        elif "gpt-3.5" in text_engine:
            return {
                "messages":[
                {"role": "system", "content": chunk_prompt}
                ]
            }
        return chunk_prompt
    def get_consolidated_prompt(self, chunk_responses, text_engine="text-davinci-003"):
        consolidated_prompt = f"#lang:{self.language}#Instructions\n Consoloidate these summaries under 150 words.And list 5key takeaways with list.#Input\n|{chunk_responses}|\n#lang:{self.language}\n"
        if "text"in text_engine:
            return {
                "prompt": consolidated_prompt,
            }
        elif "gpt-3.5" in text_engine:
            return {
                "messages":[
                {"role": "system", "content": consolidated_prompt}
                ]
            }
        return consolidated_prompt
