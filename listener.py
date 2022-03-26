import RPi.GPIO as GPIO
import time
import sys
import gammu.smsd
import MySQLdb
from hx711 import HX711
from time import gmtime, strftime

customer = int(0)

db = MySQLdb.connect("localhost","root", "root", "smartdisplay" )

cursor = db.cursor()

sql = "SELECT * FROM information"

try:
cursor.execute(sql)
result = cursor.fetchall()

 for row in results:
        customer = row[0]
except:
print "Error: unable to fetch data"
db.close()

smsd = gammu.smsd.SMSD('/etc/gammu-smsdrc')

def cleanAndExit():
print "Cleaning..."
GPIO.cleanup()
print "Bye!"
sys.exit()

hx1 = HX711(5, 6)
hx2 = HX711(13, 26)
hx3 = HX711(23, 24)

hx1.set_reading_format("LSB", "MSB")
hx2.set_reading_format("LSB", "MSB")
hx3.set_reading_format("LSB", "MSB")

hx1.set_reference_unit(21)
hx2.set_reference_unit(21)
hx3.set_reference_unit(21)

hx1.reset()
hx1.tare()
hx2.reset()
hx2.tare()
hx3.reset()
hx3.tare()
status = 0

while True:
try:
val1 = hx1.get_weight(5)
val2 = hx2.get_weight(5)
val3 = hx3.get_weight(5)
messages = "Panel1: " + str(val1) + ", Panel2: " + str(val2) + ", Panel3: " + str(val3) + ", Customer: " + str(customer)

	hours = strftime("%H", gmtime())
	minutes = strftime("%M", gmtime())
	times = ((int(hours) + int(8)) * int(60)) + int(minutes)
	print times

	if int(times)%2 == 0 :
		if(status == 0):
			message = { 'Text': messages , 'SMSC' : {'Location' : 1}, 'Number' : '0928.......' }
			smsd.InjectSMS([message])
			print ("Panel1: %s , Panel2: %s , Panel3: %s, Customer: %s " %(val1,val2,val3,customer))				
			print "Message Sent"
			status = 1
	else:	
			status = 0

	hx1.power_down()
	hx1.power_up()
	hx2.power_down()
	hx2.power_up()
	hx3.power_down()
	hx3.power_up()
	time.sleep(0.5)
except (KeyboardInterrupt, SystemExit):
cleanAndExit()
