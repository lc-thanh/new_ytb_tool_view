import gspread
from time import sleep
import random
from CONSTANT_gspread import *
from gpm_v2.start_gpm_v2 import get_ip_proxy


def start_sheet(name_sheet, name_tab):
    sa = gspread.service_account(filename="./data/ivory-granite-384307-5a39b263c3ba.json")
    sh = sa.open(name_sheet)
    wks = sh.worksheet(name_tab)
    return wks


def get_account(wks):
    print("get accounts")
    sleep(random.uniform(0.2, 2.5))
    index_error = 0

    while True:
        try:
            index_record = 1
            for record in wks.get_all_records():
                index_record = index_record + 1
                status = record.get("Status")
                if "GOOD" in status \
                        or "FAIL" in status \
                        or "LOADING" in status:
                    continue
                wks.update(COL_STATUS + str(index_record), "LOADING")
                return str(index_record), record
            return None, None

        except Exception as ex:
            print(str(ex))
            index_error = index_error + 1
            print(f"Getting account failed, sleep {index_error * 5}s and try again")
            sleep(index_error * 5)


def get_account_by_index(wks, index):
    print("get accounts")
    sleep(random.uniform(0.2, 2.5))
    index_error = 0

    while True:
        try:
            index_record = 1
            for record in wks.get_all_records():
                index_record = index_record + 1
                if index_record == index:
                    status = record.get("Status")
                    if "GOOD" in status \
                            or "FAIL" in status \
                            or "LOADING" in status:
                        continue
                    wks.update(COL_STATUS + str(index_record), "LOADING")
                    return str(index_record), record
            return None, None

        except Exception as ex:
            print(str(ex))
            index_error = index_error + 1
            print(f"Getting account failed, sleep {index_error * 5}s and try again")
            sleep(index_error * 5)


def get_proxy_first(name_sheet):
    print("get_proxy_first")
    while True:
        try:
            name_tab = "proxy"
            sleep(random.uniform(0.2, 2.5))
            sa = gspread.service_account(filename="./data/ivory-granite-384307-5a39b263c3ba.json")
            sh = sa.open(name_sheet)
            wks = sh.worksheet(name_tab)
            index_record = 1
            for sock_item in wks.get_all_records():
                index_record = index_record + 1
                status = sock_item.get("Status")
                proxy = sock_item.get("ip xoay")
                if "LOADING" in status:
                    continue

                try:
                    print("proxy: " + str(proxy))
                    new_ip_proxy = get_ip_proxy(proxy)
                    if new_ip_proxy == "" or new_ip_proxy is None:
                        wks.update(COL_PROXY_STATUS + str(index_record), "FAIL")
                        sleep(2)
                        continue
                    if new_ip_proxy == sock_item.get("IP"):
                        wks.update(COL_PROXY_STATUS + str(index_record), "UNCHANGED")
                        sleep(2)
                        continue
                    wks.update(COL_IP + str(index_record), str(new_ip_proxy))
                except:
                    wks.update(COL_PROXY_STATUS + str(index_record), "FAIL")
                    continue

                wks.update(COL_PROXY_STATUS + str(index_record), "LOADING")
                return str(index_record), proxy

            return None, None
        except:
            print("get proxy error, trying again..")
            sleep(random.uniform(3, 5))
            pass


def refresh_proxy_status(name_sheet):
    print("refreshing proxy status...")
    wks = start_sheet(name_sheet, "proxy")
    index_error = 0
    while True:
        if index_error > 10:
            return False
        try:
            index_record = 1
            for record in wks.get_all_records():
                index_record = index_record + 1
                status = record.get("Status")
                if "LOADING" in status:
                    wks.update(COL_PROXY_STATUS + str(index_record), "")
                    sleep(random.uniform(0.2, 0.5))
            return True
        except Exception as ex:
            print(str(ex))
            index_error = index_error + 1
            print(f"refresh proxy status error, try again in {index_error * 0.1}s")
            sleep(index_error * 0.1)
