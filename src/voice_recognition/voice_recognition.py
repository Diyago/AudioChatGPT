"""
Size	Parameters	English-only model	Multilingual model	Required VRAM	Relative speed
tiny	39 M	tiny.en	tiny	~1 GB	~32x
base	74 M	base.en	base	~1 GB	~16x
small	244 M	small.en	small	~2 GB	~6x
medium	769 M	medium.en	medium	~5 GB	~2x
large	1550 M	N/A	large	~10 GB	1x
"""
import whisper


class VoiceRecognizer:
    """
    A class for performing voice recognition using a pre-trained model.
    """

    def __init__(self, model_name: str):
        """
        Initializes the VoiceRecognizer object with the path to the pre-trained model.

        Args:
            model_name (str): The model name of the pre-trained model.
        """
        implemented_list = ["tiny", "base", "small", "medium", "large", \
                            "tiny.en", "base.en", "small.en", "medium.en", \
                            ]
        if model_name not in implemented_list:
            raise NotImplementedError(
                "You provide for VoiceRecognizer next model name: {}, but only {} implemented".format(model_name,
                                                                                                      implemented_list))
        self.model = whisper.load_model(model_name)

    def transcribe(self, audio_path: str) -> str:
        """
        Transcribes the audio file at the given path using the pre-trained model.

        Args:
            audio_path (str): The path to the audio file to transcribe.

        Returns:
            str: The transcribed text.
        """
        result = self.model.transcribe(audio_path)
        return result["text"]


if __name__ == "__main__":
    # Create a VoiceRecognizer object with the path to the pre-trained model
    vr = VoiceRecognizer("base")

    # Transcribe an audio file
    result = vr.transcribe("../text_readers/output.wav")

    # Print the transcribed text
    print(result)
