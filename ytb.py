import datetime
import threading

from common_element import *
from common_gspread import start_sheet
from gpm_v2.start_gpm_v2 import open_profile, create_profile

COL_VIDEO_STATUS = 'C'


def ytb_tool_view(name_sheet, browser):
    def get_youtube_video_IDs():
        print("Getting Youtube video IDs...")
        sleep(random.uniform(0.2, 2.5))
        index_error = 0

        while True:
            if index_error > 5:
                print("EXIT get Youtube video IDs")
                sleep(random.uniform(0.2, 2.5))
                return

            try:
                videos = WebDriverWait(browser, 10) \
                    .until(EC.presence_of_all_elements_located((By.XPATH, f'//a[@id="thumbnail" and '
                                                                          f'@class="yt-simple-endpoint inline-block '
                                                                          f'style-scope ytd-thumbnail" and contains('
                                                                          f'@href, "watch?v")]')))
                video_IDs = []
                for video in videos:
                    link = video.get_attribute('href')
                    video_IDs.append(link.split('=')[1])

                return video_IDs
            except:
                print("Get Youtube video IDs error, trying again...")
                sleep(random.uniform(2.5, 3.5))
                index_error += 1

    def get_sheet_video_IDs():
        print("Getting Sheet video IDs...")
        sleep(random.uniform(0.2, 2.5))
        index_error = 0
        sheet_video_IDs = dict()

        while True:
            try:
                index_record = 1
                for record in wks.get_all_records():
                    index_record += 1
                    status = record.get("Status")
                    if "watched" in status:
                        continue
                    # wks.update(COL_VIDEO_STATUS + str(index_record), "watching")
                    sheet_video_IDs[index_record] = record

                return sheet_video_IDs

            except Exception as ex:
                print(str(ex))
                index_error += 1
                print(f"Getting account failed, sleep {index_error * 5}s and try again")
                sleep(index_error * 5)

    # //a[@id="thumbnail" and @class="yt-simple-endpoint inline-block style-scope ytd-thumbnail" and contains(@href, "watch?v")]
    # //a[@id="thumbnail" and @class="yt-simple-endpoint inline-block style-scope ytd-thumbnail" and contains(@href, "watch?v={video_id}")]/../../../..

    def find_video(sheet_video_IDs: dict, youtube_video_IDs):
        for index_video, sheet_video in sheet_video_IDs.items():
            if sheet_video.get("ID") in youtube_video_IDs:
                return index_video, sheet_video

        return None, None

    def scroll_and_find_video(sheet_video_IDs):
        youtube_video_IDs = get_youtube_video_IDs()
        index_video_sheet, video_sheet = find_video(sheet_video_IDs, youtube_video_IDs)
        index_scroll = 0
        max_index_scroll = random.randint(3, 5)

        # Khi chưa tìm được video thì scroll xuống rồi tìm tiếp
        while video_sheet is None:
            if index_scroll >= max_index_scroll:
                if "watch?v=" in browser.current_url:
                    browser.get("https://www.youtube.com/")
                    waitWebLoading(browser, 5)
                    scroll_and_find_video(sheet_video_IDs)
                    return
            index_scroll += 1
            scroll_down(browser, 300, 400, times=3)
            youtube_video_IDs = get_youtube_video_IDs()
            index_video_sheet, video_sheet = find_video(sheet_video_IDs, youtube_video_IDs)

        scroll_random(browser, 300, 700, times=2)

        video_element = WebDriverWait(browser, 10) \
            .until(EC.element_to_be_clickable((By.XPATH, f'//a[@id="thumbnail" and '
                                                         f'@class="yt-simple-endpoint inline-block '
                                                         f'style-scope ytd-thumbnail" and contains(@href, '
                                                         f'"watch?v={video_sheet.get("ID")}")]/../../../..')))
        scroll_into_view(browser, video_element)
        sleep(random.uniform(2.5, 4.5))
        video_element.click()
        return index_video_sheet, video_sheet

    def watch_video(video_percent_watch):
        def skip_ads():
            print("skip ads...")
            if click_elment_xpath(browser, '//button[@class="ytp-ad-skip-button ytp-button"]', 2):
                click_elment_xpath(browser, '//button[@class="ytp-ad-skip-button ytp-button"]', 2)

        waitWebLoading(browser, 5)
        # thread_skip_ads = threading.Thread(target=skip_ads())
        skip_ads()
        # thread_skip_ads.start()

        # Lấy độ dài video
        video_duration = int(browser.execute_script(
            'ytplayer = document.getElementById("movie_player"); return ytplayer.getDuration();'))

        # Lấy time hiện tại của video
        video_current_time = int(browser.execute_script(
                'ytplayer = document.getElementById("movie_player"); return ytplayer.getCurrentTime();'))

        # Lấy thời gian xem
        video_time_watch = int(video_duration * video_percent_watch / 100)

        print(f"Video duration: {datetime.timedelta(seconds=video_duration)}")
        print(f"Watch video to: {datetime.timedelta(seconds=video_time_watch)}")
        print(f"Current time: {datetime.timedelta(seconds=video_current_time)}"
              f"/{datetime.timedelta(seconds=video_time_watch)}")

        while video_current_time < video_time_watch:
            skip_ads()
            # thread_skip_ads.start()
            video_current_time = int(browser.execute_script(
                'ytplayer = document.getElementById("movie_player"); return ytplayer.getCurrentTime();'))
            print(f"Current time: {datetime.timedelta(seconds=video_current_time)}"
                  f"/{datetime.timedelta(seconds=video_time_watch)}")

        print("Watch DONE! Find next video...")

    wks = start_sheet(name_sheet, "videos")
    browser.get("https://www.youtube.com/")
    waitWebLoading(browser, 5)

    _index_error = 0
    while True:
        try:
            if _index_error > 3:
                return False

            _sheet_video_IDs = get_sheet_video_IDs()
            if not bool(_sheet_video_IDs):  # Nếu danh sách sheet là rỗng => Đã xem hết
                print("All videos are watched!")
                return True

            _index_video_sheet, _video_sheet = scroll_and_find_video(_sheet_video_IDs)
            watch_video(_video_sheet.get("Time watch"))
            wks.update(COL_VIDEO_STATUS + str(_index_video_sheet), "watched")
        except Exception as ex:
            print(str(ex))
            print("error...")
            sleep(3)
            _index_error += 1


if __name__ == '__main__':
    # print(create_profile("YTB tool view", "All", None))  # 9c8732d7-7371-4089-badc-c6f204b9c6a1
    driver = open_profile("9c8732d7-7371-4089-badc-c6f204b9c6a1")
    ytb_tool_view("YTB_tool_view", driver)
