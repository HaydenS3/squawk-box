# Author: Hayden Schroeder
# Description: Simple listener for respeaker pi hat. With this class I should be able to easily pull, analyze, then write interesting data to a wav file.

import pyaudio
import wave

RESPEAKER_RATE = 16000
RESPEAKER_CHANNELS = 2
RESPEAKER_WIDTH = 2
# run getDeviceInfo.py to get index
RESPEAKER_INDEX = 1  # refer to input device id
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

class Listener:
    p = pyaudio.PyAudio()

    def __init__(self):
        self.stream = self.p.open(
            rate=RESPEAKER_RATE,
            format=self.p.get_format_from_width(RESPEAKER_WIDTH),
            channels=RESPEAKER_CHANNELS,
            input=True,
            input_device_index=RESPEAKER_INDEX,
        )

    def __del__(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    def get_next_frames(self, n):
        frames = []
        for i in range(n):
            data = self.stream.read(CHUNK)
            frames.append(data)
        return frames

    def write_wav(self, frames, filename=WAVE_OUTPUT_FILENAME):
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(RESPEAKER_CHANNELS)
            wf.setsampwidth(self.p.get_sample_size(self.p.get_format_from_width(RESPEAKER_WIDTH)))
            wf.setframerate(RESPEAKER_RATE)
            wf.writeframes(b''.join(frames))
            wf.close()

    def detect_squawk(self, frames):
        # Placeholder for squawk detection logic
        # This function should analyze the frames and return True if a squawk is detected
        # Simple detection logic will look for audio to surpass a dB threshold within the squawk frequency range
        return False

    def listen(self):
        print("Listening for squawks...")
        while True:
            frames = self.get_next_frames(1)
            if self.detect_squawk(frames):
                print("Squawk detected!")
                self.write_wav(frames)
