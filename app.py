import os
import requests
import tkinter as tk
from tkinter import filedialog, messagebox
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import subprocess

def create_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def download_file(url, folder, filename=None):
    """Downloads a file and saves it locally"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        if not filename:
            filename = os.path.basename(urlparse(url).path) or "file"
        filepath = os.path.join(folder, filename)
        with open(filepath, "wb") as file:
            file.write(response.content)
        return filepath
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None

def get_chrome_canary_version():
    """ Get the version of Chrome Canary """
    try:
        version = subprocess.check_output(
            ["/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary", "--version"]
        ).decode("utf-8").strip().split()[-1]
        return version
    except Exception as e:
        print("❌ Failed to get Chrome Canary version:", e)
        return None

def extract_computed_styles(driver):
    """ Extracts inline styles from computed styles for accurate page rendering """
    return driver.execute_script("""
        function getComputedStylesForAllElements() {
            let styles = "";
            document.querySelectorAll('*').forEach(element => {
                let computedStyle = window.getComputedStyle(element);
                let styleString = "";
                for (let i = 0; i < computedStyle.length; i++) {
                    let prop = computedStyle[i];
                    styleString += `${prop}: ${computedStyle.getPropertyValue(prop)}; `;
                }
                styles += `${element.tagName.toLowerCase()} { ${styleString} }\n`;
            });
            return styles;
        }
        return getComputedStylesForAllElements();
    """)

def download_website():
    url = url_entry.get()
    output_folder = folder_entry.get()

    if not url or not output_folder:
        messagebox.showerror("Error", "Please enter a URL and select a folder.")
        return

    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.binary_location = "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary"

        driver = webdriver.Chrome(service=Service(), options=options)
        driver.get(url)
        html_content = driver.page_source

        # Extract dynamically loaded CSS
        stylesheets = driver.execute_script("""
            return Array.from(document.styleSheets)
                .filter(sheet => sheet.href)
                .map(sheet => sheet.href);
        """)

        computed_css = extract_computed_styles(driver)
        driver.quit()

        soup = BeautifulSoup(html_content, "html.parser")
        create_folder(output_folder)

        # Save HTML file
        html_path = os.path.join(output_folder, "index.html")
        with open(html_path, "w", encoding="utf-8") as file:
            file.write(soup.prettify())

        status_label.config(text="✅ HTML Saved!")

        # Download CSS files (external + inline stylesheets)
        css_folder = os.path.join(output_folder, "css")
        create_folder(css_folder)

        for css_url in stylesheets:
            if css_url.startswith("http"):
                downloaded_file = download_file(css_url, css_folder, filename=os.path.basename(urlparse(css_url).path))
                if downloaded_file:
                    for link_tag in soup.find_all("link", href=True):
                        if link_tag["href"] == css_url:
                            link_tag["href"] = os.path.relpath(downloaded_file, output_folder)

        # Save computed CSS
        computed_css_path = os.path.join(css_folder, "computed_styles.css")
        with open(computed_css_path, "w", encoding="utf-8") as file:
            file.write(computed_css)

        # Inject computed CSS into HTML
        new_style_tag = soup.new_tag("link", rel="stylesheet", href=os.path.relpath(computed_css_path, output_folder))
        soup.head.append(new_style_tag)

        # Save updated HTML file with computed styles applied
        with open(html_path, "w", encoding="utf-8") as file:
            file.write(soup.prettify())

        messagebox.showinfo("Success", "🚀 Website Download Complete!")
        status_label.config(text="✅ Download Complete!")

    except Exception as e:
        messagebox.showerror("Error", f"❌ Failed to download website: {e}")
        status_label.config(text="❌ Download Failed")

# GUI Setup
root = tk.Tk()
root.title("Website Downloader")
root.geometry("500x300")

# URL Entry
tk.Label(root, text="Enter Website URL:").pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# Folder Selection
tk.Label(root, text="Select Output Folder:").pack(pady=5)
folder_entry = tk.Entry(root, width=40)
folder_entry.pack(side=tk.LEFT, padx=5)

def browse_folder():
    folder = filedialog.askdirectory()
    folder_entry.delete(0, tk.END)
    folder_entry.insert(0, folder)

browse_button = tk.Button(root, text="Browse", command=browse_folder)
browse_button.pack()

# Download Button
download_button = tk.Button(root, text="Download Website", command=download_website, bg="blue", fg="white")
download_button.pack(pady=20)

# Status Label
status_label = tk.Label(root, text="", fg="green")
status_label.pack()

# Run Tkinter Event Loop
root.mainloop()
