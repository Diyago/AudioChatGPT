import wave

import pyaudio


#todo  change prints to logs
class VoiceRecorder:
    """
    A class for recording voice using PyAudio and saving it as a WAV file.

    Attributes:
    chunk (int): Record in chunks of this many samples.
    sample_format (pyaudio.SampleFormat): Format of each sample.
    channels (int): Number of audio channels.
    fs (int): Record at this many samples per second.
    filename (str): Name of the output WAV file.
    p (pyaudio.PyAudio): Interface to PortAudio.
    stream (pyaudio.Stream): Audio stream for recording.
    frames (list): List of recorded audio frames.
    """

    def __init__(self, chunk=1024, sample_format=pyaudio.paInt16, channels=2, fs=44100, filename="voice_record.wav"):
        self.chunk = chunk
        self.sample_format = sample_format
        self.channels = channels
        self.fs = fs
        self.filename = filename
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.frames = []
        self.get_device_info()

    def get_device_info(self):
        info = self.p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        print("Available microphones:")
        for i in range(0, numdevices):
            if (self.p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels') > 0):
                if i == 0:
                    print("default one: ", self.p.get_device_info_by_host_api_device_index(0, i).get('name'))
                else:
                    print(self.p.get_device_info_by_host_api_device_index(0, i).get('name'))

    def start_recording(self):
        """
        Start recording audio.
        """
        self.stream = self.p.open(format=self.sample_format,
                                  channels=self.channels,
                                  rate=self.fs,
                                  frames_per_buffer=self.chunk,
                                  input=True)
        print('Recording')

        while True:
            data = self.stream.read(self.chunk)
            self.frames.append(data)
            # Check if stop_recording() has been called
            if not self.stream.is_active():
                break

    def stop_recording(self):
        """
        Stop recording audio and save the recorded data as a WAV file.
        """
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

        print('Finished recording')

        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.sample_format))
        wf.setframerate(self.fs)
        wf.writeframes(b''.join(self.frames))
        wf.close()
