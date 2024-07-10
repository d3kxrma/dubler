from vosk import Model, KaldiRecognizer
import subprocess

class STT:
    def __init__(self):
        self.model = Model("/home/dekxrma/Стільниця/Main/projects/Python2024/dubler/Models/STT/vosk-model-en-us-0.22")
        self.recognizer = KaldiRecognizer(self.model, 16000)

    def recognize(self, path_to_audio:str):
        with subprocess.Popen(["ffmpeg", "-loglevel", "quiet", "-i",
                                path_to_audio,
                                "-ar", str(16000) , "-ac", "1", "-f", "s16le", "-"],
                                stdout=subprocess.PIPE) as process:

            while True:
                data = process.stdout.read(4000)
                if len(data) == 0:
                    break
                self.recognizer.AcceptWaveform(data)
                
        return eval(self.recognizer.FinalResult())["text"]
        