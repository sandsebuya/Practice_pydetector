import telebot
class Bot:
	def __init__(self):
		self.bot = telebot.TeleBot(token="6929847377:AAEqLZgMri76KbRYB9AqO8PcUELulklLf4A")

	def send_message_to(self,chat_id):
		self.bot.send_message(chat_id,"Gas leak")
	def polling(self):
		self.bot.infinity_polling()
