from time import sleep
import random

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


def input_value_by_xpath(browser, xpath, value):
    index_time = 0
    while True:
        print("input into xpath: " + str(xpath))
        index_time = index_time + 1
        if index_time > 5:
            return False
        try:
            # input_el = browser.find_element(By.XPATH, xpath)
            input_el = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            input_el.click()
            sleep(0.5)
            input_el.clear()
            sleep(0.5)
            input_el.send_keys(Keys.CONTROL + Keys.BACKSPACE)
            sleep(0.5)
            input_el.send_keys(value)
            sleep(2)
            return True
        except:
            print(f"input_value_by_xpath error 3s, XPATH: {xpath}")
            sleep(3)


def input_value_by_id(browser, id, value, is_enter=False):
    print("input to element: " + str(id))
    index_time = 1
    while True:
        index_time = index_time + 1
        if index_time > 3:
            return False
        try:
            # input_el = browser.find_element(By.ID, id)
            input_el = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.ID, id)))
            input_el.click()
            sleep(0.5)
            input_el.clear()
            sleep(0.5)
            input_el.send_keys(value)
            sleep(1)
            if is_enter:
                input_el.send_keys(Keys.ENTER)
                sleep(2)
            return True
        except:
            print("not input sleep 3s")
            sleep(3)


# def input_value_by_xpath(browser, xpath, value):
#     index_time = 0
#     while True:
#         index_time = index_time + 1
#         if index_time > 10:
#             return False
#         try:
#             # input_el = browser.find_element(By.XPATH, xpath)
#             input_el = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
#             input_el.click()
#             sleep(0.5)
#             input_el.clear()
#             sleep(2)
#             input_el.send_keys(value)
#             sleep(1)
#             return True
#         except:
#             print("input_value_by_xpath  3s")
#             sleep(3)


def get_value_element(browser, element_xpath):
    index_error = 0
    while True:
        if index_error > 3:
            return False
        try:
            # data = browser.find_element(By.XPATH, element_xpath)
            data = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, element_xpath)))
            if len(data.text) > 1:
                return str(data.text)
            else:
                index_error = index_error + 1
                print("not get_value_element sleep 3s")
                sleep(3)
        except:
            index_error = index_error + 1
            print("not get_value_element sleep 3s")
            sleep(3)


def click_elment_id(browser, id_element):
    print("click element id: " + str(id_element))
    index_error = 0
    while True:
        if index_error > 3:
            return False
        try:
            # bt_add = browser.find_element(By.ID, id_element)
            bt_add = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.ID, id_element)))
            bt_add.click()
            sleep(0.5)
            return True
        except:
            index_error = index_error + 1
            print("not click sleep 3s, id: " + str(id_element))
            sleep(3)


def click_elment_xpath(browser, element_xpath, index_max=3):
    print("click_elment_xpath: " + str(element_xpath))
    index_error = 0
    while True:
        if index_error >= index_max:
            return False
        try:
            # bt_add = browser.find_element(By.XPATH, element_xpath)
            bt_add = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, element_xpath)))
            bt_add.click()
            sleep(2)
            return True
        except:
            index_error = index_error + 1
            print("not click sleep 3s " + str(element_xpath))
            sleep(3)


def hover_on_xpath(browser, xpath):
    error = 0
    while True:
        if error > 3:
            return False
        try:
            AC = ActionChains(browser)
            elem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
            AC.move_to_element(elem).perform()
            sleep(2)
            return True
        except:
            print("hover error")
            sleep(2)
            error += 1


def has_element_xpath(driver, xpath, check_times=2):
    error = 0
    while True:
        if error >= check_times:
            return False
        try:
            sleep(3)
            elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
            return len(elements) > 0
        except:
            error += 1
            print(f"no element with xpath: {xpath}")
            sleep(1)


def has_element(driver, selector):
    # elements = driver.find_elements(By.CSS_SELECTOR, selector)
    error = 0
    while True:
        if error > 1:
            return False
        try:
            elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))
            return len(elements) > 0
        except:
            error += 1
            print(f"no element with selector: {selector}")
            sleep(1)


def click_elment_xpath_slow(browser, element_xpath):
    print("click_elment_xpath_slow")
    index_error = 0
    while True:
        if index_error > 5:
            return False
        try:
            # bt_add = browser.find_element(By.XPATH, element_xpath)
            bt_add = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, element_xpath)))
            print("bt_add " + str(bt_add.text))
            bt_add.click()
            sleep(2)
            return True
        except Exception as ex:
            index_error = index_error + 1
            print("not click sleep 5s " + str(ex))
            sleep(5)


def waitWebLoading(driver, sleep_time=3):
    # Chờ trang web tải xong
    try:
        sleep(3)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    except:
        pass
    sleep(sleep_time)


def scroll_up(driver, pixels_min=500, pixels_max=1000, times=1):
    for _ in range(times):
        pixels = random.randint(pixels_min, pixels_max)
        driver.execute_script("window.scrollBy({top: -" + str(pixels) + ", behavior: 'smooth',});")
        sleep(2)


def scroll_down(driver, pixels_min=500, pixels_max=1000, times=1):
    for _ in range(times):
        pixels = random.randint(pixels_min, pixels_max)
        driver.execute_script("window.scrollBy({top: " + str(pixels) + ", behavior: 'smooth',});")
        sleep(2)


def scroll_random(driver, pixels_min=500, pixels_max=1000, times=1):
    # print(f"scroll random {times} times")
    # # Lấy chiều cao của trang web
    # page_height = driver.execute_script("return document.body.scrollHeight")
    #
    # # Scroll ngẫu nhiên đến một vị trí trên trang
    # scroll_height = random.randint(0, page_height)
    # scroll_script = f"window.scrollTo(0, {scroll_height});"
    # driver.execute_script(scroll_script)
    #
    # # Chờ trang web tải xong
    # wait = WebDriverWait(driver, 10)
    # wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    for _ in range(times):
        is_scroll_down = random.choice([True, False])
        if is_scroll_down:
            scroll_down(driver, pixels_min, pixels_max)
        else:
            scroll_up(driver, pixels_min, pixels_max)

    # Thực hiện hiệu ứng trượt mượt
    # actions = ActionChains(driver)
    # actions.move_by_offset(0, 100)  # Di chuyển chuột lên
    # actions.move_by_offset(0, -100)  # Di chuyển chuột xuống
    # actions.perform()


def scroll_into_view(driver, element):
    print("scroll into element: " + str(element))
    try:
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
    except:
        pass


def input_type_char(browser, xpath, values, is_enter=False):
    print("input_type_char")
    index_error = 0
    while True:
        if index_error > 2:
            return False
        try:
            el_input = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
            el_input.click()
            sleep(random.uniform(0.5, 1))
            el_input.clear()
            sleep(random.uniform(0.5, 1))
            is_delete = 0
            for value in values:
                if random.choice([False, True]) and random.choice([False, True]):
                    is_delete = is_delete + 1
                    if is_delete < 3:
                        el_input.send_keys(
                            random.choice(['a', 'b', 'c', 'd', 'f', 'e', 'r', 't', 'm', 'n', 's', 'v', 'l']))
                        sleep(random.uniform(0.1, 0.3))
                        el_input.send_keys(Keys.BACKSPACE)
                        sleep(random.uniform(0.1, 0.3))
                el_input.send_keys(value)
                sleep(random.uniform(0.1, 0.3))
            if is_delete == 0:
                el_input.send_keys(random.choice(['a', 'b', 'c', 'd', 'f', 'e', 'r', 't', 'm', 'n', 's', 'v', 'l']))
                sleep(random.uniform(0.1, 0.3))
                el_input.send_keys(Keys.BACKSPACE)
                sleep(random.uniform(0.1, 0.3))
            if is_enter:
                el_input.send_keys(Keys.ENTER)
                sleep(random.uniform(0.5, 2))
            return True
        except Exception as ex:
            index_error = index_error + 1
            print("not input_type_char sleep 10s " + str(ex))
            sleep(10)
