from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import random
import os

qc_name = "qc.txt"
quotes_name = "quotes.txt"
count_name = "counts.txt"
photo_uploads = "photo_uploads.txt"
brian_folder = os.getcwd() + "/brian_photos"
current_path = os.getcwd()
qc = "Oops! This wasn't supposed to happen..."
quotes = []
count = 0
users = {}

def init():
    global qc
    global quotes
    global count
    global users
    global photo_uploads
    file = open(qc_name)
    qc = file.readline()
    file.close()
    quotes = [line.strip() for line in open(quotes_name)]
    file = open(count_name)
    count = int(file.readline())
    file.close()
    for line in open(photo_uploads):
        line = line.strip().split(" ")
        users[line[0]] = line[1]
    
def q(bot, update):
    global qc
    bot.send_message(chat_id=update.message.chat_id, text=qc)

def r(bot, update, args):
    global quotes
    if len(args) == 0:
        q = quotes[random.randint(0, len(quotes) - 1)]
    else:
        filt = [i for i in quotes if args[0].lower() in i.lower()]
        if len(filt) == 0:
            q = "Sorry, I don't seem to have any quotes for that one. Be the first to add one on that topic!"
        else:
            q = filt[random.randint(0, len(filt) - 1)]
    bot.send_message(chat_id=update.message.chat_id, text=q)
    

def add(bot, update, args):
    global quotes
    if update.message.reply_to_message != None:
        reply_text = update.message.reply_to_message.text
        if len(reply_text.strip()) != 0:
            quotes += [reply_text]
            with open(quotes_name, 'a') as file:
                file.write(reply_text + "\n")
    user_text = " ".join(args)
    if len(user_text.strip()) != 0:
       quotes += [user_text]
       with open(quotes_name, 'a') as file:
           file.write(user_text + "\n")

def say(bot, update, args):
   user_text = " ".join(args)
   if len(user_text.strip()) != 0:
        bot.send_message(chat_id=update.message.chat_id, text=user_text)

def upload_brian(bot, update, user_data):
    global count
    global current_path
    global brian_folder
    global users
    global photo_uploads
    path = "brian.png"
    file_id = update.message.photo[-1].file_id
    newFile = bot.get_file(file_id)
    fname = str(count) + '.jpg'
    users[fname] = update.message.from_user.first_name
    print(users[fname])
    with open(photo_uploads, 'a') as file:
        file.write(fname + " " + update.message.from_user.first_name + "\n")
    newFile.download(str(count) + '.jpg')
    os.rename(current_path + '/' + fname, brian_folder + '/' + fname)
    count += 1
    file = open(count_name, 'w')
    file.write(str(count))
    file.close()

def brian(bot, update):
    global brian_folder
    global users
    brian = random.choice(os.listdir(brian_folder))
    cap = "Uploaded by " + users[brian]
    bot.send_photo(chat_id=update.message.chat_id, photo=open(brian_folder + '/' + brian, 'rb'), caption=cap)

def tk(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Sean is That Kid")
    

def help(bot, update):
    update.message.reply_text("Type in '/' for a list of commands!")

def main():
    key = os.environ['TELEGRAM_BOT_KEY']
    init()
    updater = Updater(key)
    command = updater.dispatcher

    command.add_handler(CommandHandler("q", q))
    command.add_handler(CommandHandler("r", r, pass_args=True))
    command.add_handler(CommandHandler("add", add, pass_args=True))
    command.add_handler(CommandHandler("say", say, pass_args=True))
    command.add_handler(MessageHandler(Filters.photo, upload_brian, pass_user_data=True))
    command.add_handler(CommandHandler("brian", brian))
    command.add_handler(CommandHandler("tk", tk))
    
    command.add_handler(CommandHandler("help", help))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
