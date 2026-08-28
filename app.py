import os
import torch
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles  # <-- Добавили
from pydantic import BaseModel

app = FastAPI(title="Local Silero TTS API")

device = torch.device('cpu')
torch.set_num_threads(4)

# Настройка доверия к репозиторию для старых версий Torch (отключает запрос y/N)
# torch.hub.set_dir('/app/.cache/torch')
# Добавляем репозиторий Silero в список доверенных по умолчанию
# import sys
# torch.hub._validate_not_a_forked_repo = lambda *args, **kwargs: True

# Загрузка локальной v4_ru модели
# Если интернета нет, torch автоматически возьмет файлы из папки кэша
try:
    model, _ = torch.hub.load(repo_or_dir='snakers4/silero-models',
                              model='silero_tts',
                              language='ru',
                              speaker='v4_ru',
                              trust_repo=True)
    model.to(device)
except Exception as e:
    print(f"Ошибка загрузки! Если вы офлайн, убедитесь, что файлы лежат в .cache/torch: {e}")

class TTSRequest(BaseModel):
    text: str
    speaker: str = "kseniya" # Доступные: aidar, baya, kseniya, xenia, eugene
    rate: float = 1.0

@app.post("/tts")
async def text_to_speech(req: TTSRequest):
    try:
        output_path = "output.wav"
        # Генерация аудио
        model.save_wav(text=req.text,
                       speaker=req.speaker,
                       sample_rate=48000,
                       put_accent=True,
                       put_yo=True,
                       audio_path=output_path)
        return FileResponse(output_path, media_type="audio/wav")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# отдаем HTML-страницу по главному адресу
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
