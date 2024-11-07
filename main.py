#import all libraries
import instagram
import time
import facebook
import twitter
from selenium import webdriver as web


#import check
driver=web.Chrome()
time.sleep(1)

#set all integer to 0
facelogged=0

#counter function
def count():

    #open file and add 1
    f=open("count.txt","r")
    accnt=list(map(str,f.read().split()))
    accnt=int(accnt[0])
    f.close()
    fi=open("count.txt","w")
    fi.write(str(accnt+1))
    fi.close
    return accnt


#secrets.txt file inculude username and password
def secrets(check):
    #open file
    f=open("secrets.txt","r")
    accnt=list(f.read().split("\n"))
    name_pass = accnt[0].split(" ")
    f.close()
    return name_pass[1], name_pass[2]

#main activity
try:
    #write caption of post
    # caption=input("Write caption: ")
    caption = "test_me"
    facebook.drivers(driver)
    #if already logged in this will be activated
    if facelogged:
        facebook.openurl("https://facebook.com")
        print("Already logged in")
    else:
        facebook.openurl("https://facebook.com")
        time.sleep(5)
        faceusrn, facepass = secrets()
        facebook.login(faceusrn, facepass)            
        #login check set 1
        facelogged=1

    #select post mode
    # post_mode=input("Normal(n/normal) || With Photo(p/photo): ")
    post_mode = "normal"
    #if select normal mode this will be activated
    if post_mode.lower()=="normal" or post_mode.lower()=="n":
        #share facebook post
        time.sleep(5)   
        facebook.share_post(caption+str(count()))
    elif post_mode.lower()=="photo" or post_mode.lower()=="p":
        img_url=input("Enter photo url(don't forget revers slash to double): ")
        #share facebook post with photo
        time.sleep(5)
        facebook.share_post(caption+str(count()),img_url)
    else:
        print("Invalid selection")
except Exception as e:
    print(e)
driver.close()
print("Closed")
