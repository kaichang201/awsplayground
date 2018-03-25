import boto3
import os
from botocore.exceptions import ClientError
from botocore.vendored import requests


myKey = os.environ['myWeatherKey']
mailFrom = os.environ['mailFrom']
wunderGround = os.environ['weatherURL']
mailTo = os.environ['mailTo'].split()


foreCastURI = '/forecast/q'
hourlyURI = '/hourly/q'
hoboken = '/NJ/Hoboken'
jsonRequest = '.json'
mailBody = ''



def lambda_handler(event, context):
    return sendWeather()


def sendWeather():
    myForecastTxtDict = dict()
    myForecastTempDict = dict()
    myHourlyDict = dict()
    mailBody = ''

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

    mailToAddresses = ", ".join(mailTo)

    sendEmail(mailFrom, mailTo, mailSubject, mailBody)
    return 

def sendEmail (fromAddress, toAddresses, subjectLine, mailBody) :
    # Replace sender@example.com with your "From" address.
    # This address must be verified with Amazon SES.
    SENDER = fromAddress
    
    # Replace recipient@example.com with a "To" address. If your account 
    # is still in the sandbox, this address must be verified.
    RECIPIENT = toAddresses
    
    # Specify a configuration set. If you do not want to use a configuration
    # set, comment the following variable, and the 
    # ConfigurationSetName=CONFIGURATION_SET argument below.
    #CONFIGURATION_SET = "ConfigSet"
    
    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "us-west-2"
    
    # The subject line for the email.
    SUBJECT = subjectLine
    
    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = (mailBody)
                
    # The HTML body of the email.
    BODY_HTML = "<pre>" + mailBody + "</pre>"

    # The character encoding for the email.
    CHARSET = "UTF-8"
    
    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)
    
    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': mailTo
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
            #ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.    
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['ResponseMetadata']['RequestId'])