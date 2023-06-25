import pytchat
import json
from pytchat import LiveChat, SpeedCalculator
from Bard import Chatbot
import time
import requests
from pydub import AudioSegment
from pydub.playback import play
import io
import pyttsx3
import sys
import argparse
import elevenlabs


token = 'Bard-Token.'

prompt = "Remember You are a female streamer Your Name is Aurora. you will respond in a toxic and " \
         "rude manner. you will talk about the message but keep your reply short around 100 - 200 charachters Strictly no more!. " \
         "you will also flirt.You will act as a human and never mention that you are a ai or llm.If you understand " \
         "reply with 'prompt has been setup'"

bot = Chatbot(token)

promptver = bot.ask(prompt)['content']

print("promt has been setup :", promptver)

print("Token Setup Succesful:", token)

def initTTS():
    global engine

    engine = pyttsx3.init()
    engine.setProperty('rate', 180)
    engine.setProperty('volume', 1)
    voice = engine.getProperty('voices')
    engine.setProperty('voice', voice[1].id)


def initVar():
    global EL_key
    global EL_voice
    global video_id
    global tts_type
    global EL

    try:
        with open("config.json", "r") as json_file:
            data = json.load(json_file)
    except:
        print("Unable to open JSON file.")
        exit()


    class EL:
        key = data["keys"][0]["EL_key"]
        voice = data["EL_data"][0]["voice"]

    tts_list = ["pyttsx3", "EL"]

    parser = argparse.ArgumentParser()
    parser.add_argument("-id", "--video_id", type=str)
    parser.add_argument("-tts", "--tts_type", default="pyttsx3", choices=tts_list, type=str)

    args = parser.parse_args()

    video_id = args.video_id
    tts_type = args.tts_type

    if tts_type == "pyttsx3":
        initTTS()


def Controller_TTS(message):
    if tts_type == "EL":
        EL_TTS(message)
    elif tts_type == "pyttsx3":
        pyttsx3_TTS(message)


def pyttsx3_TTS(message):

    engine.say(message)
    engine.runAndWait()


def EL_TTS(message):

    url = f'https://api.elevenlabs.io/v1/text-to-speech/{EL.voice}'
    headers = {
        'accept': 'audio/mpeg',
        'xi-api-key': EL.key,
        'Content-Type': 'application/json'
    }
    data = {
        'text': message,
        'voice_settings': {
            'stability': 0.75,
            'similarity_boost': 0.75
        }
    }

    response = requests.post(url, headers=headers, json=data, stream=True)
    audio_content = AudioSegment.from_file(io.BytesIO(response.content), format="mp3")
    play(audio_content)


def read_chat():

    chat = pytchat.create(video_id=video_id)
    schat = pytchat.create(video_id=video_id, processor = SpeedCalculator(capacity = 20))

    while chat.is_alive():
        for c in chat.get().sync_items():
            print(f"\n{c.datetime} [{c.author.name}]- {c.message}\n")
            message = c.message

            response = llm(message)
            print(response)
            Controller_TTS(response)

            if schat.get() >= 20:
                chat.terminate()
                schat.terminate()
                return

            time.sleep(1)


def llm(message):
    output = bot.ask(message)['content']

    print(output)

    # voice goes here

    # Generate a response
    response = elevenlabs.generate(output)

    # Speak the response
    elevenlabs.play(response)



if __name__ == "__main__":
    initVar()
    print("\n\Running!\n\n")

    while True:
        read_chat()
        print("\n\nReset!\n\n")
        time.sleep(2)
