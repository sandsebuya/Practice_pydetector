import os
from threading import Thread, Event
import time
import logging
from telegram import Bot
is_ringing = False



class IO:
	def __init__(self):
		os.system("gpio mode 0 in && gpio mode 1 in && gpio mode 2 in && gpio mode 3 out")
		self.event = Event()
		os.system("gpio write 3 1")
		time.sleep(1)
		os.system("gpio write 3 0")
		self.notification_url="https://trigger.macrodroid.com/f20ebf81-f366-4955-a912-93109c948da8/leakIson"
	def test(self):
		while (True):
			a = os.popen("gpio read 0").read().rstrip("\n")
			b = os.popen("gpio read 1").read().rstrip("\n")
			c = os.popen("gpio read 2").read().rstrip("\n")
			if(a=='1'):
				os.system("gpio write 3 1")
				pass
			else:
				os.system("gpio write 3 0")
				pass
			print("Pin 3 is {} pin 5 is {} pin 7 is {}\r".format(a,b,c),end="")

	def work(self,event):
		tbot= Bot()
		#Thread(target=tbot.polling).start()
		global is_ringing
		while True:
			a = os.popen("gpio read 0").read().rstrip("\n")
			b = os.popen("gpio read 1").read().rstrip("\n")
			c = os.popen("gpio read 2").read().rstrip("\n")
			if c=="1":
				os.system("gpio write 3 0")
				is_ringing = False
			elif a=="1" or b =="1":
				logging.info("send notification")
				os.system("curl "+self.notification_url)
				tbot.send_message_to(5115806473)
				os.system("gpio write 3 1")
				print("any is pressed")
				is_ringing = True
				time.sleep(.8)

def work_with_beeps( event):
	#print("ih")
	global is_ringing
	pos = True
	while True:
		if event.is_set():
			#print("exit")
			os.system("gpio write 3 0")
			return
		if is_ringing:
			if pos:
				print("ON")
				os.system("gpio write 3 1")
			else:
				print("off")
				os.system("gpio write 3 0")
			time.sleep(2)
			pos = not (pos)
			continue
		pos= True
io= IO()

def start():
	global is_ringing
	global io
	print("This is debug mode")
	thread = Thread(target=work_with_beeps, args=(io.event,))
	while (True):
		string = input("> ")
		if string.lstrip() == ".t":
			try:
				io.test()
			except KeyboardInterrupt:
				# os.system("clear")
				print("\r❤️" + " " * 50, end="\n")
		elif string.lstrip() == ".s":
			try:
				io.event.clear()
				print("starting")
				thread.start()
				io.work( io.event)
			except KeyboardInterrupt:
				# os.system("clear")
				print("\r❤️" + " " * 50, end="\n")
				io.event.set()
		elif string.lstrip()==".r":
			is_ringing=True
			work_with_beeps(io.event)
		else:
			print("Unknown command")

def disable_module(event):
	event.set()
	print("disable")
def get_event():
	global io
	return io.event
def start_from():
	global is_ringing
	global io
	thread = Thread(target=work_with_beeps, args = (io.event,))
	thread.start()
	io.work(io.event)
if __name__=="__main__":
	try:
		start()
	except KeyboardInterrupt:
		io.event.set()
		pass
