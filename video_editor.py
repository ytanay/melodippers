import json
import os
import itertools
import random

from tqdm import tqdm
from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips, AudioFileClip, CompositeVideoClip


CLIPS_PATH = r'clips'

with open('tempo_data.json') as f:
	beat_data = json.load(f)

audio = AudioFileClip(r'assets\example.mp3')

print('Reading clips... {}'.format(CLIPS_PATH))
clips = [VideoFileClip(os.path.join(CLIPS_PATH, x), audio=False) for x in tqdm(os.listdir(CLIPS_PATH))]

subclips = []

last_beat = 0

for beat in tqdm(beat_data[:20]):
	clip = random.choice(clips)
	start_point = random.randrange(0, max(1, int(clip.duration) - 1))
	subclips.append(clip.subclip(start_point, start_point + beat - last_beat))
	last_beat = beat


print('Concatanating...')
final_clip = concatenate_videoclips(subclips)
final_clip = final_clip.set_audio(audio)
final_clip = final_clip.subclip(5, 10)

final_clip.preview(fps=24)

print('Writing...')
final_clip.write_videofile("my_concatenation.mp4", fps=24)