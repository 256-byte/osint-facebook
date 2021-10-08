from playwright.sync_api import sync_playwright
import random

def press_mouse(element, page):
    location = page.locator(element)
    box = location.bounding_box()
    page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
    page.mouse.down()
    page.mouse.up()
    page.wait_for_timeout(2000)

def fill_bro(element, text, page):
    press_mouse(element, page)
    delay = random.randint(150, 200)
    page.keyboard.type(text, delay=delay)
    page.wait_for_timeout(2000)

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
    month = str(random.randint(1, 12))

    # Email
    email = fng.text_content(":right-of(dt:has-text('Email Address'))")
    email = email.split("@")[0].lower() + year

    # Credentials
    psw = fng.text_content(":right-of(dt:has-text('Password'))")

    value = {
        "name": name,
        "surname": surname,
        "year": year,
        "day": day,
        "month": month,
        "email": email,
        "psw": psw
    }

    # Phone number
    phone = browser.new_page()
    phone.goto("https://quackr.io/temporary-phone-number-generator")
    press_mouse(":nth-match(span:has-text('Select Country'), 2)", phone)
    phone.click("section >> text=United Kingdom")
    phone.click("text=Generate Phone Number")
    phone.wait_for_load_state()
    phone.wait_for_timeout(2000)
    number = phone.url.split("/")[-1]
    phone_number = number[2:12]


    # Yahoo!
    yh = browser.new_page()
    yh.goto("https://login.yahoo.com/")
    press_mouse("#createacc", yh) #Create account

    fill_bro("//*[@name='firstName']", value["name"], yh)
    fill_bro("//*[@name='lastName']", value["surname"], yh)

    press_mouse("//*[@name='yid']", yh)
    yh.wait_for_timeout(2000)
    press_mouse("//*[@id='desktop-suggestion-list']/li[1]", yh)
    fill_bro("#usernamereg-password", value["psw"], yh)
    yh.select_option("//*[@name='shortCountryCode']", "GB")
    fill_bro("#usernamereg-phone", phone_number, yh)

    yh.select_option("#usernamereg-month", value["month"])
    fill_bro("#usernamereg-day", value["day"], yh)
    fill_bro("#usernamereg-year", value["year"], yh)

    press_mouse("#reg-submit-button", yh)

    # Outlook
    # out = browser.new_page()
    # out.goto("https://signup.live.com/")
    #
    # email_with_outlook = value["email"] + "@outlook.com"
    # fill_bro("//*[@name='MemberName']", email_with_outlook, out)
    # press_mouse("#iSignupAction", out)
    #
    # fill_bro("//*[@name='Password']", value["psw"], out)
    # press_mouse("#iSignupAction", out)
    #
    # fill_bro("//*[@name='FirstName']", value["name"], out)
    # fill_bro("//*[@name='LastName']", value["surname"], out)
    # press_mouse("#iSignupAction", out)
    #
    # out.select_option('select#BirthDay', value["day"])
    # out.select_option('select#BirthMonth', value["month"])
    #
    # fill_bro("//*[@name='BirthYear']", value["year"], out)
    #
    # press_mouse("#iSignupAction", out)

    #Cant continue due to outlook custom captcha (diffrent from google captcha)



    yh.screenshot(path="example2.png")

    yh.pause()
    browser.close()
