import telebot
import random
import time
from config import TOKEN, questions

bot = telebot.TeleBot(TOKEN)
guesses = []
is_going = 0
rating = {}


@bot.message_handler(commands=['help'])
def start_message(message):

    text = "/start - начать игру, /stop остановить игру"
    bot.reply_to(message, text)


@bot.message_handler(commands=['start'])
def start_viktorina(message):
    global is_going
    global guesses
    is_going = 1

    while is_going:

        guessed = False

        if len(questions)-1:
            pos = random.randrange(0, len(questions))
        else:
            pos = 0
        question = questions[pos]["q"]
        answer = questions[pos]["ans"]
        guess = ""
        player = ""
        playername = ""
        nums = list(range(len(answer)))
        tip = "*" * len(answer)

        bot.send_message(message.chat.id, question)

        while not guessed and nums and is_going:

            bot.send_message(message.chat.id, tip)
            for j in list(range(10)):

                for k in guesses:
                    if k[2] == answer:
                        player = k[0]
                        playername = k[1]
                        guess = k[2]
                        break

                if guess == answer:
                    if player in rating:
                        rating[player][0] += 1
                    else:
                        rating[player] = [1, playername]

                    bot.send_message(message.chat.id, "Правильно!")
                    bot.send_message(message.chat.id, f"{playername}: {rating[player][0]}")
                    guessed = True
                    guesses = []
                    break

                time.sleep(1)

            if len(nums) - 1:
                current_letter = random.randrange(0, len(nums) - 1)
            else:
                current_letter = 0

            tip = tip[:nums[current_letter]] + answer[nums[current_letter]] + tip[nums[current_letter] + 1:]
            nums = nums[:current_letter] + nums[current_letter + 1:]

        if tip == answer and not guessed:
            bot.send_message(message.chat.id, f"Ответ: {tip}")
            guesses = []


@bot.message_handler(commands=['stop'])
def stop_viktorina(message):
    global is_going
    is_going = 0
    bot.reply_to(message, "Пока-пока!")

@bot.message_handler(commands=['rating'])
def show_rating(message):

    if rating:
        sorted_rating = sorted(rating.items(), reverse=True, key=lambda x: x[1][0])
        for i in sorted_rating[:10]:
            bot.send_message(message.chat.id, f"{i[1][1]}: {i[1][0]}")
    else:
        bot.send_message(message.chat.id, f"Здесь пока пусто.")


@bot.message_handler(content_types=['text'])
def answer_message(message):
    global guesses
    guesses.append((message.from_user.id, message.from_user.first_name, message.text.lower()))


bot.polling(none_stop=True)
