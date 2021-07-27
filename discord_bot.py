import discord
import os
import capitals
import cam_math
import cam_eval
from discord.ext import commands
import threading
from discord import File
import random
import datetime
from datetime import datetime
import calendar
from datetime import date
import time
import requests
from PyDictionary import PyDictionary
import math
from pprint import pprint
import asyncio
from tokenstorage import get_token

dictionary = PyDictionary()

# print(dictionary.meaning('indentation')['Noun'])

exitFlag = 0

intents = discord.Intents.default()
client = commands.Bot(command_prefix='+', intents=intents)
current_message_user = ''

def generate_deck():
    suits = ['spades','diamonds','hearts','clubs']
    ranks = [1,2,3,4,5,6,7,8,9,10,'Jack','Queen','King','Ace']

    deckArr = []

    for eachsuit in suits:
        for eachrank in ranks:
            deckArr.append(str(eachrank) + ' of ' + eachsuit.capitalize())
    return deckArr


@client.command(aliases=['remind'])
async def run_reminder(ctx,time,*args):
    reminder = ''.join(args)
    await asyncio.sleep(int(time)*60)
    await ctx.send(reminder)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-------')


@client.event
async def on_connect():
    print("beep..\nboop..\nbeep...\n\nBOT ONLINE\n")


@client.event
async def on_disconnect():
    print("Bot has disconnected..")


@client.command(aliases=['randomten'])
async def _random_number_one_to_ten(ctx):
    numbers = [x for x in range(1, 11)]
    await ctx.send(random.choice(numbers))


@client.listen
async def on_typing(channel, user, when):
    print(user.id)
    if user.id == 520524669565272074:
        await channel.send("id found")


@client.command(aliases=['eval'])
async def _eval(ctx, *args):
    equation = ''.join(args).replace(' ', '')
    print(equation)

    result = cam_eval.do_math(equation)

    if result == None:
        await ctx.send('Format the equation, may be missing signs, make sure there are multiplications attached to all parenthesis ex : 2(1+2) X doesnt work')
    else:
        await ctx.send(result)


@client.command(aliases=['capital'])
async def _capitals(ctx):
    state = capitals.get_random_state(capitals.states)
    await ctx.send('Guess the capital of {}'.format(state))
    Message = await client.wait_for('message', check=lambda message: message.author == ctx.author)
    guess = Message.content
    if guess.lower() == capitals.state_to_capital_dictionary[state].lower():
        await ctx.send("Correct!!!")
    else:
        await ctx.send("Wrong!!")


@client.command(aliases=['primequiz'])
async def _prime_quiz(ctx):
    score = 0
    while(True):
        random_length = random.choice([x for x in range(1, 10)])
        emptystring = ''
        back_digits = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        emptystring += str(random.choice(back_digits))
        for i in range(random_length - 1):
            emptystring += str(random.choice(back_digits))
        emptystring = int(emptystring)
        await ctx.send("Guess if {} is prime -> Answer : Prime \t Composite".format(emptystring))
        res = cam_math.is_prime(emptystring)
        Message = await client.wait_for('message', check=lambda message: message.author == ctx.author)
        if Message.content.lower() == 'prime' and res:
            score += 1
            await ctx.send("The number was prime, and you guessed prime, so you are correct!! [Current Score : {}]".format(score))
        elif Message.content.lower() == 'prime' and not res:
            score -= 1
            await ctx.send("The number was NOT prime, and you guessed prime, so you are wrong!! [Current Score : {}]".format(score))
        elif Message.content.lower() == 'composite' and res:
            score -= 1
            await ctx.send("The number was prime, and you guessed composite, so you are wrong!! [Current Score : {}]".format(score))
        elif Message.content.lower() == 'composite' and not res:
            score += 1
            await ctx.send("The number was not prime, and you guessed composite, so you are correct!! [Current Score : {}]".format(score))
        else:
            await ctx.send("Wrong input, exiting program [Current Score : {}]".format(score))
            break


onMessageSender = ''


@client.event
async def on_message(message):

    await client.process_commands(message)
    # await message.author.send('@'+message.author.name)

    #channel = message.channel

    #if message.content[0] == '+':
    #    await client.process_commands(message)
    #    await channel.send('@{} {}'.format(message.author.id,message.content))

    #if message.author == client.user:
    #    await channel.send('msg2')
        #await channel.send('@{} {}'.format(onMessageSender,message.content))
        #await client.process_commands(message)
    #else:
        #await client.process_commands(message)
    #    await channel.send('msg1')


######################
# SUCCESSFUL @MENTION
######################

@client.command(aliases=['test2'],pass_context=True)
async def test(ctx):
    await ctx.send('Test {}'.format(ctx.message.author.mention))


@client.command(aliases=['numguess', 'guess'])
async def _num_guess(ctx):
    await ctx.send("Guess a number between 1 and 100")
    numbers = [x for x in range(1, 101)]
    random_number = random.choice(numbers)
    boolVar = True
    while boolVar:
        Message = await client.wait_for('message', check=lambda message: message.author == ctx.author)
        guess = int(Message.content)
        if guess > random_number:
            await ctx.send("Guess lower")
            continue
        elif guess < random_number:
            await ctx.send("Guess higher")
            continue
        else:
            boolVar = False
    await ctx.send("You guessed correct!! Computer chose : {}".format(random_number))


@client.command(aliases=['randomint', 'randomnumber', 'random'])
async def _random_generator(ctx):
    random_number = int(random.random() * random.randint(10, 100000))
    await ctx.send("BOT ARMY HAS SPOKEN : \nRANDOM NUMBER IS {}".format(random_number))


@client.command(aliases=['roll', 'diceroll', 'dice'])
async def _dice_roll(ctx):
    rolls = [x for x in range(1, 13)]
    await ctx.send("You rolled : {}".format(random.choice(rolls)))


@client.command(aliases=['alexa', 'amazon'])
async def _alexa_jokes(ctx):
    keys = ["What's John Wayne's favorite holiday?", 'What did the corn say to the butter?']
    adict = {"What's John Wayne's favorite holiday?": 'Thanksgiving, Pilgrim',
             'What did the corn say to the butter?': 'see you on the other side'}
    randomkey = random.choice(keys)
    for i in range(1):
        await ctx.send(randomkey)
        await asyncio.sleep(3)
    await ctx.send(adict[randomkey])


@client.command(aliases=['rock'])
async def _play_rock(ctx):
    results = ['rock', 'rock', 'paper', 'paper', 'scissors', 'scissors']
    random_choice = random.choice(results)
    if random_choice == 'scissors':
        await ctx.send("You won!! Computer chose : scissors")
    elif random_choice == 'paper':
        await ctx.send("You lost!! Computer chose : paper")
    else:
        await ctx.send("Tie!!")


@client.command(aliases=['paper'])
async def _play_paper(ctx):
    results = ['rock', 'rock', 'paper', 'paper', 'scissors', 'scissors']
    random_choice = random.choice(results)
    if random_choice == 'scissors':
        await ctx.send("You lost!! Computer chose : scissors")
    elif random_choice == 'rock':
        await ctx.send("You won!! Computer chose : rock")
    else:
        await ctx.send("Tie!!")


@client.command(aliases=['scissors'])
async def _play_scissors(ctx):
    results = ['rock', 'rock', 'paper', 'paper', 'scissors', 'scissors']
    random_choice = random.choice(results)
    if random_choice == 'rock':
        await ctx.send("You lost!! Computer chose : rock")
    elif random_choice == 'paper':
        await ctx.send("You won!! Computer chose : paper")
    else:
        await ctx.send("Tie!!")


@client.command(aliases=['slots'])
async def _slots(ctx):
    numbers = [x for x in range(1, 8)]
    result = '{}{}{}'.format(random.choice(numbers), random.choice(numbers), random.choice(numbers))
    if result == '777':
        await ctx.send('{} {} YOU WON!'.format(ctx.message.author.mention,result))
    elif result.count('7') == 2:
        await ctx.send('{} {} So close!'.format(ctx.message.author.mention,result))
    elif result.count('7') == 1:
        await ctx.send('{} {} almost..'.format(ctx.message.author.mention,result))
    else:
        await ctx.send('{} {} You lost'.format(ctx.message.author.mention,result))


@client.command(aliases=['draw'])
async def _draw_card(ctx):
    cards = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']
    suits = ['clubs', 'hearts', 'spades', 'diamonds']
    await ctx.send('{} of {}'.format(random.choice(cards), random.choice(suits)))


@client.command(aliases=['table'])
async def _table_flip(ctx):
    await ctx.send("(╯°□°)╯︵ ┻━┻")


@client.command(aliases=['angry'])
async def _sad_face(ctx):
    await ctx.send("ಠ ∩ ಠ")


@client.command(aliases=['shrug'])
async def _shrug_(ctx):
    await ctx.send("¯\_(ツ)_/¯")


@client.command(aliases=['punch'])
async def _punch_(ctx):
    await ctx.send("Take this! 👊")


@client.command(aliases=['farm'])
async def _show_farm(ctx):
    await ctx.send(file=discord.File("C:\\Users\\flyin\\Desktop\\farm.PNG"))


@client.command(aliases=['blackjack'])
async def _black_jack(ctx):
    cards = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']
    suits = ['diamonds', 'clubs', 'spades', 'hearts']
    yourfirstAce = False
    dealerFirstAce = False
    gameOver = False

    ###
    await ctx.send("Welcome to blackjack!")
    your_total = 0
    dealer_total = 0

    card_dictionary = {'J': 11, 'Q': 12, 'K': 13}
    while not gameOver:
        card = draw_card(cards)
        await ctx.send(
            "Card is : {} of {}\n Your total : {} , dealer total : {}".format(card, random.choice(suits), your_total,
                                                                              dealer_total))
        if card == 'A':
            await ctx.send(
                "Dealer received first Ace: {}\n You received first Ace: {}".format(dealerFirstAce, yourfirstAce))
        await ctx.send("Hit or Wait or Pass?")
        Message = await client.wait_for('message', check=lambda message: message.author == ctx.author)
        if Message.content.lower() == 'hit':
            print(card)
            if card == 'A' and not yourfirstAce:
                your_total += 11
                yourFirstAce = True
                if your_total == 21:
                    gameOver = True
                    await ctx.send("YOU WON!! : your_total {}".format(your_total))
                elif your_total > 21:
                    gameOver = True
                    await ctx.send("YOU LOST : your total {}".format(your_total))
                else:
                    await ctx.send('Your total : {}, dealers total : {}'.format(your_total, dealer_total))
                    continue
            elif card == 'A' and yourFirstAce:
                your_total += 1
                if your_total == 21:
                    gameOver = True
                    await ctx.send("YOU WON!! : your_total {}".format(your_total))
                elif your_total > 21:
                    gameOver = True
                    await ctx.send("YOU LOST : your total {}".format(your_total))
                else:
                    await ctx.send('Your total : {}, dealers total : {}'.format(your_total, dealer_total))
                    continue
            elif card in card_dictionary.keys():
                your_total += card_dictionary[card]
                if your_total == 21:
                    gameOver = True
                    await ctx.send("YOU WON!! : your_total {}".format(your_total))
                elif your_total > 21:
                    gameOver = True
                    await ctx.send("YOU LOST : your total {}".format(your_total))
                else:
                    await ctx.send('Your total : {}, dealers total : {}'.format(your_total, dealer_total))
                    continue
            else:
                your_total += card
                if your_total == 21:
                    gameOver = True
                    await ctx.send("YOU WON!! : your_total {}".format(your_total))
                elif your_total > 21:
                    gameOver = True
                    await ctx.send("YOU LOST : your total {}".format(your_total))
                else:
                    await ctx.send('Your total : {}, dealers total : {}'.format(your_total, dealer_total))
                    continue
        elif Message.content.lower() == 'wait':
            if card == 'A' and not dealerFirstAce:
                dealer_total += 11
                dealerFirstAce = True
                if dealer_total == 21:
                    gameOver = True
                    await ctx.send("YOU LOST!! DEALER REACHED 21")
                elif dealer_total > 21:
                    gameOver = True
                    await ctx.send("YOU WON!! DEALER OVER 21")
                else:
                    await ctx.send("Your total : {}, dealers total : {}".format(your_total, dealer_total))
                    continue
            elif card == 'A' and dealerFirstAce:
                dealer_total += 1
                if dealer_total == 21:
                    gameOver = True
                    await ctx.send("YOU LOST!! DEALER REACHED 21")
                elif dealer_total > 21:
                    gameOver = True
                    await ctx.send("YOU WON!! DEALER OVER 21")
                else:
                    await ctx.send("Your total : {}, dealers total : {}".format(your_total, dealer_total))
                    continue
            elif card in card_dictionary.keys():
                dealer_total += card_dictionary[card]
                if dealer_total == 21:
                    gameOver = True
                    await ctx.send("YOU LOST!! DEALER REACHED 21")
                elif dealer_total > 21:
                    gameOver = True
                    await ctx.send("YOU WON!! DEALER OVER 21")
                else:
                    await ctx.send("Your total : {}, dealers total : {}".format(your_total, dealer_total))
                    continue
            else:
                dealer_total += card
                if dealer_total == 21:
                    gameOver = True
                    await ctx.send("YOU LOST!! DEALER REACHED 21")
                elif dealer_total > 21:
                    gameOver = True
                    await ctx.send("YOU WON!! DEALER OVER 21")
                else:
                    await ctx.send("Your total : {}, dealers total : {}".format(your_total, dealer_total))
                    continue
        else:
            continue


def draw_card(card_list):
    return random.choice(card_list)


# @client.command(aliases = ['roll','diceroll'])
# async def _dice_roll(ctx,max_num_of_dice):
#    rolls = [x for x in range(1,int(max_num_of_dice)+1)]
#    await ctx.send("You rolled : {}".format(random.choice(rolls)))

@client.command(aliases=['isprime', 'prime?', 'primality', 'prime', 'primecheck'])
async def _is_prime(ctx, is_prime_number):
    number = int(is_prime_number)
    if number > 0 and number < 4:
        await ctx.send("YES {}".format(number))
        return ''
    else:
        if number % 2 == 0 or number % 3 == 0 or number % 5 == 0:
            await ctx.send("NO {}".format(number))
            return ''
        for i in range(2, int(math.sqrt(number))):
            if number % i == 0:
                await ctx.send("NO {}".format(number))
                return ''
        await ctx.send("YES {}".format(number))


@client.command(aliases=['def', 'definition', 'meaning'])
async def _find_definition(ctx, word):
    try:
        the_word = dictionary.meaning(word)
        await ctx.send(
            str(dictionary.meaning(word)).replace('{', '').replace('}', '').replace('[', '').replace(']', ''))
    except Exception as ex:
        await ctx.send("ERROR : INVALID WORD")


@client.command(aliases=['foo'])
async def _foo(ctx):
    await ctx.send("Foo")


@client.command(aliases=[''])
async def _function(ctx):
    await ctx.send("Nothing")


def is_flush(hand:[str])->[int]:

    suits = []

    if len(hand) < 5:
        print('Not enough cards to make a flush combination possible')
        return False

    maxSuit = ''

    for eachcard in hand:
        suit = eachcard.split(' ')[2]
        suits.append(suit)

    theCards = []
    ranks = {'Jack': 11, 'Queen': 12, 'King': 13, 'Ace': 14}


    for eachsuit in suits:
        if suits.count(eachsuit) == 5:
            maxSuit = eachsuit
            for eachcard in hand:
                suit = eachcard.split(' ')[2]
                rank = eachcard.split(' ')[0]
                if suit == maxSuit:
                    try:
                        rank = int(rank)
                    except Exception as e:
                        rank = ranks[rank]
                    theCards.append(rank)
            return theCards if len(theCards) > 0 else [-1]
    return [-1]

def is_straight(hand:[str])->[int]:

    ranks = []

    #suits = ['spades','diamonds','hearts','clubs']
    #ranks = [1,2,3,4,5,6,7,8,9,10,'Jack','Queen','King','Ace']

    #for eachsuit in suits:
    #    for eachrank in ranks:
    #        deckArr.append(str(eachrank) + ' of ' + eachsuit.capitalize())
    #return deckArr

    if len(hand) < 5:
        print('Not enough cards to make a straight combination possible')
        return False

    special_ranks = {'Jack': 11,'Queen': 12,'King': 13,'Ace': 14}

    for eachcard in hand:
        split_hand = eachcard.split(' ')
        rank = split_hand[0]
        try:
            rank = int(rank)
        except Exception as e:
            rank = special_ranks[rank]
        ranks.append(rank)

    distinct_ranks = []

    for eachrank in ranks:
        if eachrank not in distinct_ranks:
            distinct_ranks.append(eachrank)

    ct = 0

    theMax = 0

    for i in range(len(distinct_ranks)-4):
        for j in range(len(distinct_ranks)-1):
          if abs(distinct_ranks[j+1] - distinct_ranks[j]) == 1 or ((distinct_ranks[j+1] == 14 and distinct_ranks[j] == 1) or (distinct_ranks[j+1] == 1 and distinct_ranks[j] == 14)):
            ct += 1
            theMax = max(theMax,distinct_ranks[j+1])
          else:
            ct = 0
            theMax = 0
            break
        if ct == 4:
            return theMax
    return [-1]

def royal_flush(hand):

    cards = []

    for eachcard in hand:
        if 'Jack' in eachcard or 'Queen' in eachcard or 'King' in eachcard or 'Ace' in eachcard:
            cards.append(eachcard)

    if len(cards) >= 5:
        suits = []
        for eachcard in cards:
            suit = eachcard.split(' ')[2]
            if suit not in suits:
                suits.append(suit)

        pairs = []
        for eachsuit in suits:
            for eachcard in cards:
                if eachsuit in eachcard: ## check if suit is in eachcard
                    if eachcard not in pairs: ## check if eachcard is not in pairs
                        pairs.append(eachcard)
            if len(pairs) == 5:
                return True
            else:
                pairs = []
        return False
    else:
        return False




def poker_combos(hand):

    if is_straight(hand) != [-1]:
        return False
    elif is_flush(hand) != [1]:
        return False




@client.command(aliases=['poker'])
async def _poker(ctx):
    deck = generate_deck()



"""
@client.command(aliases=['remind'])
async def _remind(ctx, the_time, *args):
    the_message = ' '.join(args)
    the_time = float(the_time) * 60
    while the_time > 60:
        time.sleep(60)
        the_time -= 60
    time.sleep(the_time)
    await ctx.send('@{} , here is your reminder : {}'.format(ctx.message.author.name, the_message))
"""

@client.command(aliases=['add'])
async def _add(ctx, num1, num2):
    await ctx.send(int(num1) + int(num2))


@client.command(aliases=['multiply', 'mul', 'times'])
async def _mul(ctx, num1, num2):
    await ctx.send(int(num1) * int(num2))


@client.command(aliases=['today', 'now'])
async def _today(ctx):
    today = date.today()
    await ctx.send(today)


@client.command(aliases=['joke', 'pun'])
async def _joke(ctx):
    joke_list = ['What’s the best thing about Switzerland? I don’t know, but the flag is a big plus.',
                 'I invented a new word! Plagiarism!', 'Where does the General keep his armies? In his sleevies.',
                 'How does a squid go into battle? Well-armed.',
                 'What\'s the best thing about Switzerland? I don\'t know, but their flag is a huge plus.',
                 'Where do you find a cow with no legs? Right where you left it.',
                 'Why aren\'t koalas actual bears? They don\'t meet the koalafications.',
                 'A bear walks into a restaurant. He tells his waiter, \"I want a grilled …. cheese.\" The waiter says, \"What\'s with the pause?\" "Whaddya mean?\" the bear replies. \"I\'m a bear!\"',
                 'What\'s E.T. short for? Because he\'s only got little legs.',
                 'What do you call a Frenchman wearing sandals? Phillipe Phillope',
                 'What\'s the difference between a hippo and a zippo? One is really heavy, and the other is a little lighter.',
                 'What do Alexander the Great and Winnie the Pooh have in common? Same middle name.',
                 'What did the mayonnaise say when the refrigerator door was opened? Close the door, I\'m dressing.',
                 '"I stand corrected!" Said the man in the orthopedic shoes.',
                 'I used to be addicted to soap. But I\'m clean now.',
                 'What did the left eye say to the right eye? Between you and me, something smells.',
                 'Why is England the wettest country? Because the queen has reigned there for years.',
                 'It\'s hard to explain puns to kleptomaniacs. They always take things so literally.',
                 'What do you call it when Batman skips church? Christian Bale.']
    await ctx.send(random.choice(joke_list))


# @bot.event
# async def on_message(message):
#    if message.content.startswith("foo"):
#        await bot.send_message(message_channel, "THIS WORKED")
#    await bot.process_commands(message)

@client.command()
async def ping(ctx):
    await ctx.send('Pong! Also I am running at {} ms.'.format(round(client.latency * 100)))


@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = ['It is certain.', 'It is decidely so', 'Without a doubt.', 'Yes - definitely', 'You may rely on it',
                 'As I see it, yes', 'Most likely', 'Outlook good.', 'Yes.', 'Signs point to yes.',
                 'Reply hazy, try again',
                 'Ask again later.', 'Better not tell you now', 'What did you just say???', 'Ya right', 'Yes Indeed', ]
    await ctx.send('Question: {}\n Answer: {}'.format(question, random.choice(responses)))


@client.command(aliases=['WeezyF', 'WEEZYF', 'WEEZY'])
async def drake_lyrics(ctx):
    await ctx.send("YOUNG MONEY MILITIA")


@client.command(aliases=['russianroulette'])
async def russian_roulette(ctx):
    alist = ['blank', 'blank', 'bullet', 'blank', 'blank', 'blank']
    if random.choice(alist) == 'bullet':
        await ctx.send('BANG!! YOU DED')
    else:
        await ctx.send('YOU ALIVE')

@client.command(aliases=['gofish'])
async def go_fish(ctx):
    return None

client.run(get_token()) ## make sure to delete before committing