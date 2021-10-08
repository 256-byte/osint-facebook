from playwright.sync_api import sync_playwright
import random

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    # Fake Name Generator
    fng = browser.new_page()
    fng.goto("https://www.fakenamegenerator.com/")

    # NAME
    full_name = fng.text_content("div.address > h3")
    name = full_name.split(" ")[0]
    surname = full_name.split(" ")[-1]

    # BIRTH
    birth = fng.text_content(":right-of(dt:has-text('Birthday'))")
    year = birth.split(", ")[-1]
    day = birth.split(", ")[0].split(" ")[-1]
    month = random.randint(0, 31)

    # Credentials
    psw = fng.text_content(":right-of(dt:has-text('Password'))")

    return_value = {
        "name": name,
        "surname": surname,
        "year": year,
        "day": day,
        "month": month,
        "psw": psw
    }

    fng.pause()
    # fng.screenshot(path="example2.png")
    browser.close()
