import time
import requests

from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.chrome.options import Options

from gpm_v2.GPMLoginAPI import GPMLoginAPI

apiUrl = 'http://127.0.0.1:19995'
api = GPMLoginAPI(apiUrl)


def create_profile(name, group, proxy):
    print('CREATE PROFILE ------------------')
    if proxy is None or len(proxy) < 5:
        createdResult = api.Create(name, group)
    else:
        createdResult = api.Create(name, group, proxy=proxy)
    createdProfileId = None
    if createdResult is not None:
        status = bool(createdResult['status'])
        if status:
            createdProfileId = str(createdResult['profile_id'])
    print(f"Created profile ID: {createdProfileId}")
    return createdProfileId


def open_profile(profile_id):
    index = 0
    while True:
        try:
            if index > 2:
                return None

            print('START PROFILE ------------------')
            startedResult = api.Start(profile_id)
            time.sleep(3)
            if startedResult is not None:
                status = bool(startedResult['status'])
                if status:
                    browserLocation = str(startedResult["browser_location"])
                    seleniumRemoteDebugAddress = str(startedResult["selenium_remote_debug_address"])
                    gpmDriverPath = str(startedResult["selenium_driver_location"])
                    print('gpmDriverPath = ', gpmDriverPath, 'seleniumRemoteDebugAddress = ',
                          seleniumRemoteDebugAddress)
                    # Init selenium
                    options = Options()
                    options.debugger_address = seleniumRemoteDebugAddress
                    options.binary_location = browserLocation
                    # prefs = {"profile.default_content_setting_values.notifications": 1,
                    #          "credentials_enable_service": False,
                    #          "profile.password_manager_enabled": False
                    #          }
                    # options.add_experimental_option("prefs", prefs)
                    options.add_argument('--disable-notifications')
                    options.add_argument("--disable-infobars")
                    # options.add_experimental_option('useAutomationExtension', False)
                    # options.add_argument("start-maximized")
                    # options.add_experimental_option("detach", True)
                    # options.add_argument("--disable-extensions")
                    # options.add_experimental_option("excludeSwitches", ['enable-automation'])

                    myService = service.Service(gpmDriverPath)
                    # driver = UndetectChromeDriver(service = myService, options=options)
                    driver = webdriver.Chrome(service=myService, options=options)
                    driver.set_page_load_timeout(30)
                    time.sleep(10)
                    return driver
        except:
            index = index + 1


def get_ip_proxy(proxy):
    print("get_ip_proxy")
    proxies = {
        "http": proxy,
        "https": proxy,
    }
    response = requests.get("https://checkip.amazonaws.com", proxies=proxies)
    ip = response.text.splitlines()[0]
    print("ip: " + str(ip))
    return ip


def get_info_profile_by_name(name_profile):
    print("get_info_profile_by_name")
    startedResult = api.GetProfiles()
    for profile in startedResult:
        if name_profile in str(profile.get("name")):
            print("profile id " + str(profile.get("id")))
            return str(profile.get("id"))
    return None


def close_profile(driver):
    print("close_profile")
    driver.close()
    driver.quit()


def delete_profile(profile_id):
    print('DELETE PROFILE ------------------')
    api.Delete(profile_id)
    print(f"Deleted: {profile_id}")
