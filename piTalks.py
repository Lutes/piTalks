mport urllib2
import re
import RPi.GPIO as GPIO
from datetime import datetime
import time
import sys
import pyttsx


GPIO.setmode(GPIO.BCM)

global Quote

with open('Quote') as f:
   Quote =  f.read().splitlines()

#Weather
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#Local News
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#National News
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#International News
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#Quote
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)


#???
#GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#input_state = GPIO.input(24)


#gives current weahter
def current_weather():
    current = ""
    #The RSS page enviroment canada
    urls = ["http://weather.gc.ca/rss/city/qc-147_e.xml"]
    i = 0
    #Regex for current conditions
    current_reg = "<title>Current Conditions: (.+?)</title>"
    current_pattern = re.compile(current_reg)
    #Cycles through every line of HTML
    url = urllib2.urlopen(urls[i])
    s = url.read()
    current_weather = re.findall(current_pattern,s.decode('utf-8').encode('utf-8'))
    current = re.sub('\&#xB0;C',' degrees celsius ',current_weather[0])
    current = "Current weather " + current
    i+=1
    return current


#gives forecasted weahter    
def forecasted_weather():
    forecast = ""
    #The RSS page enviroment canada
    urls = ["http://weather.gc.ca/rss/city/qc-147_e.xml"]
    i = 0
    #Regex for forecasted conditions
    forecast_reg = "<summary type=\"html\">(.+?)Forecast issued"
    forecast_pattern = re.compile(forecast_reg)
    #Cycles through every line of HTML
    url = urllib2.urlopen(urls[i])
    s = url.read()
    forecast_weather = re.findall(forecast_pattern,s.decode('utf-8').encode('utf-8'))
    forecast = "Forecasted weather," + forecast_weather[0] + " Later " + forecast_weather[1]
    i+=1
    return forecast

#gives international news stories   
def international_news():
    #CBC World News
    urls = ["http://www.cbc.ca/cmlink/rss-world"]
    i = 0
    adjusted_news = []
    #Regex
    news_reg = "(<p>)(.+?)(<\/p>)"
    news_pattern = re.compile(news_reg)
    #Cycles through every line of HTMl          
    url = urllib2.urlopen(urls[i])
    s = url.read()
    news = re.findall(news_pattern,s.decode('utf-8').encode('utf-8'))
    #Return the top three news stories
    for index in range(15):
        adjusted_news.append(news[index][1])
    i+=1
    return adjusted_news

def national_news():
    #CBC Canada News
    urls = ["http://www.cbc.ca/cmlink/rss-canada"]
    i = 0
    adjusted_news = []
    #Regex
    news_reg = "(<p>)(.+?)(<\/p>)"
    news_pattern = re.compile(news_reg)
    #Cycles through every line of HTML
    url = urllib2.urlopen(urls[i])
    s = url.read()
    news = re.findall(news_pattern,s.decode('utf-8').encode('utf-8'))
    #Return the top three news stories
    for index in range(15):
        adjusted_news.append(news[index][1])
    i+=1
    return adjusted_news

def nb_news():
    #CBC NB News
    urls = ["http://www.cbc.ca/cmlink/rss-canada-newbrunswick"]
    i = 0
    adjusted_news = []
    #Regex
    news_reg = "(<p>)(.+?)(<\/p>)"
    news_pattern = re.compile(news_reg)
    #Cycles through every line of HTML
    url = urllib2.urlopen(urls[i])
    s = url.read()
    news = re.findall(news_pattern,s.decode('utf-8').encode('utf-8'))
    #Return the top three news stories
    for index in range(15):
        adjusted_news.append(news[index][1])
    i+=1
    return adjusted_news


def update():
        global cw
        cw = current_weather()
        global fw
        fw = forecasted_weather()
        global iin
        iin = international_news()
        global nn
        nn = national_news()
        global ln
        ln = nb_news()


update()

i = 0
n = 0
l = 0
q = 0
u = 0
engine = pyttsx.init()
volume = engine.getProperty('volume')
engine.setProperty('volume', volume+1.00)
rate = engine.getProperty('rate')
engine.setProperty('rate', rate-70)


print("(F)orecast, (C)urrent, (I)nternational, (N)ational, (L)ocal")
while(1):

   ctime = datetime.now()

#print ctime.minute 
   if ((ctime.minute == 10) and (u == 0)):
        update()
        u = 1
        print "updating"

   if (ctime.minute == 11):
        u = 0

   if (GPIO.input(17) == False):
        engine.say(cw + fw)
        engine.runAndWait()
   elif (GPIO.input(18) == False):
        engine.say(iin[i])
        i = i + 1
        engine.runAndWait()
   elif (GPIO.input(27) == False):
        engine.say(nn[n])
        n = n + 1
        if n > 15:
            n = 0
        engine.runAndWait()
   elif (GPIO.input(23) == False):
        engine.say(ln[l])
        l = l + 1
        engine.runAndWait()

   elif ( GPIO.input(4) == False):
        engine.say(Quote[q])
        engine.runAndWait()
        print Quote[q]
        q = q + 2
        if (q == 346):
                q = 0

   engine.runAndWait()




