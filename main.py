
import telebot
from telebot.types import Message

API_TOKEN = '8157007442:AAFtZxPcM-bj88YT9ht5GZSgF8ZaAOYG364'
bot = telebot.TeleBot(API_TOKEN)

users = {}
queue = []

@bot.message_handler(commands=['start'])
def send_welcome(message: Message):
    bot.send_message(message.chat.id, "👋 Selamat datang di SambungRasa!

Ketik /cari untuk mulai mencari teman ngobrol secara anonim.")

@bot.message_handler(commands=['cari'])
def find_partner(message: Message):
    uid = message.chat.id
    if uid in users:
        bot.send_message(uid, "❗ Kamu sedang ngobrol. Ketik /stop untuk mengakhiri.")
        return
    if queue and queue[0] != uid:
        partner = queue.pop(0)
        users[uid] = partner
        users[partner] = uid
        bot.send_message(uid, "✅ Partner ditemukan! Mulailah ngobrol.")
        bot.send_message(partner, "✅ Partner ditemukan! Mulailah ngobrol.")
    else:
        queue.append(uid)
        bot.send_message(uid, "🔍 Menunggu partner...")

@bot.message_handler(commands=['stop'])
def stop_chat(message: Message):
    uid = message.chat.id
    if uid in users:
        partner = users.pop(uid)
        users.pop(partner, None)
        bot.send_message(uid, "❌ Obrolan dihentikan.")
        bot.send_message(partner, "❌ Partner keluar dari obrolan.")
    elif uid in queue:
        queue.remove(uid)
        bot.send_message(uid, "❌ Dihapus dari antrean.")
    else:
        bot.send_message(uid, "⚠️ Kamu tidak sedang dalam obrolan.")

@bot.message_handler(commands=['next'])
def next_partner(message: Message):
    stop_chat(message)
    find_partner(message)

@bot.message_handler(func=lambda message: True)
def relay_message(message: Message):
    uid = message.chat.id
    if uid in users:
        partner = users[uid]
        bot.send_message(partner, message.text)
    else:
        bot.send_message(uid, "⚠️ Kamu belum dalam obrolan. Ketik /cari untuk mulai.")

print("Bot SambungRasa aktif...")
bot.infinity_polling()
