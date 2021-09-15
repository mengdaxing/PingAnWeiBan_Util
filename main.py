# -*- coding: UTF-8 -*-


from time import sleep
from config import *

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import UnexpectedAlertPresentException

locator = (By.CLASS_NAME, 'task-block')

driver = webdriver.Chrome(executable_path="chromedriver")

# login
driver.get(HOST)
driver.implicitly_wait(5)
WebDriverWait(driver, 600, 0.5).until(EC.presence_of_element_located(locator))
driver.implicitly_wait(5)

# in menu
driver.find_element_by_class_name('task-block').click()
driver.implicitly_wait(5)

folderNum = len(driver.find_elements_by_class_name('folder-item'))
for i in range(folderNum):
        sleep(3)
        folder = driver.find_elements_by_class_name('folder-item')[i]
        state = folder.find_elements_by_class_name('state')[0].text.split("/")
        if state[0] != state[1]:
            folder.find_elements_by_link_text("去学习>")[0].click()
            driver.implicitly_wait(3)
            courseNum = len(driver.find_elements_by_class_name('course'))
            for j in range(courseNum):
                try:
                    print('start:第',i,'组，第',j,'个课程')
                    sleep(3)
                    course = driver.find_elements_by_class_name('course')[0]
                    course.click()

                    WebDriverWait(driver, 60, 0.5).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'page-iframe')))

                    myframe = driver.find_elements_by_class_name('page-iframe')[0]
                    driver.switch_to.frame(myframe)
                    sleep(10)
                    res = driver.execute_script(
                        'finishWxCourse();'
                    )
                    sleep(3)
                    driver.switch_to.alert.accept();
                    print('finish:第',i,'组，第',j,'个课程')
                    driver.back()
                    sleep(3)

                except Exception as e:
                    print(e)
                    driver.back()
                    sleep(3)

            print('folder back!')
            driver.back()
driver.__exit__()
