# silero-tts-reader


#### docker-compose.yml

```yaml
services:
  silero-tts-local:
    image: ghcr.io/andriell/silero-tts-reader:latest
    container_name: silero-tts-reader
    ports:
      - 8000:8000
    volumes:
      # Папка для сохранения весов лингвистической модели ударений на вашем ПК
      - ./hf_cache:/root/.cache/huggingface
    restart: unless-stopped
```
