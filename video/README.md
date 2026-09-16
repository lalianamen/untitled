# LICENA · промо-видео на испанском

Готовые файлы:

| Файл | Для чего |
|---|---|
| `licena_promo_es_vertical.mp4` | 1080×1920, Reels / TikTok / YouTube Shorts |
| `licena_promo_es_16x9.mp4` | 1920×1080, YouTube / сайт / Facebook |
| `licena_promo_es.srt` | субтитры на испанском (загрузить вместе с видео) |
| `guion_es.txt` | текст диктора (для описания под видео) |
| `licena_promo_es.html` | сама анимация; открой в браузере — проиграется без звука |

Структура ролика (продающая): хук → боль → результат → препятствие → LICENA (решение) → демо вопроса → доказательства → честная статистика → призыв.

## Как пересобрать

Нужны: Python 3, Node 22 + `playwright` (глобально), `ffmpeg` с libx264/aac, `pip install edge-tts`.

```bash
cd video/src
python3 tts.py                 # озвучка (edge-tts, голос es-US-AlonsoNeural) -> vo/*.wav
python3 mkmusic.py 64          # музыкальная подложка -> music.wav
python3 build.py --audio       # таймлайн + out/licena_promo_es.html + out/audio.wav
node render.mjs "$PWD/out/licena_promo_es.html" 1080 1920 30 <длительность> out/v.mp4
node render.mjs "$PWD/out/licena_promo_es.html" 1920 1080 30 <длительность> out/h.mp4
./mux.sh out/v.mp4 out/audio.wav ../licena_promo_es_vertical.mp4
./mux.sh out/h.mp4 out/audio.wav ../licena_promo_es_16x9.mp4
```

Длительность печатает `build.py` (поле `total`). Тексты сцен правятся в `src/promo_template.html`, текст диктора — в `src/tts.py`.
