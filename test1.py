from pedalboard import Pedalboard, Reverb
import soundfile as sf
import io

def apply_reverb(audio_bytes: bytes) -> bytes:
    audio, sr = sf.read(io.BytesIO(audio_bytes))  # читаем из байтового потока

    board = Pedalboard([
    Reverb(
        room_size=0.1,    # очень маленькое помещение
        damping=0.1,        # сильно глушится
        wet_level=0.05,     # почти нет "мокрого" сигнала
        dry_level=1.0,      # оригинальный сигнал на 100%
    )
])
   # создаём эффект реверберации
    effected = board(audio, sample_rate=sr)       # применяем эффект

    buffer = io.BytesIO()
    sf.write(buffer, effected, sr, format='WAV')  # записываем обратно в байты
    return buffer.getvalue()

# --- Пример использования ---

# 1. Загружаем аудиофайл как байты
with open("/home/miku/AIO-MITA/1.ogg", "rb") as f:
    input_bytes = f.read()

# 2. Применяем реверберацию
output_bytes = apply_reverb(input_bytes)

# 3. Сохраняем результат
with open("/home/miku/output_reverb.ogg", "wb") as f:
    f.write(output_bytes)

print("✅ Готово: output_reverb.wav")
