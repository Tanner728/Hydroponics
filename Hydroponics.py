import serial
import datetime
import time
from time import strftime
import yagmail

#adjustable Constants
delay = 3 #The amount of time that the program will wait between sending emails if something is wrong

temp_high = 26.00 #The highest temp that the water can should go. 

temp_low = 20.00 #The lowest temp that the water can should go.

ph_high = 7.1

ph_low = 7

#will be used to call all other functions and add delays
def main():
    while True:
        time.sleep(delay)
        create_temp()
        create_ph()
        print(create_ph())
        temp_check(create_temp())
        ph_check(create_ph())
        write_csv(create_temp(),create_ph(),date())

#Reading serial from arduino
ser = serial.Serial('/dev/ttyACM0',9600,timeout=1)
ser.reset_input_buffer()

#Decoding Serial Data to find temperature reading
def create_temp():
    while True:
        if ser.in_waiting>0:
            raw_serial = ser.readline()
            cookedserial = (raw_serial.decode('utf-8').strip('\r\n'))
            temperature = float(cookedserial[5:10])
            return temperature


def create_ph():
    while True:
        if ser.in_waiting>0:
            raw_serial = ser.readline()
            cookedserial = (raw_serial.decode('utf-8').strip("\r\n"))
            ph = float(cookedserial[0:4])
            return ph
#Get current date and time for measurements.
def date():
    date = datetime.datetime.now()
    return date

#Checks the temperature of the water. 
def temp_check(temperature):
    if temperature > temp_high or temperature < temp_low:
        create_email_temp(create_temp(),date())
    else:
            print("Everything is all good here")

#Check the ph of the water.
def ph_check(ph):
    if ph > ph_high or ph < ph_low:
        create_email_ph(ph_check(),date())
    else:
        print("The Ph is within specification.")

#Has all of the email information and the email format.  
def create_email_temp(temperature,time):
    #email login settings
    user = 'MSUMhydroponics@gmail.com'
    app_password = 'gxmy jvmp ygyj ixou'
    to = user

    subject = 'Water Temperature'

    content = 'The temperature of the water was {0} at {1}, this is outside of the set range ({2}-{3}).'.format(temperature,time,temp_low,temp_high)

    with yagmail.SMTP(user,app_password) as yag:
        yag.send(to,subject,content)
        print('Sent Email')

#Has all of the email information and the email format.  
def create_email_ph(temperature,time):
    #email login settings
    user = 'MSUMhydroponics@gmail.com'
    app_password = 'gxmy jvmp ygyj ixou'

    to = user
    
    subject = 'Water PH'

    content = 'The PH of the water was {0} at {1}, this is outside of the set range ({2}-{3}).'.format(ph,time,ph_low,ph_high)

    with yagmail.SMTP(user,app_password) as yag:
        yag.send(to,subject,content)
        print('Sent Email')

def write_csv(temperature,ph,date):
#write temperature data to Data.csv
    with open ('/home/raspi/Desktop/hydroponics/Data.csv',"a") as log:
        log.write("{0},{1}\n".format(strftime("%Y-%m-%d %H:%M:%S"),str(temperature)))
        print("Data Recorded at {}".format(date))
        time.sleep(delay)
        
main()

