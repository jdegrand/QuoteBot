from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import random
import os
import key_file

qc_name = "qc.txt"
quotes_name = "quotes.txt"
count_name = "counts.txt"
photo_uploads = "photo_uploads.txt"
brian_folder = os.getcwd() + "/brian_photos"
current_path = os.getcwd()
qc = "Oops! This wasn't supposed to happen..."
quotes = {}
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
    file = open(quotes_name)
    for line in file:
        key_val = line.strip().split(',', 1)  # splits at first comma only
        quotes[key_val[0]] = [key_val[1], key_val[2]]
    file.close()
    file = open(count_name)
    count = int(file.readline())
    file.close()
    for line in open(photo_uploads):
        line = line.strip().split(" ")
        users[line[0]] = [line[1]]
    
def q(bot, update):
    global quotes
    best_quote = ""
    max_occurance = 0
    ref_key = ""
    for key in list(quotes.keys()):
        quote = quotes[key]
        if quote[0] > max_occurance:
            best_quote = quote[1]
            max_occurance = quote[0]
            ref_key = key
    quotes[key][0] = str(int(quotes[key][0]) + 1)
    bot.send_message(chat_id=update.message.chat_id, text=best_quote)


def r(bot, update, args):
    global quotes
    if len(args) == 0:
        quote_info_list = random.choice(list(quotes.values()))  # occurance at index 0, quote at index 1
        q = quote_info_list[1]
    else:
        user_text = " ".join(args)
        if user_text.strip() in quotes:  
            q = quotes[user_text][1]
            quotes[user_text][0] = str(int(quotes[user_text][0]) + 1)
        else:
            q = "Sorry, I don't seem to have any quotes for that one. Be the first to add one on that topic!"
    bot.send_message(chat_id=update.message.chat_id, text=q)
    

def add(bot, update, args):
    global quotes, quotes_name
    if update.message.reply_to_message != None:
        quote_key = " ".join(args).split()
        if len(quote_key) == 0:
            q = "Please retry! Make sure to give a key for the quote!"
        else:
            reply_text = update.message.reply_to_message.text
            if len(reply_text.strip()) != 0:
                quotes[quote_key] = [0, reply_text]
                with open(quotes_name, 'a') as file:
                    file.write(quote_key, ',', str(0), ',', reply_text, '\n')
    user_text = " ".join(args)
    key_val = user_text.split(',', 1)
    elif len(key_val) == 2:
        quotes[key_val[0].strip()] = [0, key_val[1].strip()]
        with open(quotes_name, 'a') as file:
                file.write(key_val[0], ',', str(0), ',', user_text + '\n')
    elif user_text.split('+') == 1:  # no ',' or '+' in args
            q = "Sorry, try entering the quote like this: <key> , <quote>"
            bot.send_message(chat_id=update.message.chat_id, text=q)
    else:
        add_lst = user_text.split('+')
        if len(add_lst) >= 2:
            try:
                add_sum = 0
                for entry in add_lst:
                    add_sum += int(entry.strip())
                q = str(add_sum)
                bot.send_message(chat_id=update.message.chat_id, text=q)
            except ValueError:
                q = "Invalid addition!"
                bot.send_message(chat_id=update.message.chat_id, text=q)

      

def say(bot, update, args):
   user_text = " ".join(args)
   if len(user_text.strip()) != 0:
        bot.send_message(chat_id=update.message.chat_id, text=user_text)

def upload_brian(bot, update, user_data):
    global count
    global count_name
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

#def not_brian(bot, update):
#    global brian_folder, count_name
#    global users, count
#    file_id = update.message.reply_to_message.image.photo[-1].file_id  # assume one photo
#    fname = str(count) + '.jpg'
#    del users[fname]
#    count -= 1
#    with open(count_name, 'w') as file:
#        file.write(str(count))

def tk(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Sean is That Kid")
    

def help(bot, update):
    update.message.reply_text("Type in '/' for a list of commands!")

def main():
    key = key_file.get_key()
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
