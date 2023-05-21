import asyncio
import re
from abc import ABC, abstractmethod

from EdgeGPT import Chatbot, ConversationStyle, NotAllowedToAccess
from loguru import logger


class Chatter(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def new_chat(self):
        pass

    @abstractmethod
    def add_reply(self, message):
        pass

    @abstractmethod
    def close_chat(self):
        pass


class EdgeGPT(Chatter):
    def __init__(self, promt):
        self.chatter = None

        try:
            self.new_chat(promt)
        except NotAllowedToAccess:
            raise ConnectionRefusedError("Update cookies to Bing Search!")
        except Exception as error:
            raise error

    def new_chat(self, promt):
        if self.chatter is not None:
            self.close_chat()
        self.promnt = promt
        self.is_first_reply = True
        self.chatter = Chatbot()

    async def async_add_reply(self, message):
        if self.get_is_first_reply():
            message = "{} \n\n {}".format(self.promnt, message)

        return await self.chatter.ask(prompt=message,
                                      conversation_style=ConversationStyle.creative,
                                      wss_link="wss://sydney.bing.com/sydney/ChatHub")

    def add_reply(self, message):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:  # 'RuntimeError: There is no current event loop...'
            loop = None

        if loop and loop.is_running():
            tsk = loop.create_task(self.async_add_reply(message))
            reply = tsk.result()
        else:
            reply = asyncio.run(self.async_add_reply(message))
        if "text" not in reply['item']['messages'][1]:
            logger.exception("EdgeGPT return empty respond!\n\n {}".format(reply), format="{time} {level} {message}")
            return "EdgeGPT returned empty respond!"
        return self._fix_output(reply['item']['messages'][1]['text'])

    def close_chat(self):
        self.chatter.close()
        self.chatter = None
        self.promnt = None

    def get_is_first_reply(self):
        if self.is_first_reply == False:
            return False
        self.is_first_reply = False
        return True

    @staticmethod
    def _fix_output(output_txt: str) -> str:
        output_txt = re.sub("\[\^[0-9]+\^\]", '', output_txt)
        output_txt.replace(" , это Bing", "")
        output_txt.replace(" , Bing", "")
        return output_txt


class CowGPT(Chatter):
    def __init__(self, promt=""):
        self.is_first_reply = None
        self.chatter = None
        self.new_chat(promt)

    def new_chat(self, promt=""):
        if self.chatter is not None:
            self.close_chat()
        self.promnt = promt
        self.is_first_reply = True
        self.chatter = "Chatbot"

    def add_reply(self, message):
        return "Moo-moo, moo-moo"

    def close_chat(self):
        self.chatter = None
        self.promnt = None

    def get_is_first_reply(self):
        if not self.is_first_reply:
            return False
        self.is_first_reply = False
        return True


def _main():
    # cookies_path = r"C:\Users\dex\Desktop\gpt4free\AudioChatGPT\configs\cookies_edge.json"
    prompt = "You are an english teacher and you need to explain teachable way:"
    bot = EdgeGPT(promt=prompt)
    print('prompt {}'.format(prompt))

    asking = "Explain me something about conditional sentences?"
    print('asking {}'.format(asking))
    response = bot.add_reply(asking)
    print("reply: {}".format(response))

    asking = "Give me some examples"
    print('asking {}'.format(asking))
    response = bot.add_reply(asking)
    print("reply: {}".format(response))


if __name__ == "__main__":
    _main()
