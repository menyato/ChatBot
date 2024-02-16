import speech_recognition as sr
import requests
import pyaudio
import sys  # Import sys module for exiting the script

def speech_to_text(language='en-US'):
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say something...")
        recognizer.adjust_for_ambient_noise(source)

        try:
            audio = recognizer.listen(source, timeout=3)
            transcription = recognizer.recognize_google(audio, language=language)
            print("Transcription:", transcription)

            # Send the transcription to the Flask server
            send_transcription(transcription)

            if transcription.lower() == "quit the program":
                print("Exiting the program.")
                sys.exit()  # Exit the script if the user says "quit"
        except sr.UnknownValueError:
            transcription = "Please Repeat I could not understand"
            send_transcription(transcription)
            print("Please Repeat I could not understand.")
        except sr.WaitTimeoutError:
            print("Timeout occurred. No speech detected.")

def send_transcription(transcription):
    # Define the Flask server URL
    server_url = "http://localhost:5001/receive_transcription"

    # Send a POST request with the transcription data
    response = requests.post(server_url, json={"transcription": transcription})

    # Print the response from the Flask server
    print("Response from server:", response.text)

def audio_receive():
    # Define the Flask server URL
    server_url = "http://localhost:5001/static/output.wav"
    response = requests.get(server_url)
    if response.status_code == 200:
        p = pyaudio.PyAudio()

        # Open stream
        stream = p.open(format=p.get_format_from_width(2),  # Adjust based on your audio data
                        channels=1,  # Adjust based on your audio data
                        rate=22050,  # Adjust based on your audio data
                        output=True)

        stream.write(response.content)

        stream.stop_stream()
        stream.close()
        p.terminate()
    else:
        print(f"Failed to fetch audio from {server_url}")

if __name__ == "__main__":
    while True:
        # For English
        speech_to_text(language='en-US')

        audio_receive()

        # For Arabic
        # speech_to_text(language='ar')
