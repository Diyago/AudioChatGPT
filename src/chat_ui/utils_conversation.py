import asyncio
import base64
import os
import pickle
import sys
from pathlib import Path
from random import randrange

import streamlit as st
from streamlit_chat import message

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from chats.chatters import CowGPT, EdgeGPT
from player.player import TextToAudio
# from .agi.chat_gpt import create_gpt_completion
# from .stt import show_voice_input
# from .tts import show_audio_player
from constants import BUG_REPORT_URL, REPO_URL

conversations_file = "conversations.pkl"
async_models = ["EdgeGPT"]
bot = None


def clear_chat() -> None:
    st.session_state.generated = []
    st.session_state.past = []
    st.session_state.messages = []
    st.session_state.user_text = ""
    st.session_state.seed = randrange(10 ** 8)
    global bot
    bot = None


def show_text_input() -> None:
    st.text_area(label=st.session_state.locale.chat_placeholder, value=st.session_state.user_text, key="user_text")


def get_user_input():
    match st.session_state.input_kind:
        case st.session_state.locale.input_kind_1:
            show_text_input()
        case st.session_state.locale.input_kind_2:
            # todo implement
            print("Voice_check")
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


def find_indices(list_to_check, item_to_find):
    indices = []
    for idx, value in enumerate(list_to_check):
        if value == item_to_find:
            indices.append(idx)
    return indices


def show_chat(ai_content: str, user_text: str) -> None:
    past_users = find_indices(st.session_state.past, user_text)
    past_ai = find_indices(st.session_state.generated, ai_content)
    if len(set(past_users) & set(past_ai)) == 0:
        st.session_state.past.append(user_text)
        st.session_state.generated.append(ai_content)
    if st.session_state.generated:
        for i in range(len(st.session_state.generated)):
            message(st.session_state.past[i], is_user=True, key=str(i) + "_user", seed=st.session_state.seed)
            message(st.session_state.generated[i], key=str(i), seed=st.session_state.seed)


def show_gpt_conversation() -> None:
    try:
        if st.session_state.model in async_models:
            gpt_reply = asyncio.run(create_async_gpt_completion(st.session_state.model, st.session_state.messages))
        else:
            gpt_reply = create_gpt_completion(st.session_state.model, st.session_state.messages)
        if gpt_reply:
            show_chat(gpt_reply, st.session_state.user_text)
            # st.divider()
            TextToAudio.text_to_audio(gpt_reply)
    except UnboundLocalError as err:
        st.error(err)


async def create_async_gpt_completion(model_name, message):
    global bot
    if bot:
        reply = await bot.add_reply(message[1]['content'])
        return reply
    elif model_name == 'EdgeGPT':
        bot = EdgeGPT(cookies_path=r"C:\Users\dex\Desktop\gpt4free\AudioChatGPT\configs\cookies_edge.json",
                      promt=message[0]['content'])
        reply = await bot.add_reply(message[1]['content'])
        return reply


def create_gpt_completion(model_name, message):
    global bot
    if bot:
        reply = bot.add_reply(message[1]['content'])
        return reply
    elif model_name == 'CowGPT':
        bot = CowGPT(promt=message[0]['content'])
        return bot.add_reply(message[1]['content'])


def show_conversation() -> None:
    if st.session_state.messages:
        st.session_state.messages.append({"role": "user", "content": st.session_state.user_text})
    else:
        ai_role = f"{st.session_state.locale.ai_role_prefix} {st.session_state.role}. {st.session_state.locale.ai_role_postfix}"
        st.session_state.messages = [
            {"role": "system", "content": ai_role},
            {"role": "user", "content": st.session_state.user_text},
        ]
    show_gpt_conversation()


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
