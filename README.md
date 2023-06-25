# AI-Tuber
This code is designed to read chat messages from YouTube and then utilize Bard language model to generate responses. The output from Bard is then read out loud using a TTS (Text-to-Speech) engine provided by ElevenLabs.


# Setup
Install dependencies
```
git clone [https://github.com/](https://github.com/RDGitHubZ/AI-Tuber.git)
cd AI-Vtuber
pip install -r requirements.txt
```
It also requires [`ffmpeg`](https://ffmpeg.org/) to be installed

# Usage

Edit the variables `EL_key` in `config.json`

Edit the `Token` in `run.py`

`EL_key` is the API key for [ElevenLabs](https://beta.elevenlabs.io/). Found in Profile Settings

`Token` is the API key for BardAI. Found [here](https://bard.google.com/)
Go to https://bard.google.com/
```
F12 for console
Copy the values
    Session: Go to Application → Cookies → __Secure-1PSID. Copy the value of that cookie.
```

Edit the `start.bat` put video yt-id or run `run.py`

### Default TTS
```
python run.py -id STREAMID 
```
### Elevenlabs TTS
```
python run.py -id STREAMID -tts EL 
```
then you're set
## Notes
Replace `STREAMID` with the stream's ID that you can find on the Youtube Stream link

You can change the voice by changing `voice` in `config.json`. You can find the ID's [here](https://api.elevenlabs.io/docs) in `Get Voices`


# Other
I used [This VTS plugin](https://lualucky.itch.io/vts-desktop-audio-plugin) to make her mouth move

Please note that this project was created solely for fun and as part of a YouTube video, so the quality and reliability of the code may be questionable. Also, after the completion of the project checklist, there won't be much activity in updating or improving this repository. Nonetheless, we hope that this project can serve as a source of inspiration for anyone interested in building their own AI Vtuber.

- [x] Clean up
- [ ] GUI
- [ ] Executables (exe, bat or sh)
- [ ] Extra features (maybe) (Prompt injection protection, questions only mode, virtual audio)

# credit
https://github.com/Koischizo/AI-Vtuber
https://github.com/meet447/MeuxVtuber
