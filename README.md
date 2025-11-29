# USTA

This repository contains utilities for collecting and visualizing USTA tournament data.

## Updating the tournament data

The tournament data is collected and summarized into `output.json` by the summary script.
To update `output.json` run the summary script from the `src/usta/tournaments` directory using Poetry:

```bash
cd src/usta/tournaments
poetry run python scripts/summarize_data.py
```

On success this will (re)write `output.json` in the same directory (`src/usta/tournaments/output.json`).

## Viewing the data in a browser

A simple static server can be used to view `tournaments.html` and the JSON data locally. Start the server from the `src/usta/tournaments` directory so the HTML can fetch `output.json` from the same folder:

```bash
cd src/usta/tournaments
poetry run python3 -m http.server 8000
# then open http://localhost:8000/tournaments.html in your browser
```

If you see stale results in the browser, confirm you're running the server from `src/usta/tournaments` and that `output.json` was updated by `summarize_data.py`. Some additional troubleshooting tips:

- Use `curl -v http://localhost:8000/output.json` to see exactly what the server is serving.
- Disable browser cache in DevTools (Network → Disable cache) or hard-reload (Cmd+Shift+R) to force a fresh fetch.
- The HTML uses a plain `fetch('output.json')`, so it expects `output.json` to be in the same directory as `tournaments.html`.

Note: For best results open the URL in Google Chrome. Safari may cache requests more aggressively while you're developing and can appear to show stale JSON.

## HTML generation script

There is also a helper script that can generate or regenerate `tournaments.html` programmatically:

- `src/usta/tournaments/scripts/generate_html.py`

The script contains logic (and a prompt used with Anthropic) to produce a map-based visualization HTML file. The repository also includes a hand-written `tournaments.html` that fetches `output.json` and renders the data on a Leaflet map.

When developing, you can either edit the included `tournaments.html` directly or regenerate it with `generate_html.py` and then serve the directory as shown above.

## Notes

- Always run the `summarize_data.py` script before serving to ensure `output.json` is up to date.
- For development, you can modify `tournaments.html` to add cache-busting for `output.json` (for example, append `?ts=${Date.now()}` or use `fetch('output.json', { cache: 'no-store' })`).
