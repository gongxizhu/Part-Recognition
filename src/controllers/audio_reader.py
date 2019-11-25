import os
import sys
import wave
import numpy as np
from pyaudio import PyAudio, paInt16


class AudioReader(object):
    cap = None
    off = False


    def __init__(self):
        self.sampling_rate = 8000
        self.num_samples = 2000
        self.level = 1000
        self.count_num = 20
        self.save_length = 8
        self.time_count = 8
        pa = PyAudio()
        self.stream = pa.open(format=paInt16, channels=1, rate=self.sampling_rate, input=True,
                         frames_per_buffer=self.num_samples)


    def read_audio(self):
        save_count = 0
        save_buffer = []
        time_count = self.time_count

        while True:
            time_count -= 1

            string_audio_data = self.stream.read(self.num_samples)
            audio_data = np.fromstring(string_audio_data, dtype=np.short)
            large_sample_count = np.sum(audio_data > self.level)
            #print(np.max(audio_data), "large_sample_count=>", large_sample_count)
            if large_sample_count > self.count_num:
                save_count = self.save_length
            else:
                save_count -= 1
            if save_count < 0:
                save_count = 0

            if save_count > 0:
                save_buffer.append(string_audio_data)
            else:
                if len(save_buffer) > 0:
                    break

            if time_count == 0:
                break

        voice_string = save_buffer
        save_buffer = []

        return voice_string