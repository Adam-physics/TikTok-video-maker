# "One relationship": voiceover script

70 seconds. Read it calm and unhurried. Each line starts on its timestamp, which is when the matching caption appears on screen, so a recording can be laid straight over `arsenal-story.mp4`.

| Start | Line |
|---|---|
| 0:01 | Most studios start with an idea, then go looking for revenue. |
| 0:06 | Arsenal started with revenue. |
| 0:10 | Energy and finance businesses that operate today… |
| 0:16 | …and fund everything we build. |
| 0:22 | On that foundation: one shared AI stack. |
| 0:29 | And a portfolio of AI-native companies, all built on it. |
| 0:37 | One relationship becomes many revenue lines. |
| 0:50 | We don't strip companies. We build them. |
| 0:56 | A public listing turns that growth into currency for the next one. |
| 1:04 | We don't back the future. We build it. |

To add a recording (and optional music) without re-rendering:

```bash
ffmpeg -i arsenal-story.mp4 -i voiceover.wav -c:v copy -c:a aac -b:a 192k -shortest arsenal-story-vo.mp4
```

Because Arsenal is a public company, have counsel review the narration before it's used with investors.
