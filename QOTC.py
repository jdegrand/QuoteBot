from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import random
import os

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
        key_val = line.strip().split(',', 2)  # splits at first two commas  only
        if key_val[0].strip() != "":
            quotes[key_val[0].strip()] = [key_val[1].strip(), key_val[2].strip()]
        else:
            quotes_no_key.append([key_val[1].strip(), key_val[2].strip()])
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
        if key == None:  # contains all quotes with no key
            for i in range(len(quotes[key])):  # iterate through no-key quotes
                if int(quotes[key][i][0]) > max_occurance:
                    best_quote = quotes[key][i][1]
                    max_occurance = int(quotes[key][i][0])
                    ref_key = key
                    no_key_index = i
        else:
            quote = quotes[key]
            if int(quote[0]) > max_occurance:
                best_quote = quote[1]
                max_occurance = int(quote[0])
                ref_key = key
    if ref_key is None:
        quotes[ref_key][no_key_index][0] = str(int(quotes[ref_key][no_key_index][0]) + 1)
    else:
        quotes[ref_key][0]  = str(int(quotes[ref_key][0]) + 1)
    bot.send_message(chat_id=update.message.chat_id, text=best_quote)


def r(bot, update, args):
    global quotes
    total_entries = len(quotes) + len(quotes[None]) - 1
    if len(args) == 0:
        choice_from_total = random.randint(0, total_entries)
        if choice_from_total < len(quotes):  # choose from quotes with key
            quote_info_list = [[]]  # make following conditional true
            while type(quote_info_list[0]) == list:  # anything besides quotes[None]
                 quote_info_list = random.choice(list(quotes.values()))  # occurance at index 0, quote at index 1
        else:
            quote_info_list = random.choice(quotes[None])
        q = quote_info_list[1]
        bot.send_message(chat_id=update.message.chat_id, text=q)
        quote_info_list[0] = str(int(quote_info_list[0]) + 1)
    else:
        user_text = " ".join(args)
        if user_text.strip() in quotes:
            q = quotes[user_text][1]
            bot.send_message(chat_id=update.message.chat_id, text=q)
            quotes[user_text][0] = str(int(quotes[user_text][0]) + 1)
        else:
            filt = [i for i in quotes[None] if args[0].lower() in i[1].lower()]
            if len(filt) == 0:
                q = "Sorry, I don't seem to have any quotes for that one. Be the first to add one on that topic!"
            else:
                rand_idx = random.randint(0, len(filt)-1)
                q = filt[rand_idx][1]
                filt[rand_idx][0] = str(int(filt[rand_idx][0]) + 1)
            bot.send_message(chat_id=update.message.chat_id, text=q)
    

def add(bot, update, args):
    global quotes, quotes_name
    user_text = " ".join(args)
    key_val = user_text.split(',', 1)
    if update.message.reply_to_message != None:
        quote_key = user_text.split()
        reply_text = update.message.reply_to_message.text
        if len(reply_text.strip()) != 0:
            if len(quote_key) == 0:
                quotes[None].append[0, reply_text]
            else:
                quotes[user_text] = [0, reply_text]
            with open(quotes_name, 'a') as file:
                file.write(user_text + ',' + str(0) + ',' + reply_text + '\n')
    elif len(key_val) == 2:
        if key_val[0].strip() in quotes:
            q = "Sorry, that key is already in use!"
            bot.send_message(chat_id=update.message.chat_id, text=q)
        else:
            quotes[key_val[0].strip()] = [0, key_val[1].strip()]
            with open(quotes_name, 'a') as file:
                file.write(key_val[0].strip() + ',' + str(0) + ',' + key_val[1].strip() + '\n')
    elif len(user_text.split('+')) == 1:  # no ',' or '+' in args
        if len(user_text.strip()) != 0:
            quotes[None].append([0, user_text])
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

def yesornos(bot, update, args):
    nos = "That one is a nos fam"
    yes = "I'd give that one a yes"
    reply = "Hmm, ask me again sometime"
    value = 1
    value = random.randint(0, 1)
    if value == 1:
        reply = nos
    else:
        reply = yes
    bot.send_message(chat_id=update.message.chat_id, text=reply)

def drawstraws(bot, update, args):
    user_text = " ".join(args)
    halves = user_text.split(',')
    if len(halves) == 2:
        halves[0] = halves[0].split(" ")
        halves[1] = halves[1].split(" ")
    print(halves)
    if len(halves) != 2:
        bot.send_message(chat_id=update.message.chat_id, text="Please use one ',' to seperate arguments")
    elif len(halves[0]) != len(halves[1]):
        bot.send_message(chat_id=update.message.chat_id, text="Please use the same number of arguments for both sides")
    else:
        result = {}
        for i in range(0, len(halves[0])):
            index = random.randint(0, len(halves[1]) - 1)
            result[halves[0][i]] = halves[1][index]
            del halves[1][index]
        final = ""
        for key in result.keys():
            temp = key + "    " + result[key] + "\n"
            final += temp
        bot.send_message(chat_id=update.message.chat_id, text=final)

            
        
    

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
    command.add_handler(CommandHandler("yesornos", yesornos, pass_args=True))
    command.add_handler(CommandHandler("drawstraws", drawstraws, pass_args=True))
    
    command.add_handler(CommandHandler("help", help))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
