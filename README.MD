# Netflix Account Checker v2.0

Selenium-based Netflix combo-list checker for Linux.

![Screenshot](assets/pic.png)

## Features

- Checks Netflix accounts via Selenium WebDriver
- Auto-resume on 403 / rate-limit errors
- Stores valid accounts in `valid.txt`
- IP & country detection on startup

## Requirements

- Python 3.7+
- Google Chrome / Chromium
- ChromeDriver (matching your Chrome version)

## Setup

```bash
pip install -r requirements.txt
```

## Usage

1. Create a file named `netflix.txt` in the project root with combos in `email:password` format (one per line)
2. Run the checker:

```bash
python3 netflix.py
```

3. Valid accounts are saved to `valid.txt`

## Resume

If the checker is interrupted (403 error, rate limit, etc.), remaining combos are saved to `resume.txt`. On next run, the checker automatically detects and resumes from that file.

## Project Structure

```
netflix.py        # Main checker logic
countries.py      # IP & geolocation lookup
header.py         # Terminal UI (title, menu)
requirements.txt  # Python dependencies
```

## License

For educational purposes only.
