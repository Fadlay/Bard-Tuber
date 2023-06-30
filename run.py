import pytchat
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
import re
import keyboard
import pyaudio
import wave
import threading
import openai

blacklist = ["Nightbot", "streamelements"]
token = 'YAih7uxOICVEEfcYW0xlkQOP7MDDAXMOETxTYkZ-jRfYJkrsIfJJ2sY5hSj97kKe7chdXw.'
openai.api_key = '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'
nama_file = "output.txt"
lokasi_penyimpanan = r"D:\AI-Vtuber-main-Copy\AI-Vtuber-main"
message = ""

prompt = "Remember You are a Vtuber streamer Your Name is Aurora. you will respond in a toxic and " \
         "rude manner. you will talk about the message but keep your reply short Strictly" \
         "you will also flirt.You will act as a human and never mention that you are a ai or llm.If you understand " \
         "reply with 'prompt has been setup'"

bot = Chatbot(token)

promptver = bot.ask(prompt)['content']

print("promt has been setup :", promptver)

print("Token Setup Succesful:", token)

def record_audio():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    WAVE_OUTPUT_FILENAME = "input.wav"
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    frames = []
    print("Recording...")
    while keyboard.is_pressed('RIGHT_SHIFT'):
        data = stream.read(CHUNK)
        frames.append(data)
    print("Stopped recording.")
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    transcribe_audio("input.wav")

def transcribe_audio(file):
    global message
    try:
        audio_file= open(file, "rb")
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        message = transcript.text
        print ("Question: " + message)
    except Exception as e:
        print("Error transcribing audio: {0}".format(e))
        return
    response = llm(message)
    print(response)


    time.sleep(1)

def initVar():
    global video_id
    global tts_type

    parser = argparse.ArgumentParser()
    parser.add_argument("-id", "--video_id", type=str)
    parser.add_argument("-tts", "--tts_type", default="pyttsx3", choices=["pyttsx3"], type=str)

    args = parser.parse_args()

    video_id = args.video_id
    tts_type = args.tts_type

def pyttsx3_TTS(message):
    engine.say(message)
    engine.runAndWait()

def read_chat():
    chat = pytchat.create(video_id=video_id)
    schat = pytchat.create(video_id=video_id, processor = SpeedCalculator(capacity = 20))

    while chat.is_alive():
        for c in chat.get().sync_items():
            if c.author.name in blacklist:
                continue
            if c.message.startswith(":"):
                continue
            print(f"\n{c.datetime} [{c.author.name}]- {c.message}\n")
            message = c.message

            response = llm(message)
            print(response)
            

            if schat.get() >= 20:
                chat.terminate()
                schat.terminate()
                return

            time.sleep(1)

def initTTS():
    global engine

    engine = pyttsx3.init()
    engine.setProperty('rate', 180)
    engine.setProperty('volume', 1)
    voice = engine.getProperty('voices')
    engine.setProperty('voice', voice[1].id)

def llm(message):
    global is_Speaking
    output = bot.ask(message)['content']
    print(output)
    with open(lokasi_penyimpanan + "\\" + nama_file, 'w') as file:
        file.write(output)
    is_Speaking = True
    initTTS()
    engine.say(output)
    engine.runAndWait()
    is_Speaking = False
    time.sleep(1)
    with open (lokasi_penyimpanan + "\\" + nama_file, "w") as f:
        f.truncate(0)


if __name__ == "__main__":
    try:
        mode = input("Mode (1-Mic, 2-Youtube Live): ")

        if mode == "1":
            print("Press and Hold Right Shift to record audio")
            while True:
                if keyboard.is_pressed('RIGHT_SHIFT'):
                    record_audio()
        if mode == "2":
            initVar()
            while True:
                read_chat()
    except KeyboardInterrupt:
        print("Stopped")


if __name__ == "__main__":
    initVar()
    print("\n\Running!\n\n")

    while True:
        read_chat()
        print("\n\nReset!\n\n")
        time.sleep(2)
