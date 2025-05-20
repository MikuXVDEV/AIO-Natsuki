from loguru import logger
from typing import List, Dict
from datetime import datetime

from .core import Core
from .memory import Memory
from ...config_reader import config


class Natsuki:
    def __init__(self) -> None:
        self.user_ollama_instances = {}

    async def call_llm(
            self, user_id: int,
            memory_instante,
            messages: List[Dict[str, str]]
            ) -> str:
        """Вызов Ollama API с использованием библиотеки ollama."""

        full_messages = memory_instante + messages
        
        system_prompt = "Меня зовут игрок. Я хочу, чтобы ты меня всегда называла игроком."

        message_history = [
            {"role": "user", "content": system_prompt},
            ] + full_messages

        try:
            if user_id not in self.user_ollama_instances:
                self.user_ollama_instances[user_id] = Core(model=config.model_ollama.get_secret_value(), system=system_prompt)

            ollama_instance = self.user_ollama_instances[user_id]
            response = await ollama_instance.generate_in_thread(message_history)


            formatted_ai_response = response.strip('\n')

            memory = Memory(user_id)
            mem = memory.memory
            mem.append({'role': 'user', 'content': messages[0].get('content')})
            mem.append({'role': 'assistant', 'content': formatted_ai_response})
            memory.save_memory(mem, user_id)

            return {
                    'response': formatted_ai_response,
   
                }
        except Exception as e:
            logger.error(f"Ошибка запроса к Натсуки. Юзер: {user_id}\nОшибка{e}", exc_info=True)
            return {
                    'response': f"Натсуки, почему-то ничего  не ввернула в ответ.\n{response}\n{e}",
                }
