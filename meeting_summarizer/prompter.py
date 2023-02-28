class SummarizerPrompter:
    def __init__(self, language):
        if language not in ["en", "zh-tw"]:
            print("Currently only supports en and zh-TW.")
            raise ValueError(f"Invalid language: {language}")
        self.language = language

    def get_chunk_prompt(self, chunk):
        if self.language == "en":
            chunk_prompt = f"Summarize the transcript:\n\n{chunk}"
        elif self.language == "zh-tw":
            chunk_prompt = f"請用中文總結，並加上標點符號:\n {chunk}"
        return chunk_prompt
    def get_consolidated_prompt(self, chunk_responses):
        if self.language == "en":
            consolidated_prompt = f"Consoloidate these summaries::\n\n{chunk_responses}"
        elif self.language == "zh-tw":
            consolidated_prompt = f"整合這些會議摘要:\n\n{chunk_responses}"
        return consolidated_prompt

