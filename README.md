# Bard-Tuber
This code is designed to read chat messages from YouTube and Hearing from microphone and then utilize Bard language model to generate responses. The output from Bard is then read out loud using a TTS (Text-to-Speech) engine provided by pyttsx3.


# Setup
Install dependencies
```
git clone https://github.com/Fadlay/Bard-Tuber.git
cd Bard-Tuber
pip install -r requirements.txt
```
It also requires [`ffmpeg`](https://ffmpeg.org/) to be installed

# Usage
Edit the `Token` in `run.py`

Edit the `openai.api_key` in `run.py`

`Token` is the API key for BardAI. Found [here](https://bard.google.com/)
Go to https://bard.google.com/

```
F12 for console
Copy the values
    Session: Go to Application → Cookies → __Secure-1PSID. Copy the value of that cookie.
```

`openai.api_key` is the API key for OpenAI. Found [here](https://platform.openai.com/account/api-keys)

Edit the `start.bat` put video yt-id or run `run.py`

### Default TTS
```
python run.py --video_id STREAMID 
```
## Notes
Replace `STREAMID` with the stream's ID that you can find on the Youtube Stream link


# Other
I used [This VTS plugin](https://lualucky.itch.io/vts-desktop-audio-plugin) to make her mouth move

Please note that this project was created solely for fun and as part of a YouTube video, so the quality and reliability of the code may be questionable. Nonetheless, we hope that this project can serve as a source of inspiration for anyone interested in building their own AI Vtuber.

- [x] Clean up
- [ ] GUI
- [ ] Executables (exe, bat or sh)
- [ ] Extra features (maybe) (Prompt injection protection, questions only mode, virtual audio)

# credit
https://github.com/Koischizo/AI-Vtuber

https://github.com/acheong08/Bard
