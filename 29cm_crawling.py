from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
import urllib
import pandas as pd
import os
import time
import re
import warnings
warnings.filterwarnings(action='ignore')

try: 
    os.mkdir('29cm_shoes')
except:
    pass

def crawling29cm(big_category_num):
    # big_category_num : 대분류 (1 : 아우터 , 4 :스커트)
    try:
        driver_path = r'C:\Users\82103\Documents\ds_study\driver\chromedriver_win32\chromedriver.exe'

        driver = webdriver.Chrome(executable_path = driver_path)
        driver.get('https://www.29cm.co.kr/home/')
        driver.maximize_window()

        ActionChains(driver).click(driver.find_element(By.CSS_SELECTOR, 'body > home-root > div > ruler-gnb > div > div.ng-tns-c43-0.nav_snb > div > ul > li.ng-tns-c43-0.WOMEN.ng-star-inserted > div.group.ng-tns-c43-0')).perform()
        
        # 대분류
        if big_category_num == 1:
            # 샌들
            driver.find_element(By.CSS_SELECTOR, 'body > home-root > div > ruler-gnb > div > div.ng-tns-c43-0.nav_snb > div > ul > li.ng-tns-c43-0.WOMEN.ng-star-inserted > div.snb_container.ng-tns-c43-0 > div > div.list_wrap.ng-tns-c43-0 > div:nth-child(1) > div > ul > li:nth-child(9) > a').click()          
            li_num = [21]
            porducts_count = [5128]
        elif big_category_num == 4:
            # 스커트
            driver.find_element(By.CSS_SELECTOR, 'body > home-root > div > ruler-gnb > div > div.ng-tns-c43-0.nav_snb > div > ul > li.ng-tns-c43-0.WOMEN.ng-star-inserted > div.snb_container.ng-tns-c43-0 > div > div.list_wrap.ng-tns-c43-0 > div:nth-child(1) > div > ul > li:nth-child(10) > a').click()
            li_num = [3, 2]
            porducts_count = [5417,4027]
        elif big_category_num == 5:
            # 스니커즈
            driver.find_element(By.CSS_SELECTOR, 'body > home-root > div > ruler-gnb > div > div.ng-tns-c43-0.nav_snb > div > ul > li.ng-tns-c43-0.WOMEN.ng-star-inserted > div.snb_container.ng-tns-c43-0 > div > div.list_wrap.ng-tns-c43-0 > div:nth-child(3) > div > ul > li:nth-child(9) > a').click()
            li_num = [1]
            porducts_count = [5100]
        elif big_category_num == 6:
            # 슬리퍼
            driver.find_element(By.CSS_SELECTOR, 'body > home-root > div > ruler-gnb > div > div.ng-tns-c43-0.nav_snb > div > ul > li.ng-tns-c43-0.WOMEN.ng-star-inserted > div.snb_container.ng-tns-c43-0 > div > div.list_wrap.ng-tns-c43-0 > div:nth-child(3) > div > ul > li:nth-child(8) > a').click()
            li_num = [3]
            porducts_count = [5552]
        else:
            print('Wrong Input')
            driver.close()

        time.sleep(0.3)
        # 소분류 선택
        for li_category, product_counts in zip(li_num, porducts_count):

            if li_category == 17:
                small_category_num = 0
            elif (li_category == 15) or (li_category == 21):
                small_category_num = 1
            elif li_category == 10:
                small_category_num = 2
            elif li_category == 19:
                small_category_num = 3
            elif li_category == 3:
                small_category_num = 1
            elif li_category == 1:
                small_category_num = 0

            try:
                driver.find_element(By.CSS_SELECTOR, f'body > shop-root > div > section > ui-list-category > div > div > div.category_tab.ng-star-inserted > ruler-small-tab > div > ul > li:nth-child({li_category}) > a').click()
            except:
                driver.find_element(By.TAG_NAME,'body').send_keys(Keys.HOME)
                driver.find_element(By.CSS_SELECTOR, f'body > shop-root > div > section > ui-list-category > div > div > div.category_tab.ng-star-inserted > ruler-small-tab > div > ul > li:nth-child({li_category}) > a').click()

            time.sleep(0.3)
            # 리뷰많은순(박스)
            driver.find_element(By.CSS_SELECTOR, 'body > shop-root > div > section > ui-list-category > div > ui-category-option > div > div > div.filter_bar > div.filter_dropdown > ruler-dropdown > div > div.resultbx').click()
            # 리뷰많은순(값)
            driver.find_element(By.CSS_SELECTOR, 'body > shop-root > div > section > ui-list-category > div > ui-category-option > div > div > div.filter_bar > div.filter_dropdown > ruler-dropdown > div > div.sel_lst > div > div > ul > li:nth-child(3) > a').click()

            time.sleep(1)
            # if li_category == 1:
            #     n = 4
            # elif li_category == 3:
            #     n = 7
            # else: 
            #     n = 1

           
            product_count = product_counts

            while True:
                # if product_count >= 6500:
                #     driver.find_element(By.TAG_NAME,'body').send_keys(Keys.HOME)
                #     break
                # else:    
                    # if li_category == 10:
                    #     n_click = 0
                    # else:
                    #     n_click = 10000
                    
                    for li_product in range(4, 51):
                        if product_count >= 6182:
                            driver.find_element(By.TAG_NAME,'body').send_keys(Keys.HOME)
                            break

                        time.sleep(5)
                        # 상품선택
                        time.sleep(0.3)
                        driver.find_element(By.CSS_SELECTOR, f'body > shop-root > div > section > ui-list-category > div > div > div.product_content.ng-star-inserted > ul > li:nth-child({li_product}) > ruler-product-list-large-item > div > a.prd_b_area > div.info > div.name').click()

                        # 아래로 이동
                        time.sleep(1)
                        some_tag = driver.find_element(By.CSS_SELECTOR, '#__next > div.css-1hv8s2.evt9g3e2 > section.eeja3je7.css-f18qjw.epg39k0 > div.css-3sj7fp.epg39k2 > div.css-190b6wm.epg39k4 > h2')
                        action = ActionChains(driver)
                        action.move_to_element(some_tag).perform()
                        time.sleep(1)
                        page_count = 0
                        page_num = 0
                        while True:
                            if page_count >= 150:
                                break

                            page_num += 1
                            time.sleep(5)
                            req = driver.page_source
                            soup = BeautifulSoup(req,'html.parser')
                            time.sleep(1)
                            button_count = int(len(soup.select('#__next > div.css-1hv8s2.evt9g3e2 > section.eeja3je6.css-1w043rb.e16llo9z0 > div.css-0.e1fqypsc0 > div > button')))
                            # print(button_count)
                            # if (li_category == 10) & (n_click == 0):
                            #     for i in range(1, 4):
                            #         n_click += 1
                            #         if n_click == 1:
                            #             driver.find_element(By.CSS_SELECTOR,'#__next > div.css-1hv8s2.evt9g3e2 > section.eeja3je6.css-1w043rb.e16llo9z0 > div.css-0.e1fqypsc0 > div > button').click()
                            #             time.sleep(1)
                            #         else:
                            #             driver.find_element(By.CSS_SELECTOR,'#__next > div.css-1hv8s2.evt9g3e2 > section.eeja3je6.css-1w043rb.e16llo9z0 > div.css-0.e1fqypsc0 > div > button:nth-child(3) > svg').click()
                            #             time.sleep(1)
                            #             page_num = n_click
                            #     else:
                            #         time.sleep(3)
                            #         req = driver.page_source
                            #         soup = BeautifulSoup(req,'html.parser')
                            #         time.sleep(1)
                            #         button_count = int(len(soup.select('#__next > div.css-1hv8s2.evt9g3e2 > section.eeja3je6.css-1w043rb.e16llo9z0 > div.css-0.e1fqypsc0 > div > button')))
                            
                            if (button_count == 1) and (page_num != 1):
                                break
                            else:
                                review_list = soup.select('#__next > div.css-1hv8s2.evt9g3e2 > section.eeja3je6.css-1w043rb.e16llo9z0 > div.css-0.e1fqypsc0 > ul > li')
                                pattern = r'img'
                                for review in review_list:
                                    true_false = review.select_one(pattern)
                                    
                                    if true_false:
                                        review_img_url = true_false['src']
                                        review_img_url = review_img_url.split('?')[0]
                                        time.sleep(0.5)
                                        product_count += 1
                                        page_count +=1 
                                        review_image_name = f'{big_category_num}_{small_category_num}_{product_count}_32.jpg'
                                        urllib.request.urlretrieve(review_img_url, f'./29cm/{review_image_name}')

                                        print(f'대분류_소분류_갯수_등급 : {li_product} >> {review_image_name} << {page_num}',end='\r')
                                    else:
                                        continue
                                
                                if button_count == 0:
                                    break
                                elif button_count == 1:
                                    driver.find_element(By.CSS_SELECTOR,'#__next > div.css-1hv8s2.evt9g3e2 > section.eeja3je6.css-1w043rb.e16llo9z0 > div.css-0.e1fqypsc0 > div > button').click()
                                    
                                elif button_count == 2:
                                    driver.find_element(By.CSS_SELECTOR,'#__next > div.css-1hv8s2.evt9g3e2 > section.eeja3je6.css-1w043rb.e16llo9z0 > div.css-0.e1fqypsc0 > div > button:nth-child(3) > svg').click()
                                    
                
                        driver.back()
                        time.sleep(1)
                    else:
                        driver.find_element(By.TAG_NAME,'body').send_keys(Keys.HOME)
                        time.sleep(0.5)
                        break
                          

    except Exception as e:
        print(f"오류 발생: {e}")
        
    finally:
        driver.close()