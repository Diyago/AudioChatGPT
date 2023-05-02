from TTS.api import TTS

"""
Available models: tts --list_models
"""


class Custom_TTS(TTS):
    def __init__(self, model_name, num_speaker, num_language, emotion='neutral', speed=1):
        """
        Initializes a new instance of the Custom_TTS class with the specified model name, speaker, and language.

        Args:
            model_name (str): The name of the TTS model to use.
            speaker (str): The name of the speaker to use.
            language (str): The language to use.
        """
        self.model_name = model_name
        self.speaker = num_speaker
        self.language = num_language
        self.emotion = emotion
        self.speed = speed
        self.tts = TTS(model_name, progress_bar=False, gpu=False)

    def tts_to_file(self, text, filename):
        """
        Generates an audio file from the specified text.

        Args:
            text (str): The text to generate audio from.
            filename (str): The name of the output audio file.
        """
        self.tts.tts_to_file(text=text, file_path=filename,
                             speaker=self.tts.speakers[self.speaker],
                             language=self.tts.languages[self.language],
                             emotion=self.emotion,
                             speed=self.speed, )


if __name__ == "__main__":
    custom_tts = Custom_TTS('tts_models/multilingual/multi-dataset/your_tts', num_speaker=0, num_language=0)
    custom_tts.tts_to_file("Hello, world!", "output.wav")
