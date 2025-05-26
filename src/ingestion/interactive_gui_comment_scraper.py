import json
import time
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os

# Instagram scraping configuration
CHROMEDRIVER_PATH = "driver/chromedriver.exe"
COOKIES_PATH = "instagram_cookies_scraper.json"
OUTPUT_COMMENTS_JSON = "data/gui_extracted_comments.json"

REFERENCE_POST_URL = ""  # sarà settato dinamicamente

def load_driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("user-agent=Mozilla/5.0")
    driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=options)
    driver.get("https://www.instagram.com/")
    time.sleep(5)
    with open(COOKIES_PATH, "r") as f:
        cookies = json.load(f)
    for cookie in cookies:
        if "sameSite" in cookie:
            cookie.pop("sameSite")
        driver.add_cookie(cookie)
    driver.refresh()
    time.sleep(5)
    return driver

def extract_comments_from_current_page(driver, max_comments=50):
    global REFERENCE_POST_URL
    print(f"\n Estrazione commenti dalla struttura reale Instagram")
    time.sleep(2)

    REFERENCE_POST_URL = driver.current_url
    comments = []
    comment_blocks = driver.find_elements(By.XPATH, "//ul/div")

    for idx, block in enumerate(comment_blocks):
        try:
            username_el = block.find_element(By.XPATH, ".//a[starts-with(@href, '/')]")
            username = username_el.text.strip()

            spans = block.find_elements(By.XPATH, ".//span")
            comment_text = ""
            like_count = 0

            for span in spans:
                text = span.text.strip()

                # Detect like count
                if "mi piace" in text.lower():
                    digits = ''.join(c for c in text if c.isdigit())
                    if digits:
                        like_count = int(digits)

                # Detect valid comment text
                if (
                    text and
                    text.lower() != username.lower() and
                    all(x not in text.lower() for x in [
                        "mi piace", "piace a", "rispondi", "vedi", "g", "settim", "giorn", "risposte"
                    ])
                ):
                    comment_text = text

            if username and comment_text:
                comments.append({
                    "content_id": f"ig_comment_{idx+1}",
                    "observation_time": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "user": username,
                    "user_location": "",
                    "social_media": "Instagram",
                    "publish_date": "",
                    "geo_location": None,
                    "comment_raw_text": comment_text,
                    "emoji": [c for c in comment_text if c in '😬🏎️🥇🚀🔥'],
                    "reference_post_url": REFERENCE_POST_URL,
                    "like_count": like_count,
                    "reply_count": 0,
                    "repost_count": 0,
                    "quote_count": 0,
                    "bookmark_count": 0,
                    "content_type": "comment"
                })

            if len(comments) >= max_comments:
                break

        except Exception:
            continue

    print(f" Trovati {len(comments)} commenti validi")
    return comments


def save_comments_to_json(new_comments, filepath=OUTPUT_COMMENTS_JSON):
    try:
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                existing_comments = json.load(f)
        else:
            existing_comments = []

        combined = existing_comments + new_comments

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(combined, f, ensure_ascii=False, indent=2)

        print(f"💾 Salvati in {filepath}")
    except Exception as e:
        print(f" Errore salvataggio JSON: {e}")


def launch_gui(driver):
    def scrape():
        result_box.delete(1.0, tk.END)
        comments = extract_comments_from_current_page(driver, max_comments=50)
        if comments:
            result_texts = [f"{c['user']}: {c['comment_raw_text']}" for c in comments]
            result_box.insert(tk.END, "\n".join(result_texts))
            save_comments_to_json(comments)
            messagebox.showinfo("Salvataggio completato", f"{len(comments)} commenti salvati in {OUTPUT_COMMENTS_JSON}")
        else:
            result_box.insert(tk.END, "⚠️ Nessun commento trovato o struttura cambiata.")

    root = tk.Tk()
    root.title("Instagram Comment Scraper")
    root.geometry("600x500")

    label = tk.Label(root, text="🖱️ Vai manualmente su un post Instagram, poi clicca 'Estrai Commenti'")
    label.pack(pady=10)

    scrape_button = tk.Button(root, text="Estrai Commenti e Salva", command=scrape)
    scrape_button.pack(pady=10)

    result_box = tk.Text(root, height=20, wrap=tk.WORD)
    result_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    root.mainloop()

if __name__ == "__main__":
    driver = load_driver()
    launch_gui(driver)
    driver.quit()

