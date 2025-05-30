import asyncio
from loguru import logger
from typing import List, Dict
from ollama import AsyncClient

from ...config_reader import config


class Core:
    def __init__(
            self,
            model: str,
            system: str = None) -> None:
        self.model = model
        self.system = system
        self.client = AsyncClient(host=config.ollama_api.get_secret_value())

    async def generateWithMemory(self, messages: List[Dict[str, str]]) -> str:
        print(messages)
        '''
        Sends the message history to Ollama.

        Parameters
        ----------
        messages : List[Dict[str, str]]
            The message history (list of dictionaries with role and content).

        Returns
        -------
        str
            The assistant's response.
        '''
        try:
            response = await self.client.chat(
                model=self.model,
                messages=messages,
                options={
                    "num_predict": 150
                    },
                stream=False            )

            # response = await self.client.chat.completions.create(
            #     model=self.model,
            #     messages=messages,
            #     stream=False
            # )

            # assistant_reply = response.choices[0].message.content

            assistant_reply = response['message']['content']


            return assistant_reply


        except Exception as e:
            logger.error(f"Error during Ollama call: {e}")
            return e

    async def generate_in_thread(self, messages: List[Dict[str, str]]) -> str:
        """
        Runs generateWithMemory in a separate thread and awaits the result.

        This is necessary because ollama's AsyncClient might still have some
        blocking operations, and running it directly in the main asyncio loop
        could block the bot.  Using a thread avoids this.

        Args:
            messages: The message history.

        Returns:
            The assistant's response.
        """

        loop = asyncio.get_event_loop()

        # Use run_in_executor to run the synchronous function in a thread pool
        # This ensures that the blocking I/O doesn't block the asyncio event loop.
        return await loop.run_in_executor(
            None,
            lambda: asyncio.run(self.generateWithMemory(messages))
        )
