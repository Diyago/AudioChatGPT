import base64
from io import BytesIO

import streamlit as st
from gtts import gTTS, gTTSError
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


class TextToAudio:
    """
    A class that plays Text to audio
    """

    @staticmethod
    def text_to_audio(text: str) -> None:
        def autoplay_audio(file_path: str):
            with open(file_path, "rb") as f:
                data = f.read()
                b64 = base64.b64encode(data).decode()
                md = f"""
                    <audio autoplay="true">
                    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                    </audio>
                    """
                st.markdown(
                    md,
                    unsafe_allow_html=True,
                )
        sound_file = BytesIO()
        try:
            tts = gTTS(text=text, lang=st.session_state.locale.lang_code)
            tts.write_to_fp(sound_file)
            st.write(st.session_state.locale.stt_placeholder)
            #st.audio(sound_file)
            tts.save('audio.mp3')
            autoplay_audio("audio.mp3")
        except gTTSError as err:
            st.error(err)




if __name__ == "__main__":
    WavPlayer.read_play("../text_readers/output.wav")
