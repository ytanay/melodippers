import numpy as np
import sys
import librosa
import json


# Some magic number defaults, FFT window and hop length
N_FFT = 2048

# We use a hop of 512 here so that the HPSS spectrogram input
# matches the default beat tracker parameters
HOP_LENGTH = 512


def hpss_beats(input_file):

	# Load the file
	print('Loading  ', input_file)
	y, sr = librosa.load(input_file)

	# Do HPSS
	print('Harmonic-percussive separation ... ')
	y_harmonic, y_percussive = librosa.effects.hpss(y)

	# Construct onset envelope from percussive component
	print('Tracking beats on percussive component')
	onset_env = librosa.onset.onset_strength(y=y_percussive,
											 sr=sr,
											 hop_length=HOP_LENGTH,
											 n_fft=N_FFT,
											 aggregate=np.median)

	# Track the beats
	tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env,
										   sr=sr,
										   hop_length=HOP_LENGTH)

	onset_frames = librosa.onset.onset_detect(y=y_percussive, sr=sr, onset_envelope=onset_env, hop_length=HOP_LENGTH)

	print('Computed tempo is {}'.format(tempo))

	beat_times = librosa.frames_to_time(beats,
										sr=sr,
										hop_length=HOP_LENGTH)

	onset_times = librosa.frames_to_time(onset_frames, sr=sr, hop_length=HOP_LENGTH)

	return beat_times, onset_times

