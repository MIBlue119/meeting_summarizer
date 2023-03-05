"""Defines the prompter class for the summarizer."""

class SummarizerPrompter:
    def __init__(self, language):
        if language not in ["en", "zh-tw"]:
            print("Currently only supports en and zh-TW.")
            raise ValueError(f"Invalid language: {language}")
        self.language = language

    def get_chunk_prompt(self, chunk, text_engine="text-davinci-003"):
        if self.language == "en":
            chunk_prompt = f"{chunk}\nTL;DR en:"
        elif self.language == "zh-tw":
            chunk_prompt = f"{chunk}\nTL;DR zhtw:"

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
        if self.language == "en":
            consolidated_prompt = f"#lang:en#Instructions\n Consoloidate these summaries under 150 words.And list 5key takeaways.\n#Input\n{chunk_responses}"
        elif self.language == "zh-tw":
            consolidated_prompt = f"#lang:zh-tw#Instructions\n Consoloidate these summaries under 150 words.And list 5key takeaways.\n#Input\n{chunk_responses}"
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
