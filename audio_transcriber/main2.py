import os
import logging

# Set up logging
logging.basicConfig(filename='transcription.log', level=logging.INFO)

def install_assemblyai():
    print("[*] Assemblyai is not installed")
    print("[*] Installing assemblyai")
    os.system("pip3 install assemblyai -q")
    print("[*] Assemblyai installed successfully")
    print("[*] Restarting the program")
    import assemblyai as aai
    return aai

try:
    import assemblyai as aai
except ImportError:
    aai = install_assemblyai()

# Replace with your API token
api_key = input("[*] Enter your API key: ")

# Validate API key format
if not api_key or len(api_key) != 64:
    print("[*] Invalid API key format")
    exit(1)

aai.settings.api_key = api_key

# Ask the user for the transcription mode (local or online)
while True:
    transcription_mode = input("[*] Select transcription mode (1: Local, 2: Online): ")
    if transcription_mode == '1':
        file_path = input("[*] Enter the local file path: ")
        break
    elif transcription_mode == '2':
        file_url = input("[*] Enter the file URL: ")
        break
    else:
        print("[*] Invalid choice. Please select 1 for local or 2 for online transcription.")

try:
    if transcription_mode == '1':
        if not os.path.isfile(file_path):
            print("[*] File does not exist.")
            exit(1)

        # Transcribe the local file
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(file_path)
    elif transcription_mode == '2':
        # Validate file URL format (you can add more validation logic here)
        if not file_url.startswith("http"):
            print("[*] Invalid file URL format")
            exit(1)

        # Transcribe the online file
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(file_url)
        
    # Formats the text
    text = transcript.text
    print("[*] Transcription complete")
    file_name = input("[*] Enter the file name: ")
    sentences = text.split(". ")
    formatted_text = "\n".join(sentences)

    # Saves the transcription to a file
    with open(f"{file_name}.txt", "w") as f:
        f.write(formatted_text)

    print(f"[*] Transcription saved to {file_name}.txt")
    logging.info(f"Transcription saved to {file_name}.txt")
except Exception as e:
    print("[*] An error occurred during transcription:")
    print(str(e))
    logging.error("Error during transcription:", exc_info=True)
