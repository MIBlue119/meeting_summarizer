

class WebVttLoader:
    def __init__(self)->None:
        pass
    
    def load_data(self, file_path: str):
        """Load data from a WebVTT file.
        
        1.Skip the first line which contains only the WEBVTT header.
        2.Extract text from each line.

        Returns:
            str: The text from the WebVTT file.
        """
        # Load data from file
        with open(file_path, 'r', encoding="utf-8") as file:
            lines = file.readlines()
        # Skip the first line which contains the header
        lines = lines[1:]
        # Extract text from each line, skipping time stamps and other metadata
        text = []
        for line in lines:
            if "-->" not in line:
                text.append(line.strip()) # Remove trailing and leading whitespace
        # Join the lines of text together into a single string
        text = " ".join(text)
        return text        

