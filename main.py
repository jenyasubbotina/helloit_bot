from PIL import Image, ImageDraw, ImageFont
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import os

name = ''
surname = ''
teacher = ''
course = ''
teachers_names = ['Bekhzodov Fozilbek', "Saidjonov Behruz",
                  'Yusupov Afzal', 'Ibragimov Desir', 'Subbotina Evgeniya']
sign_path = 'unterschrifte/'
signatures = ['f.png', 'b.png', 'a.png', 'd.png', 's.png']
course_names = [
    'Python for beginners',
    'C# for beginners',
    'WEB technologies stage 1',
    'WEB technologies stage 2',
    'WEB technologies stage 3',
    'Programming Algorithms stage 1',
    'Programming Algorithms stage 2',
]

# Python for beginners
# C# for beginners
# WEB technologies stage 1/2/3 ...
# Programming Algorithms stage 1/2

token = "796303915:AAF4MJs2lqEYxUWtK-7VSjYVWGjeLhNEXnU"
bot = telebot.TeleBot(token)


def check_string(str1):
    str1 = str1.lower()
    for i in str1:
        if i not in "abcdefghijk lmnopqrstuvwxyz-'":
            return False
    return True


def surname_step(message):
    if message.text == '/start' or message.text == '/certificate':
        bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
        return
    global name
    name = message.text
    if not check_string(name):
        msg = bot.send_message(message.chat.id, 'Попробуйте снова. Фамилия должна быть на латинице')
        bot.register_next_step_handler(msg, surname_step)
        return
    msg = bot.send_message(message.chat.id, "Напишите имя на латинице")
    bot.register_next_step_handler(msg, teacher_name_step)


def teacher_name_step(message):
    if message.text == '/start' or message.text == '/certificate':
        bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
        return
    global surname
    surname = message.text
    if not check_string(surname):
        msg = bot.send_message(message.chat.id, 'Попробуйте снова. Имя должно быть на латинице')
        bot.register_next_step_handler(msg, teacher_name_step)
        return
    teachers_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for i in teachers_names:
        cur = KeyboardButton(i)
        teachers_markup.add(cur)
    msg = bot.reply_to(message, 'Выберите имя учителя', reply_markup=teachers_markup)
    print(msg)
    bot.register_next_step_handler(msg, course_name_step)


def course_name_step(message):
    if message.text == '/start' or message.text == '/certificate':
        bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
        return
    course_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    global teacher
    teacher = message.text
    for i in course_names:
        cur = KeyboardButton(i)
        course_markup.add(cur)
    msg = bot.reply_to(message, 'Выберите курс', reply_markup=course_markup)
    bot.register_next_step_handler(msg, image_giving_step)


def image_giving_step(message):
    global course
    course = message.text
    font_size = 72
    border = 2595
    x = 1470
    y = 1065
    tx = 2165
    ty = 1860
    course1x = 1435
    course1y = 1305
    tfont_size = font_size//2
    while x + max(len(name), len(surname)) * font_size > border:
        font_size -= 2
    image = Image.open('cert.png')
    font = ImageFont.truetype("font-m.ttf", font_size)
    draw = ImageDraw.Draw(image)
    draw.text((x, y), name, font=font, fill=(237, 186, 45))
    draw.text((x, y + font_size), surname, font=font, fill=(237, 186, 45))
    draw.text((tx, ty), teacher, font=ImageFont.truetype("font-b.ttf", tfont_size+20), fill=(0, 0, 0))
    draw.text((course1x, course1y - 30), "as having successfully completed the",
              font=ImageFont.truetype("font-m.ttf", tfont_size+15), fill=(0, 0, 0))
    draw.text((course1x, course1y + tfont_size), course,
              font=ImageFont.truetype("font-r.ttf", tfont_size+15), fill=(0, 0, 0))
    draw.text((course1x, course1y + tfont_size*2 + 30), "offline course",
              font=ImageFont.truetype("font-m.ttf", tfont_size+15), fill=(0, 0, 0))

    # подпись училки
    sign_img = Image.open(sign_path + signatures[teachers_names.index(teacher)], 'r')
    sign_img = sign_img.resize((300, 300), Image.ANTIALIAS)
    image.paste(sign_img, (2330, 1550), sign_img)

    # подпись владельца
    sign_main_img = Image.open(os.path.join(sign_path, 'c.png'), 'r')
    sign_main_img = sign_main_img.resize((300, 300), Image.ANTIALIAS)
    image.paste(sign_main_img, (1630, 1550), sign_main_img)

    image.save('cur.png')
    bot.send_chat_action(message.chat.id, 'upload_photo')
    img = open('cur.png', 'rb')
    bot.send_document(message.chat.id, img,
                      reply_to_message_id=message.message_id)
    img.close()


@bot.message_handler(commands=['start', 'certificate'])
def send_photo(message):
    if message.text == '/start':
        bot.send_message(message.chat.id, "Напишите /certificate, чтобы получить сертификат")
    if message.text == '/certificate':
        msg = bot.send_message(message.chat.id, "Напишите фамилию на латинице")
        bot.register_next_step_handler(msg, surname_step)


bot.polling(none_stop=True)
