
from ..core.memory import Memory


async def memory_chars(memory: Memory) -> int:
    user_chars = 0
    mita_chars = 0
    for item in memory:
        if item['role'] == 'user':
            user_chars += len(item['content'])
        elif item['role'] ==  'assistant':
            mita_chars += len(item['content'])
    return user_chars, mita_chars