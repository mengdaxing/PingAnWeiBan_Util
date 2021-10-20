# -*- coding: UTF-8 -*-
from time import sleep

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json

driver = webdriver.Chrome(executable_path="chromedriver")

HOST='https://weiban.mycourse.cn/#/'

# login
driver.get(HOST)
driver.implicitly_wait(5)
WebDriverWait(driver, 600, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, 'task-block')))
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
        WebDriverWait(driver, 600, 0.5).until(EC.presence_of_element_located(
            (By.CLASS_NAME, 'folder-item')
        ))
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
                    WebDriverWait(driver, 600, 0.5).until(EC.presence_of_element_located(
                        (By.CLASS_NAME, 'course')
                    ))
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

    WebDriverWait(driver, 600, 0.5).until(EC.presence_of_element_located(
        (By.CLASS_NAME, 'mint-tab-item')
    ))
    driver.find_elements_by_class_name('mint-tab-item')[1].click()

    WebDriverWait(driver, 600, 0.5).until(EC.presence_of_element_located(
        (By.CLASS_NAME, 'exam-btn-group')
    ))
    btn_group = driver.find_elements_by_class_name('exam-btn-group')[0].find_elements_by_class_name('exam-block')
    btn_group[len(btn_group)-1].click()

    WebDriverWait(driver, 600, 0.5).until(EC.presence_of_element_located(
        (By.CLASS_NAME, 'mint-msgbox-confirm')
    ))
    driver.find_elements_by_class_name('mint-msgbox-confirm')[0].click()

    while(1):
        try:
            sleep(1)
            question = driver.find_elements_by_class_name('quest-stem')[0].text
            
            theQ = None
            for q in db['questions']:
                if question.find(q['title']) > -1:
                    theQ = q
            if theQ is None:
                driver.execute_script(
                    '''for(i of document.getElementsByClassName("quest-option-item")){
                        i.innerHTML += "<span style="color:red">（题库木有这题，请人工回答）</span>"
                    }'''
                )
                WebDriverWait(driver, 600, 0.5).until_not(
                    EC.text_to_be_present_in_element(
                        driver.find_elements_by_class_name('quest-stem')[0],
                        question
                    )
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
