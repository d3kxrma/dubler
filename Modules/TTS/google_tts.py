from gtts import gTTS
from moviepy.editor import AudioFileClip
import tempfile
class TTS:
    def __init__(self, lang):
        self.lang = lang
    
    def say(self, text):
        tts = gTTS(text=text, lang=self.lang, slow=False)
        with tempfile.NamedTemporaryFile(suffix=".mp3") as f:
            tts.save(f.name)
            audio_segment = AudioFileClip(f.name)
        return audio_segment
        
if __name__ == "__main__":
    tts = TTS("uk")
    f = tts.say("отже, є новий знімок двадцять чотири w тринадцять, і всі постійно говорять про кут злиття, що баффує булаву, і я думав, що вони збираються це знерфувати, а також кожна рейдова ферма та існування були нервами на шість футів у графіку, але є один інші мережі, які, здається, пройшли зовсім непоміченими, і ця зміна полягає в тому, що злиття нарешті повернуло чашу пари")
    f.write_audiofile("test2.mp3")
        