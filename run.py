import os
import pytchat
from pytchat import LiveChat, SpeedCalculator
from Bard import Chatbot
import time
from pydub import AudioSegment
from pydub.playback import play
import argparse
import keyboard
import pyaudio
import wave
import openai
import torch
import torchaudio
import winsound
import io
import speech_recognition as sr

blacklist = ["Nightbot"]
token = 'Bard-API-Token'
openai.api_key = 'OpenAI-API'
name_file = "output.txt"
saving_location = r"D:\AI-Vtuber-mains-Copy\AI-Vtuber-main"
message = ""

prompt = "Remember You are a female streamer Your Name is [Your Vtuber Name].People call you Aria you will respond in a funny, toxic and " \
         "rude manner. you will talk about the message but keep your reply short around 5 - 6 words Strictly no more and no less!. " \
         "you will also flirt.Your Creator name is [Your Name]. If you understand " \
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
    response = llmn(message)
    print(response)


    time.sleep(1)

def silero_tts(tts, language, model, speaker):
    device = torch.device('cpu')
    torch.set_num_threads(4)
    local_file = 'model.pt'

    if not os.path.isfile(local_file):
        torch.hub.download_url_to_file(f'https://models.silero.ai/models/tts/{language}/{model}.pt',
                                    local_file)  

    model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
    model.to(device)

    example_text = "i'm fine thank you and you?"
    sample_rate = 48000

    audio_paths = model.save_wav(text=tts,
                                 speaker=speaker,
                                sample_rate=sample_rate)
                                
def read_chat(video_id):
    chat = pytchat.create(video_id=video_id)
    schat = pytchat.create(video_id=video_id, processor = SpeedCalculator(capacity = 20))

    while chat.is_alive():
        for c in chat.get().sync_items():
            if c.author.name in blacklist:
                continue
            if c.message.startswith(":"):
                continue
            if c.message.startswith("@"):
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

def llm(message):
    global is_Speaking
    output = bot.ask(message)['content']
    print(output)
    with open(saving_location + "\\" + name_file, 'w') as file:
        file.write(output)
    if len (output) > 950:
        while True:
            read_chat()
    else:
        silero_tts(output, "en", "v3_en", "en_21")
        winsound.PlaySound("test.wav", winsound.SND_FILENAME)
        is_Speaking = False
        time.sleep(1)
        with open (saving_location + "\\" + name_file, "w") as f:
            f.truncate(0)

def llms(message):
    global is_Speaking
    output = bot.ask(message)['content']
    print(output)
    with open(saving_location + "\\" + name_file, 'w') as file:
        file.write(output)
    if len (output) > 950:
        while True:
            mode_2()
    else:
        silero_tts(output, "en", "v3_en", "en_21")
        winsound.PlaySound("test.wav", winsound.SND_FILENAME)
        is_Speaking = False
        time.sleep(1)
        with open (saving_location + "\\" + name_file, "w") as f:
            f.truncate(0)

def llmn(message):
    global is_Speaking
    output = bot.ask(message)['content']
    print(output)
    with open(saving_location + "\\" + name_file, 'w') as file:
        file.write(output)
    if len (output) > 950:
        while True:
            record_audio()
    else:
        silero_tts(output, "en", "v3_en", "en_21")
        winsound.PlaySound("test.wav", winsound.SND_FILENAME)
        is_Speaking = False
        time.sleep(1)
        with open (saving_location + "\\" + name_file, "w") as f:
            f.truncate(0)

def mode_2():
    global is_Speaking
    text = input("Send a Messages: ")
    while True:
        llms(text)
        is_Speaking = False
        time.sleep(1)
        mode_2()

def mod():
    mode = input("Mode (1-Mic, 2-Owner Chat, 3-Youtube Live, 4-Exit): ")

    if mode == "1":
        print("Press and Hold Right Shift to record audio")
        while True:
            if keyboard.is_pressed('RIGHT_SHIFT'):
                record_audio()
            if keyboard.is_pressed('Left_Shift'):
                mod()
    if mode == "2":
            mode_2()

    if mode == "3":
        video_id = input("Livestream ID: ")
        while True:
            read_chat(video_id)

    if mode == "4":
        exit

if __name__ == "__main__":
    try:
        mode = input("Mode (1-Mic, 2-Owner Chat, 3-Youtube Live, 4-Exit): ")

        if mode == "1":
            print("Press and Hold Right Shift to record audio")
            while True:
                if keyboard.is_pressed('RIGHT_SHIFT'):
                    record_audio()
                if keyboard.is_pressed('Left_Shift'):
                    mod()
        if mode == "2":
            mode_2()

        if mode == "3":
            video_id = input("Livestream ID: ")
            while True:
                read_chat(video_id)

        if mode == "4":
            exit
    except KeyboardInterrupt:
        print("Stopped")
