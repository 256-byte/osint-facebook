from playwright.sync_api import sync_playwright
import random

# path_to_extension = "./buster-master"
# user_data_dir = "/tmp/test-user-data-dir"


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=100)

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
    month = str(random.randint(0, 12))

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

    # facebook
    fc = browser.new_page()
    fc.goto("https://www.facebook.com/")
    # fc.click("[name='sign_up']") #Create new account
    fc.click("[data-testid='open-registration-form-button']")
    fc.wait_for_timeout(2000)

    fc.fill("[name='firstname']", "Ali")
    fc.fill("[name='lastname']", "Bitiren")

    fc.fill("[name='reg_email__']", "fbounjoumsouh14@wpadye.com")
    fc.fill("[name='reg_passwd__']", return_value["psw"])
    fc.select_option('select#day', return_value["day"])
    fc.select_option('select#month', return_value["month"])
    fc.select_option('select#year', return_value["year"])
    fc.check("//*[@value='1'][@name='sex']")
    fc.fill("[name='reg_email_confirmation__']", "fbounjoumsouh14@wpadye.com")

    fc.click("[name='websubmit']")
    fc.click("text='Devam'")
    # run(p)  # captcha solver extention
    fc.pause()
    fc.screenshot(path="example.png")
    browser.close()
