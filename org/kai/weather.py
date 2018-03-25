#!/usr/bin/python
'''
Created on Jan 29, 2017

@author: kai
'''

import requests
import smtplib
from email.mime.text import MIMEText

myKey = '68d80040a0370286'
wunderGround = 'http://api.wunderground.com/api/'
foreCastURI = '/forecast/q'
hourlyURI = '/hourly/q'
hoboken = '/NJ/Hoboken'
jsonRequest = '.json'
mailFrom = 'kaichang201@gmail.com'
mailTo = ['kaichang2@gmail.com','wangdandans@gmail.com']
mailBody = ''



if __name__ == '__main__':
    myForecastTxtDict = dict()
    myForecastTempDict = dict()
    myHourlyDict = dict()

    resp = requests.get(wunderGround+myKey+foreCastURI+hoboken+jsonRequest)
    myForecast = resp.json()
    resp = requests.get(wunderGround+myKey+hourlyURI+hoboken+jsonRequest)
    myHourly = resp.json()


    timeStamp = myForecast['forecast']['txt_forecast']['date']

    mailSubject = timeStamp + ' ' + hoboken

    # parsing
    for forecastText in myForecast['forecast']['txt_forecast']['forecastday']:
        myForecastTxtDict[forecastText['title']] = forecastText['fcttext']

    for forecastText in myForecast['forecast']['simpleforecast']['forecastday']:
        myForecastTempDict[forecastText['date']['weekday']] = forecastText['low']['fahrenheit'] + '-' + forecastText['high']['fahrenheit']

    for forecastText in myHourly['hourly_forecast']:
        myHourlyDict[forecastText['FCTTIME']['civil']] = forecastText['condition'] + ' ' + forecastText['temp']['english'] + ' Feels ' + forecastText['feelslike']['english']

    # printing

    mailBody = mailBody + "\n\n12 Hour Forecast"
    for key in myHourlyDict:
        mailBody = mailBody + "\n" + key + ': ' + myHourlyDict[key]

    mailBody = mailBody + "\n\nDaily"
    for key in myForecastTempDict:
        mailBody = mailBody + "\n" + key + ": " + myForecastTempDict[key]

    mailBody = mailBody + '\n\nDetails'

    for key in myForecastTxtDict:
        mailBody = mailBody + "\n" + key + ": " + myForecastTxtDict[key]

    msg = MIMEText(mailBody)
    msg['Subject'] = mailSubject
    msg['From'] = mailFrom
    msg['To'] = ", ".join(mailTo)

#    s = smtplib.SMTP('localhost')
#    s.sendmail(mailFrom, mailTo, msg.as_string())
#    s.quit()

    #print (mailBody)
    print (msg)
    
