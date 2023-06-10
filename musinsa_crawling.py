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
    os.mkdir('onepiece - 3_1')
except:
    pass

def musinsaCrawling(first_review_num,product_per_review, big_category_num, product= '#ui-id-9'): 
    # first_review_num : 리뷰개수 # product_per_review : 제품당 리뷰개수
    # big_category_num : 대분류 숫자 # product : 대분류 카테고리
    try:
        driver_path = r'C:\Users\82103\Documents\ds_study\driver\chromedriver_win32\chromedriver.exe'

        driver = webdriver.Chrome(executable_path = driver_path)
        driver.get('https://www.musinsa.com/app/')
        driver.maximize_window()
        
        ActionChains(driver).click(driver.find_element(By.CSS_SELECTOR, product)).perform()
    
        ul_num = [3]
        li_num = [2]
        #ui-id-10 > ul:nth-child(3) > li:nth-child(2) > a
        #ui-id-10 > ul:nth-child(3) > li:nth-child(2) > a
        small_category_num = 0
        click_num = str(int(product.split('-')[-1]) + 1)
        product_click_num = '-'.join(product.split('-')[:-1]) + '-' + click_num
        for ul in ul_num:
            for li in li_num:
                # if (ul == 2) and (li in [3, 9]):
                #   category = driver.find_element(By.CSS_SELECTOR, f'{product_click_num} > ul:nth-child({int(ul)}) > li:nth-child({int(li)}) > a')
                # elif (ul == 3) and (li in [2, 5, 6]):
                #     category = driver.find_element(By.CSS_SELECTOR, f'{product_click_num} > ul:nth-child({int(ul)}) > li:nth-child({int(li)}) > a')  
                if ul == 2:
                    category = driver.find_element(By.CSS_SELECTOR, f'{product_click_num} > ul:nth-child({int(ul)}) > li > a')
                else:
                    category = driver.find_element(By.CSS_SELECTOR, f'{product_click_num} > ul:nth-child({int(ul)}) > li:nth-child({int(li)}) > a') 

                driver.execute_script("arguments[0].click();", category)
                # 소분류 숫자
                small_category_num += 1  
                    
                review_num = (first_review_num*2)
            
                
                # 후기순 클릭
                driver.find_element(By.CSS_SELECTOR, '#goods_list > div.boxed-list-wrapper > div.sorter-box.box > a:nth-child(6) > span').click()
                time.sleep(0.5)
                driver.find_element(By.CSS_SELECTOR, '#goods_list > div.boxed-list-wrapper > div.sorter-box.box > div > div > a:nth-child(4)').click()
                time.sleep(0.5)
                
                product_num = 1317       
                flag = True
                while flag:
                    # if ul == 3 and li == 2:
                    #     n = 20
                    #     product_num = 2668
                    # else:
                    #     n = 1
                
                    for item_n in range(1, 100):
                        # if ul == 3 and li == 5:
                        #     flag = False
                        #     break
                            
                        if int(product_num +1) >= int(review_num):
                            flag = False
                            ActionChains(driver).click(driver.find_element(By.CSS_SELECTOR, product)).perform()                 
                            time.sleep(1)
                            break

                        try:
                            time.sleep(1)
                            driver.find_element(By.CSS_SELECTOR, f'#searchList > li:nth-child({item_n}) > div.li_inner > div.article_info > p.list_info > a').click()
                                                                    #searchList > li:nth-child(1) > div.li_inner > div.article_info > p.list_info > a
                        except:
                            driver.back()
                            driver.find_element(By.CSS_SELECTOR, f'#searchList > li:nth-child({item_n}) > div.li_inner > div.article_info > p.list_info > a').click()

                        
                        req = driver.page_source
                        soup = BeautifulSoup(req,'html.parser')
                        time.sleep(0.5)
                        number_1 = int((soup.select_one('#estimate_style').text.split("(")[1].split(")")[0]).replace(',',''))
                        time.sleep(0.2)
                        number_2 = int((soup.select_one('#estimate_photo').text.split("(")[1].split(")")[0]).replace(',',''))
                        time.sleep(0.3)
                        number = min(number_1, number_2)

                        if number >= int(product_per_review):
                            page_nums = 10
                        else:
                            page_nums = (number // 10) +1
                    
                        for rank in [0, 2]:
                            for page_num in range(1, page_nums+1):
                                driver.execute_script(f"ReviewPage.goPage({page_num});")
                                time.sleep(0.5)
                                ### 상품 후기 html parser
                                req = driver.page_source
                                soup = BeautifulSoup(req,'html.parser')
                                review_list = soup.select('#reviewListFragment > div.review-list')

                                for item in review_list:
                                    product_num += 1
                                    # 이미지
                                    review_img_url = item.select_one('div.review-contents > div.review-content-photo > div > ul > li > img')['src']
                                    review_image_name = f'{big_category_num}_{small_category_num}_{product_num}_{rank}.jpg'
                                    urllib.request.urlretrieve('https:'+review_img_url, f'./onepiece - 3_1/{review_image_name}')

                                    print(f'대분류_소분류_갯수_등급: {review_image_name}',end='\r')
                                    time.sleep(0.3)
                            else:
                                try:
                                    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                                except:
                                    pass
                                time.sleep(0.1)
                                driver.find_element(By.CSS_SELECTOR,'#estimate_photo').click()   

                        else:
                            try:
                                webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                            except:
                                pass
                            driver.back()

    except Exception as e:
        print(f"오류 발생: {e}")
        
    finally:
        driver.close()


