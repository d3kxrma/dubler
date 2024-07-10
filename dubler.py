from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip, vfx
import pydub
import tempfile
from time import perf_counter
from config import input_video_name, output_video_name, source_lang, target_lang
from Modules.STT.vosk_stt import STT
from Modules.translator.google_translator import Translator
from Modules.TTS.google_tts import TTS

original_video = VideoFileClip(input_video_name)
audio_name = input_video_name.replace(".mp4", ".mp3")
original_video.audio.write_audiofile(audio_name, verbose=False, logger=None)

def find_speech(audio_name, volume_threshold=-22, duration_threshold=800, offset=100):
    audio = pydub.AudioSegment.from_file(audio_name)
    
    speech = []
    start = None
    last_quiet = None
    for i in range(len(audio)):
        if start is None:
            if audio[i].dBFS >= volume_threshold:
                start = i
                if i > offset:
                    start = i - offset
        else:
            if audio[i].dBFS < volume_threshold and last_quiet is None:
                last_quiet = i
            elif audio[i].dBFS >= volume_threshold:
                last_quiet = None
            if audio[i].dBFS < volume_threshold and i - last_quiet >= duration_threshold:
                speech.append((start/1000, last_quiet/1000))
                start = None
                last_quiet = None
    return speech

def describe_speech(speech):
    stt = STT()
    described_speech = []
    for start, end in speech:
        clip = original_video.audio.subclip(start, end)
        with tempfile.NamedTemporaryFile(suffix=".wav") as f:
            clip.write_audiofile(f.name)
            text = stt.recognize(f.name)
        
        described_speech.append({"start": start, "end": end, "text": text})
    
    return described_speech


def translate_speech(speech, source, target):
    translator = Translator(source, target)
    translated_speech = []
    for s in speech:
        translated_text = translator.translate(s["text"])
        translated_speech.append({"start": s["start"], "end": s["end"], "text": translated_text})
    return translated_speech

def generate_translated_speech(translated_speech, lang):
    tts = TTS(lang)
    clips = []
    for s in translated_speech:
        try:
            clip = tts.say(s["text"])
            clips.append({"start": s["start"], "end": s["end"], "clip": clip})
        except:
            print(f"Can't generate speech for {s['start']} - {s['end']}")
    return clips

def resize_audio_clip(translated_speech):
    clips = []
    for s in translated_speech:
        clip: AudioFileClip = s["clip"]
        coefficient = clip.duration / (s["end"] - s["start"])
        clip = clip.fx(vfx.speedx, coefficient)
        clips.append({"start": s["start"], "end": s["end"], "clip": clip})
    return clips

def replace_speech(video: VideoFileClip, clips):
    video_parts = []
    privious_end = 0
    for s in clips:
        not_changed = video.subclip(privious_end, s["start"])
        video_parts.append(not_changed)
        
        clip_w_audio = video.subclip(s["start"], s["end"]).set_audio(s["clip"])
        video_parts.append(clip_w_audio)
        privious_end = s["end"]
    if privious_end < video.duration:
        video_parts.append(video.subclip(privious_end, video.duration))
    final_video = concatenate_videoclips(video_parts)
    final_video.write_videofile("final.mp4", verbose=False)
    
        


if __name__ == "__main__":
    print("Start detecting speech")
    
    start = perf_counter()
    st = perf_counter()
    speech = find_speech(audio_name)
    # print(speech)
    print(f"Find {len(speech)} phrases")
    print(f"Time: {perf_counter() - st}")
    
    print("Start describing speech")
    st = perf_counter()
    des = describe_speech(speech)
    end = perf_counter()
    print("Speech described")
    print(f"Time: {end - st}")
    
    print("Start translating speech")
    st = perf_counter()
    tra = translate_speech(des, source_lang, target_lang)
    print("Speech translated")
    print(f"Time: {perf_counter() - st}")
    
    print("Start generating translated speech")
    st = perf_counter()
    clp = generate_translated_speech(tra, target_lang)
    print("Translated speech generated")
    print(f"Time: {perf_counter() - st}")
    
    print("Start resizing audio clips")
    st = perf_counter()
    s = resize_audio_clip(clp)
    print("Audio clips resized")
    print(f"Time: {perf_counter() - st}")
    
    print("Start replacing speech")
    st = perf_counter()
    replace_speech(original_video, s)
    print("Speech replaced")
    print(f"Time: {perf_counter() - st}")
    
    print(f"Total time: {perf_counter() - start}")