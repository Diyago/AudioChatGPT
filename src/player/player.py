from pydub import AudioSegment
from pydub.playback import play

PY_SSIZE_T_CLEAN = 0


class WavPlayer:
    """
    A class that plays WAV audio files.
    """

    @staticmethod
    def read_play(file_path):
        """
        Initializes the WavPlayer instance with the file path of the WAV audio file to play.
        And then plays the WAV audio file.

        Args:
            file_path (str): The file path of the WAV audio file to play.
        """
        # todo add different formats
        sound = AudioSegment.from_file(file_path, format="wav")
        play(sound)


if __name__ == "__main__":
    WavPlayer.read_play("../text_readers/output.wav")
