from playwright.sync_api import sync_playwright
import random


def run(element):
    locator = fng.locator(element)
    box = locator.bounding_box()
    fng.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
    fng.mouse.down()
    fng.mouse.up()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    # Fake Name Generator
    fng = browser.new_page()
    fng.goto("https://unixpapa.com/js/testover.html")

    run(".green")

    fng.screenshot(path="example2.png")

    fng.pause()
    browser.close()
