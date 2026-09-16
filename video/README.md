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

## Обложки и оформление канала (стиль licena.us)

Цвета и шрифты взяты с живого сайта: фон #090C27→#19123D, «heat»-градиент #FCDF00→#FFB300→#FF4E51, жёлтый #FFC100, заголовки Archivo 900 капсом, подписи IBM Plex Sans / Mono, логотип «L» в градиентном квадрате.

- `video/thumbs/`: `shorts_thumb_A_pain.jpg`, `shorts_thumb_B_benefit.jpg` (1080×1920, Shorts / Reels), `youtube_thumb_A_pain.jpg`, `youtube_thumb_B_benefit.jpg` (1280×720).
- `video/brand/`: `banner_es.jpg`, `banner_en.jpg` (2560×1440, текст внутри безопасной зоны 1546×423), `avatar_mono.png` (буква «L» на градиенте), `avatar_word.png` (логотип + LICENA), 800×800.

Исходник всех восьми картинок: `src/brand2.html` (параметр `?t=banner_es|banner_en|avatar_mono|avatar_word|shorts_A|shorts_B|yt_A|yt_B`), рендер: `node src/brand2.mjs "$PWD/src/brand2.html" <папка>`.

Внимание: сами видеоролики пока в старом стиле прототипа (navy/gold, Playfair) и с цифрами из старых страниц (500 + 500 вопросов). Сайт заявляет 13,000+ вопросов, много специальностей, пробный период и подписку, так что перед публикацией стоит пересобрать ролик под стиль и факты сайта.
