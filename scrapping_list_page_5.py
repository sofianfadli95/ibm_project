# -*- coding: utf-8 -*-
"""
Created on Tue May  1 14:40:17 2018

@author: sofyan.fadli

Ini adalah program untuk scrapping berita dari website mamikos.com
Kita dapat memasukkan search query sesuai dengan topik yg kita inginkan

"""

# Multiple condition
# //category[@name='Sport' and ./author/text()='James Small']

from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re
import csv

url = "https://mamikos.com/kost/kost-jakarta-murah"

def scrap_lists_mamikos(url):
                        
    try:
        # Mengirim request ke link yg kita tuju
        driver = webdriver.Chrome("D:\\Coursera\\IBM_Data_Science_Professional\\Final_Project\\chromedriver.exe")
        driver.get(url)
        time.sleep(4)
        # Klik Button "Saya Mengerti"
        driver.find_elements_by_xpath("//button[@id='popperConfirmation']")[0].click()
        time.sleep(5)
        # Click 'Login' Menu on top
        driver.find_element_by_xpath('//li[@class="user-nav user-login hidden-xs"]/a[text()="Masuk"]').click()
        time.sleep(2)
        # Click Button 'Pencari Kos'
        driver.find_element_by_xpath('//button[@class="btn btn-success btn-login-selector login-user-home"]').click()
        time.sleep(5)
        # Click Button 'Facebook'
        driver.find_element_by_xpath('//form[@class="form-login-facebook"]').submit()
        time.sleep(5)
        # Place the username and password, and login
        driver.find_element_by_xpath('//input[@id="email"]').send_keys("YourUsername")
        driver.find_element_by_xpath('//input[@id="pass"]').send_keys("YourPassword")
        driver.find_element_by_xpath('//button[@id="loginbutton"]').click()
        time.sleep(5)
        # Set the max price to the value that we want
        driver.find_element_by_xpath('//input[@id="filterPriceMax"]').click()
        driver.find_element_by_xpath('//input[@id="filterPriceMax"]').clear()
        driver.find_element_by_xpath('//input[@id="filterPriceMax"]').send_keys("3000000")   # Set to 3 million rupiah per month
        driver.find_element_by_xpath('//button[@class="btn btn-mamigreen btn-primary btn-price"]').click()
        time.sleep(5)
        # Click the next page button
        for i in range(0,5):
            my_target = driver.find_element_by_xpath('//div[@class="pagination-section"]/ul[@class="pagination"]/li/a[text()=">"]')
            my_target.click()
            time.sleep(10)
        for i in range(0, 18):
            # Save the current main page
            main_page = driver.current_window_handle
            driver.switch_to.window(main_page)
            # Get all 'kost' title from the main page
            all_title_kost = driver.find_elements_by_xpath('//h3[@class="room-title-text track-list-regular-kost"]')
            print(all_title_kost)
            # driver.find_element_by_xpath('//div[@class="room-title"]').click()
            time.sleep(20)
            # Testing buka semua title di list all_title_kost
            for index, title in enumerate(all_title_kost, start=1):
                # CLick into title element
                title.click()
                time.sleep(20)
                handles=driver.window_handles
                driver.switch_to.window(handles[1])
                if index == 1:
                    try:
                        for i in range(0,4):
                            # click radio button
                            python_button = driver.find_elements_by_xpath("//button[@class='btn-next btn-primary']")[0]
                            # print(python_button)
                            python_button.click()
                            time.sleep(2)
                        driver.find_elements_by_xpath("//button[@class='btn-primary swiper-button-disabled']")[0].click()
                        time.sleep(2)
                    except:
                        print("Button not found")
                # Click tombol Informasi yang lebih lengkap
                driver.find_element_by_xpath('//button[@class="btn btn-success btn-fac-more"]').click()
                time.sleep(10)
                html = driver.execute_script("return document.documentElement.outerHTML")
                # Scrapping dgn menggunakan BeautifulSoup
                soup = BeautifulSoup(html, 'html.parser')
                element = soup.findAll("div", {"class": "kost-fac-container"})
                price = soup.find("span", {"class" : "price-tag"})
                # Remove the \n and \t from price
                new_price = re.sub('\s+', '', price.get_text())
                # Remove 'Rp' from price
                new_price = new_price.replace('Rp', '')
                # Remove . from price
                new_price = new_price.replace('.', '')
                new_element = element[0].findAll("h3")
                facilities = []
                for ele in new_element:
                    string = ele.get_text()
                    count_word = string.split(" ")
                    if len(count_word) > 5:
                        continue
                    facilities.append(string)
                # Mendapatkan panjang dan lebar kamar kosan
                ukuran = facilities[0].lower()
                width, height = ukuran.split("x")
                # Menghapus ukuran kost an dari fasilitas
                del facilities[0]
                # Write the scrapping result into csv file
                # New line for remove blank row
                with open('data_kost_5.csv', mode='a', newline='') as kost_file:
                    kost_writer = csv.writer(kost_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    kost_writer.writerow([str(new_price), str(width), str(height), facilities])
                    facilities = []
                driver.close()
                driver.switch_to.window(main_page)
                # driver.switch_to_window(main_page)
                time.sleep(20)
            # Click the next page button
            my_target = driver.find_element_by_xpath('//div[@class="pagination-section"]/ul[@class="pagination"]/li/a[text()=">"]')
            my_target.click()
            time.sleep(20)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    print("Script running...")
    scrap_lists_mamikos(url)

