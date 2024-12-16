import re
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load the tokenizer and model for summarization
tokenizer = AutoTokenizer.from_pretrained("csebuetnlp/mT5_multilingual_XLSum")
model = AutoModelForSeq2SeqLM.from_pretrained("csebuetnlp/mT5_multilingual_XLSum")

def read_captions(file_path):
    """
    Read captions from an SRT file and return as plain text.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        
        # Remove timestamps and formatting
        content = re.sub(r'(\d+\n)|(\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3})|(\n\n)', '', content)
        
        return content.strip()

def summarize_text(text):
    """
    Generate a summary of the provided text using the mT5 model.
    """
    # Tokenize the input text
    inputs = tokenizer(text, return_tensors="pt", max_length=512, truncation=True)

    # Generate summary
    summary_ids = model.generate(inputs['input_ids'], max_length=150, min_length=30, length_penalty=2.0, num_beams=4, early_stopping=True)

    # Decode the generated summary
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    
    return summary

def main():
    # Path to your SRT file
    caption_file = "C:/Users/kirth/Downloads/01_module-introduction.srt"  # Update this path

    # Read captions from the file
    captions = read_captions(caption_file)

    # Generate summary using mT5 model
    summary = summarize_text(captions)

    # Print the generated summary
    print("Summary:")
    print(summary)

if __name__ == "__main__":
    main()
