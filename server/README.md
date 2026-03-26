# Pof Web Server

Web server to obfuscate Python scripts using pof.

Simple server written in Python with flask, and using HTMX for user interaction
with Pygment for Python syntax highlight.

Two endpoints are presented, one simple HTTP API to send raw Python sources and
receive raw outputs, and one to get HTML formatted output for use with a webpage
to show the highlighted code.

## Usage

Build:

```bash
docker build . -t pofserver
```

Run:

```bash
docker run --rm -p 5000:5000 pofserver
```

Test:

```bash
echo 'print("Hello, world!")' | curl -X POST -d @- 0.0.0.0:5000
```

Or visit [localhost:5000](http://localhost:5000).

## Dev

Generate Tailwind CSS file:

```bash
npm install
npx @tailwindcss/cli -i ./input.css -o ./app/static/tailwind.css --watch --minify
```

Generate `static/pygment.css` file:

```python
from pygments.formatters import HtmlFormatter
with open("static/pygment.css", "w") as f:
    f.write(HtmlFormatter(style="monokai").get_style_defs(".highlight"))
```

## TODO

- Download output to file.
- Add timeout in case the computation takes too long.
- Set correct version when building the server in CI.
