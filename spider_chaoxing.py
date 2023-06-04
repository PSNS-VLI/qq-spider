from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import time
URL = 'http://passport2.chaoxing.com/login'+\
'?fid=&newversion=true&refer=http%3A%2F%2Fi.chaoxing.com'
ACCOUNT = '15804213643'
PASSWORD = 'yhl205666'
COURSE = '不负卿春-大学生职业生涯规划（2019级）'

browser = webdriver.Firefox()
wait = WebDriverWait(browser, 10)

#输入账号密码并登录
browser.get(URL)
_phone = wait.until(EC.presence_of_element_located((By.ID, 'phone')))
_psw = wait.until(EC.presence_of_element_located((By.ID, 'pwd')))
_login = wait.until(EC.presence_of_element_located((By.ID, 'loginBtn')))

_phone.send_keys(ACCOUNT)
_psw.send_keys(PASSWORD)
_login.click()

browser.switch_to.frame('frame_content')
css_course = f"#courseList span[title={COURSE}]"
_course = wait.until(
EC.presence_of_element_located((By.CSS_SELECTOR, css_course))
)
_course.click()
#切换选项卡
browser.switch_to.window(browser.window_handles[1])

#点击章节
css_chapter = "#boxscrollleft div.nav-content ul li[dataname='zj']"
_chapter = wait.until(
EC.presence_of_element_located((By.CSS_SELECTOR, css_chapter))
)
time.sleep(2)
_chapter.click()

#切换到章节iframe并点击
browser.switch_to.frame('frame_content-zj')
css_target = ".catalog_level .chapter_item"
_targets = wait.until(
EC.presence_of_all_elements_located((By.CSS_SELECTOR, css_target))
)

#遍历章节列表，找到任务点
for item in _targets:
    try:
        item.find_element(By.CSS_SELECTOR, '.catalog_title .catalog_task .catalog_state')
        continue
    except NoSuchElementException:
        item.click()
        browser.switch_to.parent_frame()
        break
        

#获取目录
css_catalog = "#coursetree div.posCatalog_level .posCatalog_select"
_catalogs = wait.until(
EC.presence_of_all_elements_located((By.CSS_SELECTOR, css_catalog))
)
for item in _catalogs:
    try:
        item.find_element(By.CLASS_NAME, 'icon_Completed')
        continue
    except NoSuchElementException:
        item.click()
        browser.switch_to.frame('iframe')
        #定位视频容器
        css_wrap = '.ans-attach-ct'
        try:
            _wraps = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, css_wrap))
            )
            for wrap in _wraps:
                if 'ans-job-finished' in wrap.get_attribute('class'):
                    continue
                else:
                    browser.execute_script('window.scroll(0, 3000)')
                    browser.switch_to.frame(
                    wrap.find_element(By.TAG_NAME, 'iframe')
                    )
                    try:
                        print('ok')
                        video = wait.until(
                        EC.presence_of_element_located(
                        (By.ID, 'video_html5_api')))
                        browser.execute_script('arguments[0].play()', video)
                        print(video.location)
                        time.sleep(10)
                        video_time = wait.until(
                        EC.presence_of_element_located(
                        (By.CLASS_NAME, 'vjs-duration-display'))).text
                        print(video_time)
                        video_times = video_time.split(':')
                        print(video_times)
                        time.sleep(int(video_time[0])*60+int(video_times[1]))
                        browser.switch_to.parent_frame()
                        continue
                    except TimeoutException:
                        browser.switch_to.parent_frame()
                        print('none')
                        continue
            browser.switch_to.parent_frame()
            continue
        except TimeoutException:
            browser.switch_to.parent_frame()
            continue

