# flask_server.py
from flask import Flask, request , send_file
from chat import chat 
import base64


app = Flask(__name__)

@app.route("/receive_transcription", methods=["POST"])
def receive_transcription():
    data = request.get_json()
    transcription = data.get("transcription")

    # Handle the transcription as needed
    print("Received transcription:", transcription)
    

    # Add your logic here to process the transcription
    resp = chat(transcription)
    return resp


# @app.route("/audio_send", methods=["POST"])
# def audio_send():
#     path_to_file = r"C:\Users\Abdullah Minyato\Documents\GitHub\ChatBot\small_robot\output.wav"

#     with open(path_to_file, "rb") as file:
#         wav_content = file.read()

#     # Perform decoding, for example, using base64
#     decoded_content = base64.b64encode(wav_content).decode('utf-8')

#     return {
#         "decoded_content": decoded_content
#     } ,     



if __name__ == "__main__":
    app.run(port=5001)  # Run the Flask app on a different port


