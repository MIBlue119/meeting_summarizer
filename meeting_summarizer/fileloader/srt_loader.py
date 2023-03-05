
class SrtLoader:
    def __init__(self)->None:
        pass
    
    def load_data(self, file_path: str):
        """Load data from a Srt file.
        
        Extract text from each line.

        Returns:
            str: The text from the Srt file.
        """
        # Load data from file
        with open(file_path, 'r', encoding="utf-8") as file:
            lines = file.readlines()
        #Extract text from each line, skipping time stamps and other metadata
        text = []
        last_line= ""
        for line in lines:
            if "-->" in last_line:
                text.append(line.strip()) # Remove trailing and leading whitespace
            last_line = line

        # Join the lines of text together into a single string
        text = " ".join(text)
        return text        

if __name__ == "__main__":
    file_path = "/Users/weirenlan/Desktop/self_practice/meeting_summarizer/examples/EP108_humannosis_Podcast.srt"
    loader = SrtLoader()
    text = loader.load_data(file_path)
    print(text)