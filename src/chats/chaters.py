
import asyncio
import json
from abc import ABC, abstractmethod

from EdgeGPT import Chatbot, ConversationStyle


class Chatter(ABC):
    """Abstract base class for chatbots."""
    @abstractmethod
    def __init__(self):
        """Initialize the chatbot."""
        pass

    @abstractmethod
    def new_chat(self):
        """Start a new chat session."""
        pass

    @abstractmethod
    def add_reply(self, message):
        """Add a reply to the chat session."""
        pass

    @abstractmethod
    def close_chat(self):
        """Close the chat session."""
        pass


class EdgeGPT(Chatter):
    """A chatbot that uses EdgeGPT to generate responses."""
    def __init__(self, cookies_path, prompt):
        """
        Initialize the EdgeGPT chatbot.

        Args:
            cookies_path (str): The path to the cookies file.
            prompt (str): The initial prompt for the chat session.
        """
        self.chatter = None
        with open(cookies_path, 'r') as json_file:
            self.cookies = json.load(json_file)
        self.new_chat(prompt)

    def new_chat(self, prompt):
        """
        Start a new chat session.

        Args:
            prompt (str): The initial prompt for the chat session.
        """
        if self.chatter is not None:
            self.close_chat()
        self.prompt = prompt
        self.is_first_reply = True
        self.chatter = Chatbot(cookies=self.cookies)

    async def add_reply(self, message):
        """
        Add a reply to the chat session.

        Args:
            message (str): The message to add to the chat session.

        Returns:
            str: The response generated by the chatbot.
        """
        if self.get_is_first_reply():
            message = "{} \n\n {}".format(self.prompt, message)

        reply = await self.chatter.ask(prompt=message,
                                       conversation_style=ConversationStyle.creative,
                                       wss_link="wss://sydney.bing.com/sydney/ChatHub")
        return reply['item']['messages'][1]['text']

    def close_chat(self):
        """Close the chat session."""
        self.chatter.close()
        self.chatter = None
        self.prompt = None

    def get_is_first_reply(self):
        """
        Check if this is the first reply in the chat session.

        Returns:
            bool: True if this is the first reply, False otherwise.
        """
        if self.is_first_reply == False:
            return False
        self.is_first_reply = False
        return True


async def _main():
    """Run the chatbot."""
    cookies_path = r'C:\Users\dex\Desktop\gpt4free\AudioChatGPT\configs\cookies_edge.json'
    prompt = "You are an english teacher and you need to explain teachable way:"
    bot = EdgeGPT(cookies_path=cookies_path, prompt=prompt)
    print('prompt {}'.format(prompt))

    asking = "Explain me something about conditional sentences?"
    print('asking {}'.format(asking))
    response = await bot.add_reply(asking)
    print("reply: {}".format(response))

    asking = "Give me some examples"
    print('asking {}'.format(asking))
    response = await bot.add_reply(asking)
    print("reply: {}".format(response))


if __name__ == "__main__":
    asyncio.run(_main())
