from config import keys
from selenium import webdriver;
import os
from pyrobot import Robot
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui
import xerox
import time
import datetime

def order(k,folder_name,path_upload,photo_path_final):

    #Lauching chrome in mobile version
    mobileEmulation = {'deviceName': 'Pixel 2'}
    options = webdriver.ChromeOptions()
    options.add_experimental_option('mobileEmulation', mobileEmulation)
    driver = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=options)


    #setting the photo_path and the caption text
    photo_path=photo_path_final
    caption_path=path_upload+'\\'+folder_name + '\\text.txt'    
    print(photo_path)
    content_array = []
    with open(caption_path) as f: 
        for line in f:
            content_array.append(line)    
    print(content_array)
    
    #going to instagram page and loging in
    driver.get(k['URL_insta'])
    time.sleep(1)
    driver.find_element_by_name('username').send_keys(k["username"])
    driver.find_element_by_name('password').send_keys(k["password"])
    driver.find_element_by_name('password').send_keys(Keys.RETURN)
    wait = ui.WebDriverWait(driver,20)

    #dealing with the popups
    time.sleep(10)
    if driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/button[2]') != 0:
        driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/button[2]').click()

    #Photo being selected and uploaded
    time.sleep(4)
    robot = Robot()
    xerox.copy(photo_path_final)     
    driver.find_element_by_xpath('//*[@id="react-root"]/section/nav[2]/div/div/div[2]/div/div/div[3]').click()
    time.sleep(4)
    robot.paste() 
    robot.press_and_release('enter')
    
    #photo being adjusted
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="react-root"]/section/div[2]/div[2]/div/div/div/button[1]').click()
    driver.find_element_by_xpath('//*[@id="react-root"]/section/div[1]/header/div/div[2]/button').click()

    #Putting the caption and posting the image
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="react-root"]/section/div[2]/section[1]/div[1]/textarea').click()
    driver.find_element_by_xpath('//*[@id="react-root"]/section/div[2]/section[1]/div[1]/textarea').send_keys(content_array) 
    #driver.find_element_by_xpath('//*[@id="react-root"]/section/div[1]/header/div/div[2]/button').click()

    #Posting the image
    time.sleep(15)
    driver.quit()
    done= "Photo:"+photo_path +" Successfully uploaded"
    print(done)
    return done


if __name__ =='__main__':
    
    for cont in range(89000):
    #Navigating to the correct folder depending on the date
        print(cont)
        tday =datetime.date.today()
        day = tday.day
        ppp=os.getcwd()+"\\Uploads\\"
        post_path= ppp +str(day)
        print(post_path)
        

        #Getting a list of all the times that uploads will take place.
        todays_uploads=os.listdir(post_path)  
        todays_uploads.sort()
        print(todays_uploads)

        #getting the correct time
        ttime =datetime.datetime.now()
        hours =ttime.hour
        mins =ttime.minute
        current_time=str(hours) +'.'+ str(mins)
        print(current_time)
        for t in todays_uploads:
            upload_hours=str(t).split('.')[0]
            #print(upload_hours)
            #print(hours)
            if int(upload_hours)==int(hours):
                print("correct hour")
                upload_mins=str(t).split('.')[1]
                print(upload_mins)
                if int(upload_mins)==int(mins):
                    print("correct min")

                    photo_path=post_path+'\\'+t
                    check_photo=os.listdir(photo_path)
                    print (check_photo)
                    for i in check_photo:
                        if "photo" in i:
                            photo = photo_path+'\\'+i
                            print(photo)                           
                            order(keys,t,post_path,photo)
                    
        time.sleep(30)

        

            
            
    
    

    