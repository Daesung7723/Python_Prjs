from gtts import gTTS
from playsound import playsound
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

text = "one two three four"

tts = gTTS(text=text, lang='en')
tts.save("hi.mp3")
playsound("hi.mp3")