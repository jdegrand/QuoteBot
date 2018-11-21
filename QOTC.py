from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import random
import os
from entry import Entry

quotes_name = "quotes.txt"
count_name = "counts.txt"
photo_uploads = "photo_uploads.txt"
brian_folder = os.getcwd() + "/brian_photos"
current_path = os.getcwd()
quotes = {}
count = 0
users = {}

def init():
    global quotes
    global count
    global users
    global photo_uploads
    quotes_no_key = []
    file = open(quotes_name)
    for line in file:
        key_occur_val = line.strip().split(',', 2)  # splits at first two commas  only
        key = key_occur_val[0].strip()
        occurances = key_occur_val[1].strip()
        quote = key_occur_val[2].strip()
        if key_occur_val[0].strip() != "":
            quotes[key] = Entry(key, occurances, quote)
        else:
            quotes_no_key.append(Entry(key, occurances, quote))
    file.close()
    quotes[None] = quotes_no_key
    file = open(count_name)
    count = int(file.readline())
    file.close()
    for line in open(photo_uploads):
        line = line.strip().split(" ")
        users[line[0]] = line[1]

def q(bot, update):
    global quotes
    best_quote = ""
    max_occurance = 0
    ref_key = ""
    no_key_index = None
    for key in list(quotes.keys()):
        if key is None:  # contains all quotes with no keyi
            quotes_no_key = quotes[None]
            for i in range(len(quotes_no_key)):  # iterate through no-key quotes
                if quotes_no_key[i].get_occurances() > max_occurance:
                    best_quote = quotes_no_key[i].get_quote()
                    max_occurance = quotes_no_key[i].get_occurances()
                    ref_key = None
                    no_key_index = i
        else:
            entry = quotes[key]
            if entry.get_occurances() > max_occurance:
                best_quote = entry.get_quote()
                max_occurance = entry.get_occurances()
                ref_key = key
    if ref_key is None:
        quotes[None][no_key_index].increment_occurances()
    else:
        quotes[ref_key].increment_occurances()

    occur = "Number of references: " + str(max_occurance+1)
    q = best_quote + '\n\n' + occur
    bot.send_message(chat_id=update.message.chat_id, text=q)


def r(bot, update, args):
    global quotes
    total_entries = len(quotes) + len(quotes[None]) - 1
    if len(args) == 0:
        choice_from_total = random.randint(0, total_entries)
        if choice_from_total < len(quotes):  # choose from quotes with key
            random_entry = Entry(None, 0, "")  # make following conditional true
            while random_entry.get_key == None:  # anything besides quotes[None]
                 random_entry = random.choice(list(quotes.values()))  # occurance at index 0, quote at index 1
        else:
            random_entry = random.choice(quotes[None])
        quote = random_entry.get_quote()
        bot.send_message(chat_id=update.message.chat_id, text=quote)
        random_entry.increment_occurances()
    else:
        user_text = " ".join(args)
        if user_text.strip() in quotes:
            entry = quotes[user_text]
            quote = entry.get_quote()
            bot.send_message(chat_id=update.message.chat_id, text=quote)
            entry.increment_occurances()
        else:
            filt = [i for i in quotes[None] if args[0].lower() in i.get_quote().lower()]
            if len(filt) == 0:
                quote = "Sorry, I don't seem to have any quotes for that one. Be the first to add one on that topic!"
            else:
                entry = filt[random.randint(0, len(filt)-1)]
                quote = entry.get_quote()
                entry.increment_occurances()
            bot.send_message(chat_id=update.message.chat_id, text=quote)
    

def add(bot, update, args):
    global quotes, quotes_name
    user_text = " ".join(args)
    key_val = user_text.split(',', 1)
    if update.message.reply_to_message != None:
        quote_key = user_text.strip()
        reply_text = update.message.reply_to_message.text
        if len(reply_text.strip()) != 0:
            if not len(quote_key) == 0:
                if not quote_key in quotes:
                    quotes[None].append(Entry(None, 0, reply_text))
                else:
                    q = "Sorry, that key is already in use!"
                    bot.send_message(chat_id=update.message.chat_id, text=q)
            else:
                quotes[user_text] = Entry(quote_key, 0, reply_text)
            with open(quotes_name, 'a') as file:
                file.write(user_text + ',' + str(0) + ',' + reply_text + '\n')
    elif len(key_val) == 2:
        if key_val[0].strip() in quotes:
            q = "Sorry, that key is already in use!"
            bot.send_message(chat_id=update.message.chat_id, text=q)
        else:
            key = key_val[0].strip()
            quote = key_val[1].strip()
            quotes[key] = Entry(key, 0, quote)
            with open(quotes_name, 'a') as file:
                file.write(key + ',' + str(0) + ',' + quote + '\n')
    elif len(user_text.split('+')) == 1:  # no ',' or '+' in args
        if len(user_text.strip()) != 0:
            quotes[None].append(Entry(None, 0, user_text))
            with open(quotes_name, 'a') as file:
                file.write(',' + str(0) + ',' + "\n")
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
