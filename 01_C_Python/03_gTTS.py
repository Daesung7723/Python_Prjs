from gtts import gTTS
from playsound import playsound
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

text = "현수씨는 바보"

tts = gTTS(text=text, lang='ko')
tts.save("hi.mp3")
playsound("hi.mp3")