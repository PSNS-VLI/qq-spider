from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

class Action:
    
    SERVER = 'http://localhost:4723/wd/hub'
    PLATFORM = 'android'
    DEVICE = 'Redmi_6_Pro'
    
    def __init__(self, keyword):
        self.keyword = keyword
        self.desired_caps = {
            'platformName': Action.PLATFORM,
            'deviceName': Action.DEVICE,
            'appPackage': 'com.jingdong.app.mall',
            'appActivity': 'main.MainActivity'
        }
        self.driver = webdriver.Remote(Action.SERVER, self.desired_caps)
        self.wait = WebDriverWait(self.driver, 300)
        
    def comments(self):
        #点击同意协议
        agree = self.wait.until(EC.presence_of_element_located((By.ID, 'com.jingdong.app.mall:id/bqd')))
        agree.click()
        #点击搜索框
        x_path = "/hierarchy/android.widget.FrameLayout/"+\
        "android.widget.LinearLayout/android.widget.FrameLayout/"+\
        "android.widget.RelativeLayout/android.widget.LinearLayout/"+\
        "android.widget.RelativeLayout/android.widget.FrameLayout/"+\
        "android.widget.RelativeLayout/"+\
        "android.widget.RelativeLayout[2]/android.widget.ViewFlipper/"+\
        "android.widget.LinearLayout"
        
        search = self.wait.until(EC.presence_of_element_located((By.XPATH, x_path)))
        search.click()
        #发送搜索关键字
        search_kw = self.wait.until(EC.presence_of_element_located((By.ID, 'com.jd.lib.search.feature:id/a55')))
        search_kw.set_text(self.keyword)
        button = self.wait.until(EC.presence_of_element_located((By.ID, 'com.jingdong.app.mall:id/a9b')))
        button.click()
        #点击第一个商品
        view = self.wait.until(EC.presence_of_element_located((By.ID, 'com.jd.lib.search.feature:id/yf')))
        view.click()
        #点击评论详情
        comment = self.wait.until(EC.presence_of_element_located((By.ID, 'com.jd.lib.productdetail.feature:id/alh')))
        comment.click()
        
    def scroll(self):
        while True:
            self.driver.swipe(300, 300+700, 300, 300)
            sleep(1)
            
    def main(self):
        self.comments()
        self.scroll()
        
if __name__ == '__main__':
    action = Action("ipad")
    action.main()
        
