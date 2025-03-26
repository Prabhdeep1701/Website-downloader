# website-download
 # Website Downloader

## Overview

The **Website Downloader** is a Python-based application that allows users to download entire web pages, including HTML, CSS, and JavaScript files, for offline viewing. The project utilizes **Selenium**, **BeautifulSoup**, and **Tkinter** to automate website downloading and provide a user-friendly interface.

## Features

- Downloads and saves HTML, CSS, and JavaScript files.
- Automatically fixes CSS properties like `font-smoothing` for compatibility.
- Uses **Selenium** to render JavaScript-heavy web pages before downloading.
- Simple GUI built with **Tkinter** for easy interaction.
- Allows users to select an output folder for saving files.

## Prerequisites

Ensure you have the following installed:

- Python 3.7+
- Google Chrome or Chrome Canary
- Required Python packages (see Installation section)

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/your-username/website-downloader.git
   cd website-downloader
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   If `requirements.txt` is missing, manually install the required libraries:

   ```bash
   pip install requests beautifulsoup4 selenium chromedriver-autoinstaller tkinter
   ```

## Usage

1. Run the script:

   ```bash
   python app.py
   ```

2. Enter the URL of the website you want to download.

3. Choose a folder to save the downloaded files.

4. Click the **Download Website** button.

## Troubleshooting

### ChromeDriver Issues

If you get a `FileNotFoundError` related to ChromeDriver, try specifying the path manually: Modify `download_website()` in `app.py`:

```python
options.binary_location = "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary"
```

### Missing CSS/JavaScript Files

Some websites block direct resource downloading. Ensure the website allows resource fetching.

## Author

**Prabhdeep Singh**


