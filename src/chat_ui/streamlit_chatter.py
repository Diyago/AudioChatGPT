import sys
from pathlib import Path
from random import randrange
from typing import Dict

import streamlit as st
from loguru import logger
from streamlit_option_menu import option_menu

from constants import HEADER_STYLES
from streamlit_locale import en, ru
# from src.styles.menu_styles import FOOTER_STYLES, HEADER_STYLES
from utils_conversation import get_user_input, show_chat_buttons, show_conversation, show_info

FOOTER_STYLES: Dict[str, Dict] = {

}

# --- PATH SETTINGS ---
current_dir: Path = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file: Path = current_dir / "./styles/.css"
assets_dir: Path = current_dir / "assets"
icons_dir: Path = assets_dir / "icons"
img_dir: Path = assets_dir / "img"
tg_svg: Path = icons_dir / "tg.svg"

# --- GENERAL SETTINGS ---
PAGE_TITLE: str = "AudioChatGPT"
PAGE_ICON: str = "⚛"
LANG_EN: str = "En"
LANG_RU: str = "Ru"
AI_MODEL_OPTIONS: list[str] = [
    "CowGPT",
    "EdgeGPT",

]
# Add a button to create a new conversation
logger.add(sys.stdout, colorize=True, format="<green>{time}</green> <level>{message}</level>")

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)

# --- LOAD CSS ---
with open(css_file) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

selected_lang = option_menu(
    menu_title=None,
    options=[LANG_EN, LANG_RU, ],
    icons=["globe2", "translate"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles=HEADER_STYLES
)

# Storing The Context
if "locale" not in st.session_state:
    st.session_state.locale = en
if "generated" not in st.session_state:
    st.session_state.generated = []
if "past" not in st.session_state:
    st.session_state.past = []
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_text" not in st.session_state:
    st.session_state.user_text = ""
if "input_kind" not in st.session_state:
    st.session_state.input_kind = st.session_state.locale.input_kind_1
if "seed" not in st.session_state:
    st.session_state.seed = randrange(10 ** 3)
if 'input_field_key' not in st.session_state:
    st.session_state['input_field_key'] = 0


def main() -> None:
    """
    Main function to display the user interface and handle user interactions.
    """
    c1, c2 = st.columns(2)
    with c1, c2:
        c1.selectbox(label=st.session_state.locale.select_placeholder1, key="model", options=AI_MODEL_OPTIONS,)
        st.session_state.input_kind = c2.radio(
            label=st.session_state.locale.input_kind,
            options=(st.session_state.locale.input_kind_1, st.session_state.locale.input_kind_2),
            horizontal=True,
        )
        role_kind = c1.radio(
            label=st.session_state.locale.radio_placeholder,
            options=(st.session_state.locale.radio_text1, st.session_state.locale.radio_text2),
            horizontal=True,
        )
        match role_kind:
            case st.session_state.locale.radio_text1:
                c2.selectbox(label=st.session_state.locale.select_placeholder2, key="role",
                             options=st.session_state.locale.ai_role_options)
            case st.session_state.locale.radio_text2:
                c2.text_input(label=st.session_state.locale.select_placeholder3, key="role")

    if st.session_state.user_text:
        show_conversation()
        st.session_state.user_text = ""
    get_user_input()
    show_chat_buttons()


def run_agi():
    """
    Run the AudioChatGPT interface based on the selected language and display the appropriate content.
    """
    match selected_lang:
        case "En":
            st.session_state.locale = en
        case "Ru":
            st.session_state.locale = ru
        case _:
            st.session_state.locale = en
    st.markdown(f"<h1 style='text-align: center;'>{st.session_state.locale.title}</h1>", unsafe_allow_html=True)
    selected_footer = option_menu(
        menu_title=None,
        options=[
            st.session_state.locale.footer_option1,
            st.session_state.locale.footer_option0,
        ],
        icons=["info-circle", "chat-square-text", "piggy-bank"],  # https://icons.getbootstrap.com/
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles=FOOTER_STYLES
    )
    match selected_footer:
        case st.session_state.locale.footer_option0:
            main()
        case st.session_state.locale.footer_option1:
            show_info(tg_svg)
        case _:
            show_info(tg_svg)


if __name__ == "__main__":
    run_agi()
