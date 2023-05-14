import base64
import os
import pickle
from pathlib import Path
from random import randrange

import streamlit as st
from streamlit_chat import message

# from .agi.chat_gpt import create_gpt_completion
# from .stt import show_voice_input
# from .tts import show_audio_player
from constants import BUG_REPORT_URL, REPO_URL

conversations_file = "conversations.pkl"


def clear_chat() -> None:
    st.session_state.generated = []
    st.session_state.past = []
    st.session_state.messages = []
    st.session_state.user_text = ""
    st.session_state.seed = randrange(10 ** 8)  # noqa: S311
    st.session_state.costs = []
    st.session_state.total_tokens = []


def show_text_input() -> None:
    st.text_area(label=st.session_state.locale.chat_placeholder, value=st.session_state.user_text, key="user_text")


def get_user_input():
    match st.session_state.input_kind:
        case st.session_state.locale.input_kind_1:
            show_text_input()
        case st.session_state.locale.input_kind_2:
            print("check")
            # show_voice_input()
        case _:
            show_text_input()


def show_chat_buttons() -> None:
    b0, b1, b2 = st.columns(3)
    with b0, b1, b2:
        b0.button(label=st.session_state.locale.chat_run_btn)
        b1.button(label=st.session_state.locale.chat_clear_btn, on_click=clear_chat)
        b2.download_button(
            label=st.session_state.locale.chat_save_btn,
            data="\n".join([str(d) for d in st.session_state.messages[1:]]),
            file_name="ai-talks-chat.json",
            mime="application/json",
        )


def show_chat(ai_content: str, user_text: str) -> None:
    if ai_content not in st.session_state.generated:
        # store the ai content
        st.session_state.past.append(user_text)
        st.session_state.generated.append(ai_content)
    if st.session_state.generated:
        for i in range(len(st.session_state.generated)):
            message(st.session_state.past[i], is_user=True, key=str(i) + "_user", seed=st.session_state.seed)
            message("", key=str(i), seed=st.session_state.seed)
            st.markdown(st.session_state.generated[i])
            st.caption(f"""
                {st.session_state.locale.tokens_count}{st.session_state.total_tokens[i]} |
                {st.session_state.locale.message_cost}{st.session_state.costs[i]:.5f}$
            """, help=f"{st.session_state.locale.total_cost}{sum(st.session_state.costs):.5f}$")


def show_gpt_conversation() -> None:
    ai_content = "DUMMY_OUTPUT"
    st.session_state.messages.append({"role": "assistant", "content": "DUMMY_OUTPUT"})
    if ai_content:
        show_chat(ai_content, st.session_state.user_text)
        st.divider()
        # show_audio_player(ai_content)


def show_conversation() -> None:
    if st.session_state.messages:
        st.session_state.messages.append({"role": "user", "content": st.session_state.user_text})
    else:
        ai_role = f"{st.session_state.locale.ai_role_prefix} {st.session_state.role}. {st.session_state.locale.ai_role_postfix}"  # NOQA: E501
        st.session_state.messages = [
            {"role": "system", "content": ai_role},
            {"role": "user", "content": st.session_state.user_text},
        ]
    # todo apply chatting classes show_gpt_conversation()


def load_conversations():
    try:
        with open(conversations_file, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return []
    except EOFError:
        return []


def save_conversations(conversations, current_conversation):
    updated = False
    for idx, conversation in enumerate(conversations):
        if conversation == current_conversation:
            conversations[idx] = current_conversation
            updated = True
            break
    if not updated:
        conversations.append(current_conversation)

    temp_conversations_file = "temp_" + conversations_file
    with open(temp_conversations_file, "wb") as f:
        pickle.dump(conversations, f)

    os.replace(temp_conversations_file, conversations_file)


def delete_conversation(conversations, current_conversation):
    for idx, conversation in enumerate(conversations):
        conversations[idx] = current_conversation
        break
    conversations.remove(current_conversation)

    temp_conversations_file = "temp_" + conversations_file
    with open(temp_conversations_file, "wb") as f:
        pickle.dump(conversations, f)

    os.replace(temp_conversations_file, conversations_file)


def exit_handler():
    print("Exiting, saving data...")
    # Perform cleanup operations here, like saving data or closing open files.
    save_conversations(st.session_state.conversations, st.session_state.current_conversation)


def show_info(icon: Path) -> None:
    st.divider()

    st.markdown(f"""### :page_with_curl: {st.session_state.locale.footer_title}""", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align: justify;'>{st.session_state.locale.responsibility_denial}</div>",
                unsafe_allow_html=True)
    st.markdown(f"Project [repo on github]({REPO_URL}) waiting for your :star: | [report]({BUG_REPORT_URL}) a bug")


def render_svg(svg: Path) -> str:
    """Renders the given svg string."""
    with open(svg) as file:
        b64 = base64.b64encode(file.read().encode("utf-8")).decode("utf-8")
        return f"<img src='data:image/svg+xml;base64,{b64}'/>"
