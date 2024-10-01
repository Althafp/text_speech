from transformers import pipeline
from gtts import gTTS

def summarize_text(text):
    # Load the summarization pipeline
    summarizer = pipeline("summarization")
    # Perform summarization
    summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
    return summary[0]['summary_text']

def text_to_speech(text, filename="summary_audio.mp3"):
    # Convert text to speech
    tts = gTTS(text=text, lang='en')
    tts.save(filename)
    return filename

def main():
    # Prompt user for input text
    print("Please enter the text you want to summarize and convert to speech:")
    input_text = input()

    # Summarize the text
    summary = summarize_text(input_text)
    print("Summary:", summary)
    
    # Convert summary to speech
    audio_file = text_to_speech(summary)
    print(f"Generated audio file: {audio_file}")

# Run the main function
if __name__ == "__main__":
    main()
