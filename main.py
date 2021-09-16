# -*- coding: UTF-8 -*-


from time import sleep

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import UnexpectedAlertPresentException
import json

locator = (By.CLASS_NAME, 'task-block')

driver = webdriver.Chrome(executable_path="chromedriver")

HOST='https://weiban.mycourse.cn/#/'

# login
driver.get(HOST)
driver.implicitly_wait(5)
WebDriverWait(driver, 600, 0.5).until(EC.presence_of_element_located(locator))
driver.implicitly_wait(5)

# in menu
driver.find_element_by_class_name('task-block').click()
driver.implicitly_wait(5)

folderNum = len(driver.find_elements_by_class_name('folder-item'))
###################
# part1 答题
###################
sleep(3)
for i in range(folderNum):
        folder = driver.find_elements_by_class_name('folder-item')[i]
        state = folder.find_elements_by_class_name('state')[0].text.split("/")
        if state[0] != state[1]:
            sleep(3)
            driver.implicitly_wait(3)
            folder.find_elements_by_link_text("去学习>")[0].click()
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
            driver.back()

###################
# part2 考试
###################
with open("db.json", 'r', encoding='utf8') as f:
    db = json.load(f)

    sleep(3)
    driver.find_elements_by_class_name('mint-tab-item')[1].click()
    sleep(3)
    driver.find_elements_by_class_name('exam-block')[6].click()
    sleep(3)
    driver.find_elements_by_class_name('mint-msgbox-confirm')[0].click()

    while(1):
        try:
            sleep(1)
            question = driver.find_elements_by_class_name('quest-stem')[0].text
            
            theQ = None
            for q in db['questions']:
                if question.find(q['title']) > -1:
                    theQ = q
            if theQ == None:
                print('题库没有这题，您只能自己动手了。自动化到此结束。')
                driver.execute_script(
                    'alert("题库没有这题，您只能自己动手了。自动化到此结束。");'
                )
            
            for i in range(len(theQ['optionList'])):
                if theQ['optionList'][i]['isCorrect'] == 1:
                    driver.find_elements_by_class_name('quest-option-item')[i].click()
            
            # 下一题
            sleep(1)
            driver.find_elements_by_class_name('bottom-ctrls')[0].find_elements_by_class_name('mint-button--default')[1].click()
            
            # 判断是否可以提交
            sleep(1)
            confirm_window_style = driver.find_elements_by_class_name('confirm-sheet')[0].get_property('style')
            if (confirm_window_style.count('display') == 0):
                sleep(3)
                driver.find_elements_by_class_name('confirm-sheet')[0].find_elements_by_class_name('mint-button--danger')[0].click()
                break
        except Exception as e:
            print(e)
print('完成了')
# driver.__exit__()
