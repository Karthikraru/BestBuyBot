from selenium import webdriver
import time

from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException


def timeme(method):
    def wrapper(*args, **kw):
        startTime = int(round(time.time() * 1000))
        result = method(*args, **kw)
        endTime = int(round(time.time() * 1000))
        print('Checked out in ', (endTime - startTime) / 1000, 's')
        return result

    return wrapper

@timeme
def order(refreshDelay, cvc):
    ATC(refreshDelay)
    startTime = int(round(time.time() * 1000))
    while True:
        if driver.current_url == "https://www.bestbuy.com/cart":
            break
        try:
            driver.find_element_by_xpath('//*[@id="shop-attach-modal-33398265-modal"]/div/div[1]/div/div/div/div/div[1]/div[3]/a').click()
            break
        except NoSuchElementException:
            pass
        except ElementNotInteractableException:
            pass
        endTime = int(round(time.time() * 1000))
        if (endTime - startTime)/1000 >5:
            driver.refresh()
            ATC(refreshDelay)
            startTime = int(round(time.time() * 1000))

    while True:
        try:
            driver.find_element_by_xpath('//*[@id="cartApp"]/div[2]/div[1]/div/div/span/div/div[2]/div[1]/section[2]/div/div/div[3]/div/div[1]/button').click()
            break
        except NoSuchElementException:
            pass

    while True:
        try:
            driver.find_element_by_xpath('//*[@id="checkoutApp"]/div[2]/div[1]/div[1]/main/div[2]/div[3]/section[1]/div[2]/div/div[2]/div/div/div[2]/div[3]/div/button')
            break
        except NoSuchElementException:
            pass
        except ElementNotInteractableException:
            pass
    try:
        driver.find_element_by_xpath('//*[@id="credit-card-cvv"]').send_keys(cvv)
        time.sleep(2)
    except NoSuchElementException:
        pass
    except ElementNotInteractableException:
        pass

    while True:
        try:
            driver.find_element_by_xpath('//*[@id="checkoutApp"]/div[2]/div[1]/div[1]/main/div[2]/div[2]/div/div[4]/div[3]/div/button').click()
            break
        except NoSuchElementException:
            pass
        except ElementNotInteractableException:
            pass

def ATC(refreshDelay):
    added = False
    while True:
        if driver.current_url == "https://www.bestbuy.com/cart":
            break
        i = 0
        while i < 10:
            try:
                driver.find_element_by_xpath('/html/body/div[3]/main/div[2]/div[3]/div[2]/div/div/div[{}]/div[1]/div/div/div/button'.format(i)).click()
                added = True
                break
            except NoSuchElementException:
                i = i + 1
                pass
        if added:
            break
        time.sleep(refreshDelay)
        driver.refresh()

if __name__ == '__main__':
    driver = webdriver.Chrome('./chromedriver')
    username = input("What is the username of your Best Buy account?\n > ")
    password = input("What is the password of you Best Buy account?\n > ")
    url = input("What is the product url?\n > ")
    refreshDelay = input("What refresh delay would you like? (In seconds)\n > ")
    refreshDelay = int(refreshDelay)
    cvv = input('What is the CVV for the card on the Best Buy account?\n > ')
    driver.get('https://www.bestbuy.com/identity/signin?token=tid%3A98e09591-2479-11eb-b081-0ebd52d90641')
    driver.find_element_by_xpath('//*[@id="fld-e"]').send_keys(username)
    driver.find_element_by_xpath('//*[@id="fld-p1"]').send_keys(password)
    driver.find_element_by_xpath('/html/body/div[1]/div/section/main/div[1]/div/div/div/div/form/div[4]/button').click()
    while driver.current_url != 'https://www.bestbuy.com/':
        pass
    driver.get(url)
    order(refreshDelay, cvv)
