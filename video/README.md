# LICENA · промо-видео на испанском (California + Arizona)

Готовые файлы:

| Файл | Для чего |
|---|---|
| `licena_promo_es_short_vertical.mp4` | 1080×1920, ~51 с, короткая версия для Instagram Reels / TikTok / Shorts |
| `licena_promo_es_16x9.mp4` | 1920×1080, ~68 с, полная версия для YouTube / сайта / Facebook |
| `licena_promo_es_short.srt`, `licena_promo_es.srt` | субтитры на испанском (короткая / полная) |
| `guion_es_short.txt`, `guion_es.txt` | текст диктора (для описания под видео) |
| `licena_promo_es_short.html`, `licena_promo_es.html` | сама анимация; открой в браузере, проиграется без звука |

Структура ролика (продающая): хук → боль → результат → препятствие → LICENA (решение) → демо вопроса → доказательства → честная статистика → призыв. В короткой версии сцена «доказательства» слита со статистикой, а в сценах меньше пунктов.

## Как пересобрать

Нужны: Python 3, Node 22 + `playwright` (глобально), `ffmpeg` с libx264/aac, `pip install edge-tts`.

```bash
cd video/src
MODE=full  python3 tts.py       # озвучка (edge-tts, голос es-US-AlonsoNeural) -> vo/
MODE=short python3 tts.py       # короткая версия -> vo_short/
python3 mkmusic.py 70           # музыкальная подложка -> music.wav
python3 build.py --audio        # полная: out/licena_promo_es.html + out/audio.wav
python3 build.py --short --audio  # короткая: out/licena_promo_es_short.html + out/audio_short.wav
node render.mjs "$PWD/out/licena_promo_es_short.html" 1080 1920 30 <длительность> out/vs.mp4
node render.mjs "$PWD/out/licena_promo_es.html" 1920 1080 30 <длительность> out/h.mp4
./mux.sh out/vs.mp4 out/audio_short.wav ../licena_promo_es_short_vertical.mp4
./mux.sh out/h.mp4  out/audio.wav       ../licena_promo_es_16x9.mp4
```

Длительность печатает `build.py` (поле `total`). Любую комбинацию (например, полная вертикальная) можно собрать той же командой `render.mjs` с другим размером кадра. Тексты сцен правятся в `src/promo_template.html` (атрибуты `data-t-short` и `data-hide` управляют короткой версией), текст диктора — в `src/tts.py`.
