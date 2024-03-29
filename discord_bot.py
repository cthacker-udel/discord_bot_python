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
import bs4
import selenium.webdriver
from webdriver_manager.microsoft import IEDriverManager as InternetExplorerDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager as EdgeDriverManager
from webdriver_manager.opera import OperaDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager as FirefoxDriverManager
import pymongo
from tokenstorage import get_conn_string


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


@client.command(aliases=['script'])
async def get_script(ctx):
    return None


@client.command(aliases=['ready'])
async def is_ready(ctx):

    if client.is_ready():
        await ctx.send('{} The bot {} is ready to receive requests!'.format(ctx.message.author.mention,client.user.display_name))
    else:
        await ctx.send('{} The bot {} is not ready to receive requests!'.format(ctx.message.author.mention,client.user.display_name))




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
    random.seed(time.time() * 1000)
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
        try:
            guess = int(Message.content)
        except Exception as e:
            continue
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
    await ctx.send("{} You rolled : {}".format(ctx.message.author.mention,random.choice(rolls)))


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
        await ctx.send("{} You won!! Computer chose : scissors".format(ctx.message.author.mention))
    elif random_choice == 'paper':
        await ctx.send("{} You lost!! Computer chose : paper".format(ctx.message.author.mention))
    else:
        await ctx.send("Tie!!")


@client.command(aliases=['paper'])
async def _play_paper(ctx):
    results = ['rock', 'rock', 'paper', 'paper', 'scissors', 'scissors']
    random_choice = random.choice(results)
    if random_choice == 'scissors':
        await ctx.send("{} You lost!! Computer chose : scissors".format(ctx.message.author.mention))
    elif random_choice == 'rock':
        await ctx.send("{} You won!! Computer chose : rock".format(ctx.message.author.mention))
    else:
        await ctx.send("Tie!!")


@client.command(aliases=['scissors'])
async def _play_scissors(ctx):
    results = ['rock', 'rock', 'paper', 'paper', 'scissors', 'scissors']
    random_choice = random.choice(results)
    if random_choice == 'rock':
        await ctx.send("{} You lost!! Computer chose : rock".format(ctx.message.author.mention))
    elif random_choice == 'paper':
        await ctx.send("{} You won!! Computer chose : paper".format(ctx.message.author.mention))
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

"""
#Deprecated
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
"""


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


def is_three_of_a_kind(hand):

    adict = {}

    for eachcard in hand:
        rank = eachcard.split(' ')[0]
        if rank in adict:
            adict[rank] = adict[rank] + 1
        else:
            adict[rank] = 1


    for eachkey in adict.keys():
        if adict[eachkey] == 3:
            return True
    return False

def get_three_of_a_kind_cards(hand):

    adict = {}

    for eachcard in hand:
        rank = eachcard.split(' ')[0]
        if rank in adict:
            adict[rank] = adict[rank] + 1
        else:
            adict[rank] = 1
    for eachkey in adict.keys():
        if adict[eachkey] == 3:
            return eachkey


def is_two_pair(hand):

    adict = {}

    for eachcard in hand:
        rank = eachcard.split(' ')[0]
        if rank in adict:
            adict[rank] = adict[rank] + 1
        else:
            adict[rank] = 1

    found_pair = False
    for eachkey in adict.keys():
        if adict[eachkey] == 2 and not found_pair:
            found_pair = True
        elif found_pair and adict[eachkey] == 2:
            return True
    return False

def get_two_pair_cards(hand):

    cards = []

    adict = {}

    for eachcard in hand:
        rank = eachcard.split(' ')[0]
        if rank in adict:
            adict[rank] = adict[rank] + 1
        else:
            adict[rank] = 1

    found_pair = False
    for eachkey in adict.keys():
        if adict[eachkey] == 2 and not found_pair:
            found_pair = True
            cards.append(eachkey)
        elif found_pair and adict[eachkey] == 2:
            cards.append(eachkey)
            return cards
    return []


def is_one_pair(hand):

    adict = {}

    for eachcard in hand:
        rank = eachcard.split(' ')[0]
        if rank in adict:
            adict[rank] = adict[rank] + 1
        else:
            adict[rank] = 1


    for eachkey in adict.keys():
        if adict[eachkey] == 2:
            return True
    return False

def get_one_pair_cards(hand):
    adict = {}

    for eachcard in hand:
        rank = eachcard.split(' ')[0]
        if rank in adict:
            adict[rank] = adict[rank] + 1
        else:
            adict[rank] = 1

    for eachkey in adict.keys():
        if adict[eachkey] == 2:
            return eachkey
    return False

def high_card(hand):

    misc_ranks = {'Jack': 11, 'Queen': 12, 'King': 13, 'Ace': 14}
    rank_list = []

    for eachcard in hand:
        rank = eachcard.split(' ')[0]
        if rank in misc_ranks.keys():
            rank_list.append(misc_ranks[rank])
        else:
            rank_list.append(int(rank))

    return max(rank_list)

def deal_high_card(hand):

    misc_ranks = {'Jack': 11, 'Queen': 12, 'King': 13, 'Ace': 14}
    rank_list = []

    rank = 0
    for eachcard in hand:
        try:
            rank = eachcard.split(' ')[0]
            if rank in misc_ranks.keys():
                rank_list.append(misc_ranks[rank])
            else:
                rank_list.append(int(rank))
        except Exception as e:
            rank_list.append(rank)

    max_card = max(rank_list)

    for i in range(len(hand)):
        try:
            rank = hand[i].split(' ')[0]
            if rank in misc_ranks.key() and misc_ranks[rank] == max_card:
                del hand[i]
                return misc_ranks[rank],hand
            elif int(rank) == max_card:
                del hand[i]
                return rank,hand
        except Exception as e:
            continue
    return max_card,hand


def is_flush(hand:[str])->[int]:

    suits = []

    if len(hand) < 5:
        print('Not enough cards to make a flush combination possible')
        return [-1]

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
            ### flush already returns cards
    return [-1]

def deal(hand):

    card = hand[-1]
    hand = hand[:-1]
    return card,hand

def shuffle(hand):
    indexes = [x for x in range(0,len(hand))]
    new_hand = []

    for i in range(len(hand)):
        index_chosen = random.choice(indexes)
        indexes.remove(index_chosen)
        new_hand.append(hand[index_chosen])
    return new_hand


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
        return [-1]

    special_ranks = {'Jack': 11,'Queen': 12,'King': 13,'Ace': 14}

    for eachcard in hand:
        split_hand = eachcard.split(' ')
        rank = split_hand[0]
        try:
            rank = int(rank)
        except Exception as e:
            rank = special_ranks[rank]
        ranks.append(rank)

    ranks = sorted(ranks)

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


def get_straight_cards(hand):

    cards = []

    ranks = []

    # suits = ['spades','diamonds','hearts','clubs']
    # ranks = [1,2,3,4,5,6,7,8,9,10,'Jack','Queen','King','Ace']

    # for eachsuit in suits:
    #    for eachrank in ranks:
    #        deckArr.append(str(eachrank) + ' of ' + eachsuit.capitalize())
    # return deckArr

    if len(hand) < 5:
        print('Not enough cards to make a straight combination possible')
        return False

    special_ranks = {'Jack': 11, 'Queen': 12, 'King': 13, 'Ace': 14}

    for eachcard in hand:
        split_hand = eachcard.split(' ')
        rank = split_hand[0]
        try:
            rank = int(rank)
        except Exception as e:
            rank = special_ranks[rank]
        ranks.append(rank)

    ranks = sorted(ranks)

    distinct_ranks = []

    for eachrank in ranks:
        if eachrank not in distinct_ranks:
            distinct_ranks.append(eachrank)

    ct = 0

    for i in range(len(distinct_ranks) - 4):
        for j in range(len(distinct_ranks) - 1):
            if abs(distinct_ranks[j + 1] - distinct_ranks[j]) == 1 or (
                    (distinct_ranks[j + 1] == 14 and distinct_ranks[j] == 1) or (
                    distinct_ranks[j + 1] == 1 and distinct_ranks[j] == 14)):
                ct += 1
                if distinct_ranks[j] not in cards:
                    cards.append(distinct_ranks[j])
                if distinct_ranks[j+1] not in cards:
                    cards.append(distinct_ranks[j+1])
            else:
                ct = 0
                cards = []
                break
        if ct == 4:
            return cards
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


def is_four_of_a_kind(hand):

    adict = {}

    for eachcard in hand:
        rank = eachcard.split(' ')[0]
        if rank in adict.keys():
            adict[rank] = adict[rank] + 1
        else:
            adict[rank] = 1

    for eachkey in adict.keys():
        if adict[eachkey] == 4:
            return True
    return False

def get_four_of_a_kind_cards(hand):

    adict = {}

    cards = []

    for eachcard in hand:
        rank = eachcard.split(' ')[0]
        if rank in adict.keys():
            adict[rank] = adict[rank] + 1
        else:
            adict[rank] = 1

    for eachkey in adict.keys():
        if adict[eachkey] == 4:
            cards.append(eachkey)
            return cards
    return []

def is_full_house(hand):

    adict = {}

    for eachcard in hand:
        rank = eachcard.split(' ')[0]
        if rank in adict.keys():
            adict[rank] = adict[rank] + 1
        else:
            adict[rank] = 1

    found_three = False
    found_two = False

    for eachkey in adict.keys():
        if adict[eachkey] == 3:
            found_three = True
        elif adict[eachkey] == 2:
            found_two = True
    return found_three and found_two

def get_full_house_cards(hand):

    cards = []

    adict = {}

    for eachcard in hand:
        rank = eachcard.split(' ')[0]
        if rank in adict.keys():
            adict[rank] = adict[rank] + 1
        else:
            adict[rank] = 1

    found_three = False
    found_two = False

    for eachkey in adict.keys():
        if adict[eachkey] == 3:
            cards.append(eachkey)
            found_three = True
        elif adict[eachkey] == 2:
            cards.append(eachkey)
            found_two = True
    return cards


def poker_combos(hand):

    if royal_flush(hand):
        return 9
    if is_straight(hand) != [-1] and is_flush(hand) != [-1]:
        return 8 ## straight flush
    if is_four_of_a_kind(hand):
        return 7 ## four of a kind
    if is_full_house(hand):
        return 6
    elif is_flush(hand) != [-1]:
        return 5
    elif is_straight(hand) != [-1]:
        return 4
    elif is_three_of_a_kind(hand):
        return 3
    elif is_two_pair(hand):
        return 2
    elif is_one_pair(hand):
        return 1
    else:
        return [high_card(hand)] ## check if type of return is type(var) == [] to assert if high card value has been assesed

def showdown(player_hand,computer_hand):

    player_strength = poker_combos(player_hand)
    computer_strength = poker_combos(computer_hand)
    player_cards = []
    computer_cards = []

    print('entered showdown function')

    if type(player_strength) == type([]) and type(computer_strength) == type([]):
        print('entered 1st if --- both have high cards')
        player_high_card = ''
        computer_high_card = ''
        while len(player_hand) > 0:
            player_high_card, player_hand = deal_high_card(player_hand)
            computer_high_card, computer_hand = deal_high_card(computer_hand)
            if player_high_card > computer_high_card:
                return 1
            elif computer_high_card > player_high_card:
                return 2
            else:
                player_high_card, player_hand = deal_high_card(player_hand)
                computer_high_card, computer_hand = deal_high_card(computer_hand)
        if player_high_card > computer_high_card:
            return 1
        elif computer_high_card > player_high_card:
            return 2
        else:
            return 3
    elif type(player_strength) == type([]) and type(computer_strength) != type([]):
        print('entered 2 if')
        return 2
    elif type(player_strength) != type([]) and type(computer_strength) == type([]):
        print('entered 3 if')
        return 1

    ## 1 - player win
    ## 2 - computer win
    ## 3 - tie

    if player_strength > computer_strength:
        return 1
    elif computer_strength > player_strength:
        return 2
    else:
        if player_strength == 9 and computer_strength == 9:
            print('entered 4 if')
            return 3
        elif player_strength == 8 and computer_strength == 8:
            print('entered 5 if')
            player_cards = get_straight_cards(player_hand)
            computer_cards = get_straight_cards(computer_hand)
            player_high_card,player_cards = deal_high_card(player_cards)
            computer_high_card,computer_cards = deal_high_card(computer_cards)
            while len(player_cards) > 0:
                if player_high_card > computer_high_card:
                    return 1
                elif computer_high_card > player_high_card:
                    return 2
                else:
                    player_high_card,player_cards = deal_high_card(player_cards)
                    computer_high_card,computer_cards = deal_high_card(computer_cards)
            while len(player_hand) > 0:
                player_high_card,player_hand = deal_high_card(player_hand)
                computer_high_card,computer_hand = deal_high_card(computer_hand)
                if player_high_card > computer_high_card:
                    return 1
                elif computer_high_card > player_high_card:
                    return 2
                else:
                    player_high_card,player_hand = deal_high_card(player_hand)
                    computer_high_card,computer_hand = deal_high_card(computer_hand)
            if player_high_card > computer_high_card:
                return 1
            elif computer_high_card > player_high_card:
                return 2
            else:
                return 3
        elif player_strength == 7 and computer_strength == 7:
            print('entered 6 if')
            player_card = get_four_of_a_kind_cards(player_hand)
            computer_card = get_four_of_a_kind_cards(computer_hand)
            if player_card > computer_card:
                return 1
            elif player_card < computer_card:
                return 2
            else:
                player_high_card = ''
                computer_high_card = ''
                while len(player_hand) > 0:
                    player_high_card,player_hand = deal_high_card(player_hand)
                    computer_high_card,computer_hand = deal_high_card(computer_hand)
                    if player_high_card > computer_high_card:
                        return 1
                    elif computer_high_card > player_high_card:
                        return 2
                    else:
                        player_high_card, player_hand = deal_high_card(player_hand)
                        computer_high_card, computer_hand = deal_high_card(computer_hand)
                if player_high_card > computer_high_card:
                    return 1
                elif computer_high_card > player_high_card:
                    return 2
                else:
                    return 3
        elif player_strength == 6 and computer_strength == 6:
            print('entered 7 if')
            player_cards = get_full_house_cards(player_hand)
            computer_cards = get_full_house_cards(computer_hand)
            if max(player_cards) > max(computer_cards):
                return 1
            elif max(computer_cards) > max(player_cards):
                return 2
            elif min(player_cards) > min(computer_cards):
                return 1
            elif min(computer_cards) > min(player_cards):
                return 2
            else:
                player_high_card = ''
                computer_high_card = ''
                while len(player_hand) > 0:
                    player_high_card, player_hand = deal_high_card(player_hand)
                    computer_high_card, computer_hand = deal_high_card(computer_hand)
                    if player_high_card > computer_high_card:
                        return 1
                    elif computer_high_card > player_high_card:
                        return 2
                    else:
                        player_high_card, player_hand = deal_high_card(player_hand)
                        computer_high_card, computer_hand = deal_high_card(computer_hand)
                if player_high_card > computer_high_card:
                    return 1
                elif computer_high_card > player_high_card:
                    return 2
                else:
                    return 3
        elif player_strength == 5 and computer_strength == 5:
            print('entered 8 if')
            player_cards = is_flush(player_hand)
            computer_cards = is_flush(computer_hand)
            if max(player_cards) > max(computer_cards):
                return 1
            elif max(computer_cards) > max(player_cards):
                return 2
            else:
                ## cycle through player_cards
                player_high_card = ''
                computer_high_card = ''
                while len(player_cards) > 0:
                    player_high_card,player_cards = deal_high_card(player_cards)
                    computer_high_card,computer_cards = deal_high_card(computer_cards)
                    if player_high_card > computer_high_card:
                        return 1
                    elif computer_high_card > player_high_card:
                        return 2
                    else:
                        player_high_card, player_cards = deal_high_card(player_cards)
                        computer_high_card, computer_cards = deal_high_card(computer_cards)
                if player_high_card > computer_high_card:
                    return 1
                elif computer_high_card > player_high_card:
                    return 2
                else:
                    player_high_card = ''
                    computer_high_card = ''
                    while len(player_hand) > 0:
                        player_high_card, player_hand = deal_high_card(player_hand)
                        computer_high_card, computer_hand = deal_high_card(computer_hand)
                        if player_high_card > computer_high_card:
                            return 1
                        elif computer_high_card > player_high_card:
                            return 2
                        else:
                            player_high_card, player_hand = deal_high_card(player_hand)
                            computer_high_card, computer_hand = deal_high_card(computer_hand)
                    if player_high_card > computer_high_card:
                        return 1
                    elif computer_high_card > player_high_card:
                        return 2
                    else:
                        return 3
        elif player_strength == 4 and computer_strength == 4:
            print('entered 9 if')
            player_cards = get_straight_cards(player_hand)
            computer_cards = get_straight_cards(computer_hand)
            player_high_card = ''
            computer_high_card = ''
            while len(player_cards) > 0:
                player_high_card,player_cards = deal_high_card(player_cards)
                computer_high_card,computer_cards = deal_high_card(computer_cards)
                if player_high_card > computer_high_card:
                    return 1
                elif computer_high_card > player_high_card:
                    return 2
                else:
                    player_high_card, player_cards = deal_high_card(player_cards)
                    computer_high_card, computer_cards = deal_high_card(computer_cards)
            if player_high_card > computer_high_card:
                return 1
            elif computer_high_card > player_high_card:
                return 2
            else:
                while len(player_hand) > 0:
                    player_high_card, player_hand = deal_high_card(player_hand)
                    computer_high_card, computer_hand = deal_high_card(computer_hand)
                    if player_high_card > computer_high_card:
                        return 1
                    elif computer_high_card > player_high_card:
                        return 2
                    else:
                        player_high_card, player_hand = deal_high_card(player_hand)
                        computer_high_card, computer_hand = deal_high_card(computer_hand)
                if player_high_card > computer_high_card:
                    return 1
                elif computer_high_card > player_high_card:
                    return 2
                else:
                    return 3
        elif player_strength == 3 and computer_strength:
            print('entered 10 if')
            player_card = get_three_of_a_kind_cards(player_hand)
            computer_card = get_three_of_a_kind_cards(computer_hand)
            if player_card > computer_card:
                return 1
            elif computer_card > player_card:
                return 2
            else:
                player_high_card = ''
                computer_high_card = ''
                while len(player_hand) > 0:
                    player_high_card, player_hand = deal_high_card(player_hand)
                    computer_high_card, computer_hand = deal_high_card(computer_hand)
                    if player_high_card > computer_high_card:
                        return 1
                    elif computer_high_card > player_high_card:
                        return 2
                    else:
                        player_high_card, player_hand = deal_high_card(player_hand)
                        computer_high_card, computer_hand = deal_high_card(computer_hand)
                if player_high_card > computer_high_card:
                    return 1
                elif computer_high_card > player_high_card:
                    return 2
                else:
                    return 3
        elif player_strength == 2 and computer_strength == 2:
            print('entered 11 if')
            player_cards = get_two_pair_cards(player_hand)
            computer_cards = get_two_pair_cards(computer_hand)
            if max(player_cards) > max(computer_cards):
                return 1
            elif max(computer_cards) > max(player_cards):
                return 2
            elif min(player_cards) > min(computer_cards):
                return 1
            elif min(computer_cards) > min(player_cards):
                return 2
            else:
                player_high_card = ''
                computer_high_card = ''
                while len(player_hand) > 0:
                    player_high_card, player_hand = deal_high_card(player_hand)
                    computer_high_card, computer_hand = deal_high_card(computer_hand)
                    if player_high_card > computer_high_card:
                        return 1
                    elif computer_high_card > player_high_card:
                        return 2
                    else:
                        player_high_card, player_hand = deal_high_card(player_hand)
                        computer_high_card, computer_hand = deal_high_card(computer_hand)
                if player_high_card > computer_high_card:
                    return 1
                elif computer_high_card > player_high_card:
                    return 2
                else:
                    return 3
        elif player_strength == 1 and computer_strength == 1:
            print('entered 12 if')
            player_card = get_one_pair_cards(player_hand)
            computer_card = get_one_pair_cards(computer_hand)
            if player_card > computer_card:
                return 1
            elif computer_card > player_card:
                return 2
            else:
                player_high_card = ''
                computer_high_card = ''
                while len(player_hand) > 0:
                    player_high_card, player_hand = deal_high_card(player_hand)
                    computer_high_card, computer_hand = deal_high_card(computer_hand)
                    if player_high_card > computer_high_card:
                        return 1
                    elif computer_high_card > player_high_card:
                        return 2
                    else:
                        player_high_card, player_hand = deal_high_card(player_hand)
                        computer_high_card, computer_hand = deal_high_card(computer_hand)
                if player_high_card > computer_high_card:
                    return 1
                elif computer_high_card > player_high_card:
                    return 2
                else:
                    return 3





async def display_table_cards(ctx,hand):
    await ctx.send('#########################################################\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tTABLE CARDS\n#########################################################\n{}\n#########################################################'.format(hand))

async def display_player_hand(ctx,hand):

    await ctx.send('-----------------------------------------------------------------------------------------------------\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tPLAYER HAND\n-----------------------------------------------------------------------------------------------------\n{}\n-----------------------------------------------------------------------------------------------------'.format(hand))

@client.command(aliases=['poker'])
async def _poker(ctx):
    #print('----- displaying poker -----')
    #global player_chips
    await ctx.send('----starting poker game----')
    #deck = generate_deck()
    #for i in range(7):
    #    deck = shuffle(deck)

    """
    
    Steps :
    1) Generate Player Hand
    2) Generate Computer Hand
    3) Generate Table Hand
    4) Ask for bets
    5) Ask Player to either fold,call,or raise
    6) Depending on answer, computer chooses at random, [skewed to call or raise more then fold, 
    fold will either be if computer analyses it's hand and players hand, and the computer's hand is less, and the number it generates
    is odd, then it will fold, or if the number it generates is divisible by 5, it folds. 
    
    Then to call, it sees if it's hand strength is either equal or greater than the player's, then it calls, or if the number it generates is even. 
    
    Then for raising, if it's hand has greater strength then the player's, it raises, and also if the number it generates is odd or even 
    and its strength is greater or equal to player's hand, it raises, otherwise, if the number it generates is odd, it raises.
    
    When table cards length == 5, showdown begins
    
    
    """

    #player_hand = []
    #computer_hand = []
    #table_cards = []

    #await ctx.send('Dealing {}\'s hand'.format(ctx.message.author.mention))

    #for i in range(2):
    #    card,deck = deal(deck)
    #    player_hand.append(card)

    #await ctx.send('Dealing {}\'s hand'.format(client.user.display_name))

    #for i in range(2):
    #    card,deck = deal(deck)
    #    computer_hand.append(card)

    #await ctx.send('Dealing table cards')

    #for i in range(2):
    #    card,deck = deal(deck)
    #    table_cards.append(card)

    #await display_table_cards(ctx,table_cards)

    #await display_player_hand(ctx,table_cards + player_hand)

    player_chips = 0
    computer_chips = random.randint(10000,10000000)

    await ctx.send('{} How many chips do you wish to enter into the poker arena with?'.format(ctx.message.author.mention))

    while True:
        message = await client.wait_for('message', check=lambda message: message.author == ctx.author)
        try:
            player_chips = int(message.content)
            break
        except Exception as e:
            await ctx.send("\n------ERROR : INVALID INPUT------\n--> Enter a number value <--\n")

    rounds = 1
    player_wins = 0
    computer_wins = 0

    while True:
        first_turn = False
        raise_amt = 0
        raised = False
        await ctx.send('-----------------------------------------------------------------------------------------------------\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tROUND {}\n-----------------------------------------------------------------------------------------------------\n'.format(rounds))

        end_game = False
        if rounds > 1:
            while True:
                await ctx.send('Continue Poker? 1) Yes 2) No')
                msg = await client.wait_for('message', check=lambda message : message.author == ctx.author)
                try:
                    msg = int(msg.content)
                    if msg == 2:
                        end_game = True
                        break
                    else:
                        end_game = False
                        break
                except asyncio.TimeoutError as e:
                    await ctx.send('Enter input -- Timeout Error')
                except ValueError as e:
                    await ctx.send('Enter valid input')

        if end_game:
            break


        rounds += 1
        pot = 0
        player_raised = False
        computer_raised = False
        folded = False

        ## Pre-Round configuration
        """
        
        Configuration :
        
        1) Create new deck
        2) Empty player hand, computer hand, and table cards
        3) Deal to player hand
        4) Deal to computer hand
        5) Deal table cards
        
        """

        deck = generate_deck()
        for i in range(7):
            deck = shuffle(deck)
        player_hand = []
        computer_hand = []
        table_cards = []

        await ctx.send('Dealing {}\'s hand'.format(ctx.message.author.mention))

        for i in range(2):
            card, deck = deal(deck)
            player_hand.append(card)

        await ctx.send('Dealing {}\'s hand'.format(client.user.display_name))

        for i in range(2):
            card, deck = deal(deck)
            computer_hand.append(card)

        await ctx.send('Dealing table cards')

        for i in range(2):
            card, deck = deal(deck)
            table_cards.append(card)

        await display_table_cards(ctx, table_cards)

        await display_player_hand(ctx, table_cards + player_hand)

        player_hand += table_cards
        computer_hand += table_cards

        ## Put Down bets

        while True:
            await ctx.send("\n----------- PLAYER PLACE BET [Current Chip Amount : {}]".format(player_chips))
            bets = await client.wait_for('message', check=lambda message : message.author == ctx.author)
            try:
                bets = int(bets.content)
                player_chips -= bets
                pot += bets
                break
            except Exception as e:
                await ctx.send("\n--------- ERROR : INVALID INPUT ---------\n")
                continue


        await ctx.send("\n------- COMPUTER CALLING BET -------\n")
        if computer_chips < bets:
            pot += computer_chips
            computer_chips = 0
        else:
            computer_chips -= bets
            pot += bets


        while True:

            await ctx.send('\n------------STATS------------\n-- POT : {}                      --'.format(pot))

            if first_turn:
                if len(table_cards) == 5:
                    ## showdown between player_hand and computer_hand
                    result = showdown(player_hand,computer_hand)
                    if result == 1:
                        await ctx.send('\n{} WINS {} chips!\n'.format(ctx.message.author.mention,pot))
                        player_chips += pot

                    elif result == 2:
                        await ctx.send('\n WINS {} chips!!\n'.format(client.user.display_name, pot))
                        computer_chips += pot
                    else:
                        await ctx.send('\n TIE! Both {} and {} win {} chips!\n'.format(ctx.message.author.mention,client.user.display_name,pot // 2))
                        player_chips += pot // 2
                        computer_chips += pot // 2
                    break
                    print('showdown between player hand and computer_hand')
                card,deck = deal(deck)
                player_hand += [card]
                await ctx.send('Dealing to {}\'s hand'.format(ctx.message.author.mention))
                computer_hand += [card]
                await ctx.send('Dealing to {}\'s hand'.format(client.user.display_name))
                table_cards += [card]
                await display_table_cards(ctx, table_cards)
                await display_player_hand(ctx, player_hand)

            if raised:
                await ctx.send('\n{} must call the raise of {} chips or fold\n'.format(ctx.message.author.mention,raise_amt))
                await ctx.send('\n------------- CHOICES -------------\n1)Call\n2)Fold')
                msg = await client.wait_for('message', check=lambda message: message.author == ctx.author)
                try:
                    msg = int(msg.content)
                    if msg == 1:
                        if player_chips < raise_amt:
                            pot += player_chips
                            player_chips = 0
                        else:
                            pot += raise_amt
                            player_chips -= raise_amt
                        raised = False
                    else:
                        await ctx.send('\n{} folds\n'.format(ctx.message.author.mention))
                        folded = True
                        if player_wins == 0:
                            player_wins = 0
                        else:
                            player_wins -= 1
                        computer_wins += 1
                        computer_chips += pot
                        break
                except ValueError as e:
                    await ctx.send('\nEnter valid input\n')

            while True:
                await ctx.send("\n------------- CHOICES -------------\n1)Fold\n2)Call\n3)Raise")
                message = await client.wait_for('message',check=lambda message : message.author == ctx.author)
                try:
                    message = int(message.content)
                    break
                except Exception as e:
                    await ctx.send("\n------------ Enter valid value ----------\n")
            if message == 1:
                await ctx.send("\n{} folds\n".format(ctx.message.author.mention))
                if player_wins == 0:
                    player_wins = 0
                    computer_chips += pot
                else:
                    player_wins -= 1
                    computer_chips += pot
                computer_wins += 1
                folded = True
                break
            elif message == 2:
                ## call
                await ctx.send("\n{} calls\n".format(ctx.message.author.mention))
            elif message == 3:
                ## raise
                if player_chips == 0:
                    await ctx.send('\nYou must have chips in order to raise\n')
                    continue
                await ctx.send("\nHow many chips do you want to raise?[Current Amount : {}]".format(player_chips))
                while True:
                    amt = await client.wait_for('message',check= lambda message : message.author == ctx.author)
                    try:
                        raise_amt = int(amt.content)
                        player_chips -= raise_amt
                        pot += raise_amt
                        break
                    except Exception as e:
                        await ctx.send("\n----- ERROR INVALID INPUT -----\n")
                        continue
                await ctx.send("\n{} raises {} chips".format(ctx.message.author.mention,raise_amt))
                raised = True


            ### Computer's turn

            player_strength = poker_combos(player_hand)
            computer_strength = poker_combos(computer_hand)

            #if type(computer_strength) == list:
            #    computer_strength = 0
            #if type(player_strength) == list:
            #    player_strength = 0  ### 0 meaning high card, for non-value based purposes, the value of the high card is not evaluated, but whether both players have high cards

            if raised:
                if type(player_strength) == list:
                    if type(computer_strength) == list:
                        if computer_strength[0] > player_strength[0]:
                            ## call raise
                            await ctx.send(
                                '\n{} calls the raise of {} chips\n'.format(client.user.display_name, raise_amt))
                            pot += raise_amt
                            computer_chips -= raise_amt
                            raised = False
                            first_turn = True
                        else:
                            ## determine if call or fold
                            rand_choice = random.randint(0, 1000000)
                            if rand_choice % 2 == 0 or rand_choice % 3 == 0:
                                await ctx.send(
                                    '\n{} calls the raise of {} chips\n'.format(client.user.display_name, raise_amt))
                                pot += raise_amt
                                computer_chips -= raise_amt
                                raised = False
                                first_turn = True
                            else:
                                await ctx.send('\n{} folds\n'.format(client.user.display_name))
                                if computer_wins == 0:
                                    computer_wins = 0
                                    player_chips += pot
                                else:
                                    computer_wins -= 1
                                    player_chips += pot
                                player_wins += 1
                                ## make loss variable
                                folded = True
                                break
                    else:
                        ## call raise
                        await ctx.send('\n{} calls the raise of {} chips\n'.format(client.user.display_name, raise_amt))
                        pot += raise_amt
                        computer_chips -= raise_amt
                        raised = False
                        first_turn = True
                elif type(computer_strength) == list:
                    ## determine if call or fold
                    rand_choice = random.randint(0, 1000000)
                    if rand_choice % 2 == 0 or rand_choice % 3 == 0:
                        await ctx.send('\n{} calls the raise of {} chips\n'.format(client.user.display_name, raise_amt))
                        pot += raise_amt
                        computer_chips -= raise_amt
                        raised = False
                        first_turn = True
                    else:
                        await ctx.send('\n{} folds\n'.format(client.user.display_name))
                        if computer_wins == 0:
                            computer_wins = 0
                            player_chips += pot
                        else:
                            computer_wins -= 1
                            player_chips += pot
                        player_wins += 1
                        ## make loss variable
                        folded = True
                        break
                elif computer_strength >= player_strength:
                    if computer_chips >= raise_amt:
                        ## call raise
                        await ctx.send('\n{} calls the raise of {} chips\n'.format(client.user.display_name,raise_amt))
                        pot += raise_amt
                        computer_chips -= raise_amt
                        raised = False
                        first_turn = True
                    else:
                        ## generate random number to determine if to call or fold
                        rand_choice = random.randint(0,1000000)
                        if rand_choice % 2 == 0 or rand_choice % 3 == 0:
                            await ctx.send('\n{} calls the raise of {} chips\n'.format(client.user.display_name, raise_amt))
                            pot += raise_amt
                            computer_chips -= raise_amt
                            raised = False
                            first_turn = True
                        else:
                            await ctx.send('\n{} folds\n'.format(client.user.display_name))
                            if computer_wins == 0:
                                computer_wins = 0
                                player_chips += pot
                            else:
                                computer_wins -= 1
                                player_chips += pot
                            player_wins += 1
                            ## make loss variable
                            folded = True
                            break
                else:
                    ## generate random number to determine if to call or fold
                    rand_choice = random.randint(0, 1000000)
                    if rand_choice % 2 == 0 or rand_choice % 3 == 0:
                        await ctx.send('\n{} calls the raise of {} chips\n'.format(client.user.display_name, raise_amt))
                        pot += raise_amt
                        computer_chips -= raise_amt
                        raised = False
                    else:
                        await ctx.send('\n{} folds\n'.format(client.user.display_name))
                        if computer_wins == 0:
                            computer_wins = 0
                            player_chips += pot
                        else:
                            computer_wins -= 1
                            player_chips += pot
                        player_wins += 1
                        folded = True
                        ## make loss variable to exit out of loop
                        break
            elif message == 2:
                ## player called

                ## decide if to fold

                if type(player_strength) == type([]):
                    ## player has a high card
                    if type(computer_strength) == type([]):
                        ## both have high cards, compare high cards
                        if player_strength[0] > computer_strength[0]:
                            ## generate number to determine if to fold
                            rand_choice = random.randint(0,1000000)
                            if rand_choice % 5 == 0:
                                await ctx.send("\n{} folds\n".format(client.user.display_name))
                                if computer_wins == 0:
                                    computer_wins = 0
                                    player_chips += pot
                                else:
                                    computer_wins -= 1
                                    player_chips += pot
                                player_wins += 1
                                folded = True
                                break
                            else:
                                ## call
                                await ctx.send('\n{} calls\n'.format(client.user.display_name))
                                first_turn = True
                        else:
                            ## computer's card is higher then players card, call
                            await ctx.send('\n{} calls\n'.format(client.user.display_name))
                            first_turn = True
                    else:
                        ## computer has combo while player has high card, call
                        await ctx.send('\n{} calls\n'.format(client.user.display_name))
                        first_turn = True
                else:
                    ## player has combo, check if computer's combo is greater
                    if type(computer_strength) != list and computer_strength > player_strength:
                        await ctx.send('\n{} calls\n'.format(client.user.display_name))
                        first_turn = True
                        ## computer strength is greater, call
                    else:
                        ## generate random number to determine whether to fold
                        rand_choice = random.randint(0,1000000)
                        if rand_choice % 5 == 0:
                            await ctx.send('\n{} folds\n'.format(client.user.display_name))
                            if computer_wins == 0:
                                computer_wins = 0
                                player_chips += pot
                            else:
                                computer_wins -= 1
                                player_chips += pot
                            player_wins += 1
                            folded = True
                            # make a loss variable
                            break
                        else:
                            ## call
                            await ctx.send('\n{} calls\n'.format(client.user.display_name))
                            first_turn = True
            elif message == 3:
                ## player raised
                ## check if player has high card
                if type(player_strength) == list:
                    if type(computer_strength) == list:
                        rand_choice = random.randint(0, 1000000)
                        if rand_choice % 2 == 0 or rand_choice % 3 == 0:
                            ## raise
                            raise_amt = random.randint(0, player_chips // 2)
                            await ctx.send('\n{} raises {} chips\n'.format(client.user.display_name, raise_amt))
                            computer_chips -= raise_amt
                            pot += raise_amt
                            raised = True
                            first_turn = True
                        else:
                            await ctx.send('\n{} folds\n'.format(client.user.display_name))
                            if computer_wins == 0:
                                computer_wins = 0
                                player_chips += pot
                            else:
                                computer_wins -= 1
                                player_chips += pot
                            player_wins += 1
                            folded = True
                            break
                    else:
                        raise_amt = random.randint(0, player_chips // 2)
                        await ctx.send('\n{} raises {} chips\n'.format(client.user.display_name, raise_amt))
                        computer_chips -= raise_amt
                        pot += raise_amt
                        raised = True
                        first_turn = True
                elif type(computer_strength) == list:
                    rand_choice = random.randint(0, 1000000)
                    if rand_choice % 2 == 0 or rand_choice % 3 == 0:
                        ## raise
                        raise_amt = random.randint(0, player_chips // 2)
                        await ctx.send('\n{} raises {} chips\n'.format(client.user.display_name, raise_amt))
                        computer_chips -= raise_amt
                        pot += raise_amt
                        raised = True
                        first_turn = True
                    else:
                        await ctx.send('\n{} folds\n'.format(client.user.display_name))
                        if computer_wins == 0:
                            computer_wins = 0
                            player_chips += pot
                        else:
                            computer_wins -= 1
                            player_chips += pot
                        player_wins += 1
                        folded = True
                        break
                elif computer_strength >= player_strength:
                    ## raise
                    raise_amt = random.randint(0, player_chips // 2)
                    await ctx.send('\n{} raises {} chips\n'.format(client.user.display_name, raise_amt))
                    computer_chips -= raise_amt
                    pot += raise_amt
                    raised = True
                    first_turn = True
                else:
                    rand_choice = random.randint(0,1000000)
                    if rand_choice % 2 == 0 or rand_choice % 3 == 0:
                        ## raise
                        raise_amt = random.randint(0,player_chips // 2)
                        await ctx.send('\n{} raises {} chips\n'.format(client.user.display_name,raise_amt))
                        computer_chips -= raise_amt
                        pot += raise_amt
                        raised = True
                        first_turn = True
                    else:
                        await ctx.send('\n{} folds\n'.format(client.user.display_name))
                        if computer_wins == 0:
                            computer_wins = 0
                            player_chips += pot
                        else:
                            computer_wins -= 1
                            player_chips += pot
                        player_wins += 1
                        folded = True
                        break
        #if folded:
        #    break








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


def print_board(board):

    board_str = ''
    board_str += '\tY\nX\t'
    for i in range(len(board)):
        board_str += str(i) + '\t '
    board_str += '\n'
    for i in range(len(board)):
        board_str += str(i) + '\t'
        for j in range(len(board[i])):
            if board[i][j] == 'X':
                board_str += '[]' + '\t'
            elif board[i][j] == 'O':
                board_str += 'O' + '\t'
            else:
                board_str += board[i][j] + '\t'
        board_str += '\n'
    return board_str

@client.command(aliases=['find'])
async def find_x(ctx):
    """

    Description : This game will consist of the computer generating a NxN matrix, and hiding a letter x under one of the squares, the user
    will guess which square it is in, and the computer will tell the user whether they guessed correctly or not, and depending on how many
    guesses they made, and how many points they scored. (2 guesses right in a row earns double points! and 3 = x3 and it keeps multiplying)
    depending on how many points are acquired, an emoji is sent into the chat of either a gold, bronze, or silver medal

    Addition : The bot tells the user whether they are close or far away, depending on how close their guess is to the hidden letter,
    (sometimes it's flipped)

    """

    board = []

    await ctx.send('\nThe rules of the game are : \n\n1)You will enter a single digit to specify the matrix size\n\n2)The matrix will be generated, and one x will be hidden, the bot will announce when the x has been hidden and the game will commence\n\n3)The user will then input coordinates x,y to guess where the hidden x is, if the user is right they earn one point, if the user is wrong, they earn 0 points, if the user guesses 2 spots consecutively right, then they earn 2x score, and 3 for 3x, 4 for 4x and so on\n\n4)Once all spaces have been guessed, the game ends, and the user\'s score is displayed, along with an emoji signifying if the user has scored gold, silver, or bronze\n\n5)The user then is given the option to either keep playing, or end the game')

    await ctx.send('\n------------------------------------------END OF RULES------------------------------------------\n')
    while True:
        await ctx.send("\nUser : Enter a single number to specify the dimensions of the NxN matrix\n")
        answer = await client.wait_for('message',check=lambda message: message.author == ctx.author)
        try:
            answer = int(answer.content)
            break
        except Exception as e:
            await ctx.send("\nEnter valid input\n")
    await ctx.send('\nGenerating board of {}x{} size\n'.format(answer,answer))
    for i in range(answer):
        board_row = []
        for j in range(answer):
            board_row.append('[]')
        board.append(board_row)

    """board_str = ''
    board_str += '\tY\nX\t'
    for i in range(len(board)):
        board_str += str(i) + '\t '
    board_str += '\n'
    for i in range(len(board)):
        board_str += str(i) + '\t'
        for j in range(len(board[i])-1):
            board_str += board[i][j] + '\t'
        board_str += board[i][len(board[i])-1]
        board_str += '\n'"""

    first_turn = False
    guessed = False ## user has guessed successfully
    user_points = 0
    consecutive_guesses = 1
    consecutive_guessing = False
    hits = 0
    misses = 0
    consecutive_hits = 0
    guesses = 0
    while True: ## Game loop

        ## X <--- targets, O <--- already guessed spots, when target is guessed, turns into O and is displayed

        ## computer hides x first
        rand_x = 0
        rand_y = 0

        if not first_turn or guessed: # must hide on first turn and the sequential turns
            await ctx.send('\n{} is hiding the x in the spot first'.format(client.user.display_name))

            ## generate random x
            rand_x = random.randint(0,len(board)-1)
            rand_y = random.randint(0,len(board[0])-1)

            while board[rand_x][rand_y] == 'X' or board[rand_x][rand_y] == 'O' or board[rand_x][rand_y] == 'S':
                rand_x = random.randint(0, len(board)-1)
                rand_y = random.randint(0, len(board[0])-1)
            board[rand_x][rand_y] = 'X'
            #await ctx.send('\nBot chooses spot {},{}'.format(rand_x,rand_y))
            guessed = False

            if not first_turn:
                await ctx.send('\n{} has hidden the first target\n'.format(client.user.display_name))
            else:
                await ctx.send('\n{} has hidden the target\n'.format(client.user.display_name))

        ## get user input first
        while True:
            await ctx.send('\nUser : Enter input in x,y format exactly, any malformed input will result in re-inputting data\n')
            msg = await client.wait_for('message',check=lambda message: message.author == ctx.author)
            try:
                msg = msg.content.split(',')
                x = int(msg[0])
                y = int(msg[1])
                if board[x][y] == 'O' or board[x][y] == 'S':
                    await ctx.send('\nBoard space has already been selected, re-input values\n')
                    continue
                guesses += 1
                if not first_turn: ## first turn triggered, game initiated
                    first_turn = True
                break
            except Exception as e:
                await ctx.send('\nMalformed input : Resubmit input\n')
                continue

        if board[x][y] == 'X':
            board[x][y] = 'S'
            if consecutive_guessing:
                consecutive_guesses += 1
                consecutive_hits = max(consecutive_hits,consecutive_guesses-1)
                hits += 1
                await ctx.send('\nYou have consecutively guessed the target! This is your {} consecutive guess, equalling a total of an extra {} points!\n'.format(consecutive_guesses-1,user_points*consecutive_guesses))
                user_points += user_points*consecutive_guesses
            else:
                hits += 1
                user_points += 1
            guessed = True
            consecutive_guessing = True
            await ctx.send('{} you have hit a target! [Total points : {}]'.format(ctx.message.author.mention,user_points))
        else:
            board[x][y] = 'O'
            misses += 1
            await ctx.send('{} you have missed the target!'.format(ctx.message.author.mention))
            consecutive_guessing = False
        board_str = print_board(board)
        if guesses == answer*answer:
            break
        await ctx.send(board_str)

    await ctx.send('Congratulations on completing the game! Here are your stats!\nMisses : {}\nHits : {}\nConsecutive Hits : {}\nPoints : {}'.format(misses,hits,consecutive_hits,user_points))


def print_maze(board):

    ## Ignore printing T values, print F(ood) values, walls and start and end point

    board_str = ''

    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 'T':
                board_str += 'o'
            else:
                board_str += board[i][j]
        board_str += '\n'
    return board_str


@client.command(aliases=['war'])
async def war_game(ctx):

    deck = generate_deck()
    for i in range(7):
        deck = shuffle(deck)
    split = len(deck) // 2
    player_hand = []
    computer_hand = []
    for i in range(len(deck)):
        if len(player_hand) == split:
            computer_hand.append(deck[i])
        else:
            player_hand.append(deck[i])
    ## player hand and computer hand generated

    player_wins = 0
    computer_wins = 0
    await ctx.send("\nThe game of war is as follows : both players get half of the deck, each play card on top, each player has option to shuffle deck before deal, player with most wins at end of game wins")

    await ctx.send('\nLET THE GAMES BEGIN\n')
    while len(player_hand) > 0 and len(computer_hand) > 0:
        ## game loop
        while True:
            ## user input
            await ctx.send("\nChoices :\n1)Shuffle\n2)Deal card")
            answer = await client.wait_for('message',check=lambda message:message.author == ctx.author)
            try:
                answer = int(answer.content)
                break
            except Exception as e:
                await ctx.send('\nInvalid input\n')
                continue
        if answer == 1:
            ## shuffle
            player_hand = shuffle(player_hand)
        player_card,player_hand = deal(player_hand)

        computer_generator = random.randint(1,100000)
        if _is_prime(computer_generator):
            ## computer shuffles
            computer_hand = shuffle(computer_hand)
        computer_card,computer_hand = deal(computer_hand)

        await ctx.send('\n{} vs {}\n'.format(player_card.split(' ')[0],computer_card.split(' ')[0]))

        result = war_showdown(player_card,computer_card)

        if result == 1:
            ## player won
            await ctx.send('\nPlayer wins!\n')
            player_wins += 1
        elif result == 2:
            await ctx.send('\nComputer wins!\n')
            computer_wins += 1
        else:
            ## tie
            await ctx.send('\nTie!\n')


class Player:

    def __init__(self,name):
        self.name = name
        self.hp = 150
        self.upper_body_health = 100
        self.lower_body_health = 100
        self.upper_strength = 1
        self.lower_strength = 1
        self.upper_defense = 1
        self.lower_defense = 1
        self.agility = 1
        self.crit = 1

    def set_computer(self,name):
        if name.lower() == 'tyson': # mike tyson
            self.name = 'Mike Tyson'
            self.hp = 250
            self.upper_body_health = 200
            self.lower_body_health = 100
            self.upper_strength = 10 # max upper body
            self.lower_strength = 5 # 5% increase among hits
            self.upper_defense = 8 # 8% decrease among hits
            self.lower_defense = 5 # 5% decrease among hits
            self.agility = 5 # 5% chance to dodge attack
            self.crit = 10
        elif name.lower() == 'ali': #Ali
            self.name = 'Muhammad Ali'
            self.hp = 350
            self.upper_body_health = 325
            self.lower_body_health = 175
            self.upper_strength = 10
            self.lower_strength = 10
            self.upper_defense = 11
            self.lower_defense = 11
            self.agility = 11
            self.crit = 4
        elif name.lower() == 'mayweather':
            self.name = 'Floyd Mayweather'
            self.hp = 300
            self.upper_body_health = 200
            self.lower_body_health = 200
            self.upper_strength = 6
            self.lower_strength = 6
            self.upper_defense = 10
            self.lower_defense = 10
            self.agility = 10
            self.crit = 6
        elif name.lower() == 'rocky': ## strongest preset
            self.name = 'Rocky Balboa'
            self.hp = 400
            self.upper_body_health = 300
            self.lower_body_health = 300
            self.upper_strength = 15
            self.lower_strength = 5
            self.upper_defense = 15
            self.lower_defense = 4
            self.agility = 3
            self.crit = 15
        elif name.lower() == 'dev':
            self.name = 'DevMode'
            self.hp = 9999
            self.upper_body_health = 9999
            self.lower_body_health = 9999
            self.upper_strength = 9999
            self.lower_strength = 9999
            self.upper_defense = 9999
            self.lower_defense = 9999
            self.agility = 9999
            self.crit = 9999
        else:
            ## default computer
            self.name = 'Computer Player'
            self.hp = 150
            self.upper_body_health = 100
            self.lower_body_health = 100
            self.upper_strength = 1
            self.lower_strength = 1
            self.upper_defense = 1
            self.lower_defense = 1
            self.agility = 1

    async def change_stat(self,stat,context):
        while True:
            await context.send('\nEnter the stat\n')
            answer = await client.wait_for('message',check= lambda message: message.author == context.author)
            try:
                answer = int(answer.content)
                if stat.lower() == 'hp':
                    self.hp = answer
                    break
                elif stat.lower() == 'upper_body_health':
                    self.upper_body_health = answer
                    break
                elif stat.lower() == 'lower_body_health':
                    self.lower_body_health = answer
                    break
                elif stat.lower() == 'upper_strength':
                    self.upper_strength = answer
                    break
                elif stat.lower() == 'lower_strength':
                    self.lower_strength = answer
                    break
                elif stat.lower() == 'upper_defense':
                    self.upper_defense = answer
                    break
                elif stat.lower() == 'lower_defense':
                    self.lower_defense = answer
                    break
                elif stat.lower() == 'agility':
                    self.agility = answer
                    break
            except Exception as e:
                await context.send('\nInvalid input\n')

    def display_player(self):

        return '-=-=-=-=PLAYER {}-=-=-=-=\nHP : {}\nUPPER BODY HEALTH : {}\nLOWER BODY HEALTH : {}\nUPPER STRENGTH : {}\nLOWER STRENGTH : {}\nUPPER DEFENSE : {}\nLOWER DEFENSE : {}\nAGILITY : {}'.format(self.name,self.hp,self.upper_body_health,self.lower_body_health,self.upper_strength,self.lower_strength,self.upper_defense,self.lower_defense,self.agility)


@client.command(aliases=['box'])
async def _box(ctx):

    await ctx.send('\nWelcome to Bot Boxing!\n')
    await ctx.send('\nThere are 4 types of attacks available to the player! \n1)Uppercut\n2)Jab\n3)Leg Kick\n4)Wheel Kick')
    await ctx.send('\n{} enter the name of your fighter!'.format(ctx.message.author.mention))
    player_name = await client.wait_for('message',check= lambda message : message.author == ctx.author)
    player1 = Player(player_name.content)
    await ctx.send('\nDo you wish to edit your stats?(y/yes/n/no)')
    answer = await client.wait_for('message',check = lambda message: message.author == ctx.author)
    if answer.content.lower() == 'y' or answer.content.lower() == 'yes':
        ## display menu
        while True:
            await ctx.send('\n-=-=-=Menu-=-=-=\n1)Display Player Stats\n2)Change HP\n3)Change Upper Body Health\n4)Change Lower Body Health\n5)Change Upper Strength\n6)Change Lower Strength\n7)Change Upper Defense\n8)Change Lower Defense\n9)Change Agility\n10)Exit Stat Change Station')
            answer = await client.wait_for('message',check= lambda message : message.author == ctx.author)
            try:
                answer = int(answer.content)
                if answer == 1:
                    await ctx.send(player1.display_player())
                elif answer == 2:
                    await player1.change_stat('hp',ctx)
                elif answer == 3:
                    await player1.change_stat('upper_body_health',ctx)
                elif answer == 4:
                    await player1.change_stat('lower_body_health',ctx)
                elif answer == 5:
                    await player1.change_stat("upper_strength",ctx)
                elif answer == 6:
                    await player1.change_stat('lower_strength',ctx)
                elif answer == 7:
                    await player1.change_stat('upper_defense',ctx)
                elif answer == 8:
                    await player1.change_stat('lower_defense',ctx)
                elif answer == 9:
                    await player1.change_stat('agility',ctx)
                else:
                    break
            except Exception as e:
                await ctx.send('\nInvalid input\n')

    rand_choice = random.randint(1,2)
    turn = ''
    if rand_choice == 1:
        turn = 'u'
    else:
        turn = 'c'

    ### choose computer player
    computer_player = ''
    computer_players = ['rocky','ali','mayweather','tyson','default','dev']
    while True:
        await ctx.send('\nChoose computer player, presets are :\n--> Default\n--> Ali\n--> Mayweather\n--> Tyson\n--> Rocky\n--> Dev')
        answer = await client.wait_for('message',check= lambda message : message.author == ctx.author)
        try:
            answer = answer.content
            if answer.lower() in computer_players:
                ## valid choice
                computer_player = Player('')
                computer_player.set_computer(answer)
                break
            else:
                await ctx.send('\nInvalid choice\n')
        except Exception as e:
            await ctx.send('Invalid input')

    damage = 0
    rand_choice = 0
    crit = False
    attack_type = ''
    attack_specific = ''
    dodge = False
    attacked = ''
    multiplier = 0

    while True:

        """
        Game Format:
        
        1) Flip coin to determine who goes first
        2) Player will have overall hp, upper body hp, and lower body hp
        3) Each time a player gets attacked, there is a loop that runs x amount of times(their agility strength) and they have 10 chances to dodge the attack
        
        Defending:
        4) If the attack lands, their defense comes into play, if it is an upper body attack, their defense reduces the damage by (x)% <-- their defense
        5) If any of their area HP's reach zero, then they are unable to make attacks with that area anymore (may be added : and also defense does not negatively affect damage(to their hp) whenever an attack is placed in that area)
        
        Attacking:
        6) When an attack is placed, the attacker's damage is increased (x)% <-- their strength
        7) Also, they have a (x)% chance to land a crit( loops x times and calculates x chances), a crit does 50% more damage
        
        Ending:
        8)When a player's hp reaches zero, the game ends
        
        """

        if turn == 'u':
            ## user turn
            if attacked == 'c':
                if attack_type == 'u':
                    ## upper attack
                    damage -= (damage * (player1.upper_defense / 100))
                    if attack_specific == 'uc':
                        ## uppercut
                        multiplier = 5
                    elif attack_specific == 'jb':
                        ## jab
                        multiplier = -5
                    dodge = False
                    for i in range(player1.agility+multiplier):
                        rand_choice = random.randint(1,10)
                        if rand_choice == random.randint(1,10) or rand_choice == random.randint(1,10):
                            dodge = True
                            break
                        else:
                            dodge = False
                    if dodge:
                        await ctx.send('\n{} dodged the attack!'.format(player1.name))
                    else:
                        if player1.upper_body_health <= 0:
                            damage += (damage * (player1.upper_defense / 100))
                            player1.hp -= damage
                        else:
                            player1.upper_body_health -= damage
                            await ctx.send('\n{} takes {} damage to their upper body!'.format(player1.name,damage))
                else:
                    ## lower attack
                    damage -= (damage * (player1.lower_defense / 100))
                    if attack_specific == 'lk':
                        ## leg kick
                        multiplier = -5
                    elif attack_specific == 'wk':
                        ## wheel kick
                        multiplier = 5
                    dodge = False
                    for i in range(player1.agility+multiplier):
                        rand_choice = random.randint(1,10)
                        if rand_choice == random.randint(1,10) or rand_choice == random.randint(1,10):
                            dodge = True
                            break
                        else:
                            dodge = False
                    if dodge:
                        await ctx.send('\n{} dodged the attack!'.format(player1.name))
                    else:
                        if player1.lower_body_health <= 0:
                            damage += (damage * (player1.lower_defense / 100))
                            player1.hp -= damage
                        else:
                            player1.lower_body_health -= damage
                            await ctx.send('\n{} takes {} damage to their lower body!'.format(player1.name,damage))
            if player1.hp <= 0:
                await ctx.send('\n{} has been KO\'d!'.format(player1.name))
                break

            await ctx.send('\n{} : choose your move \n1)Uppercut\n2)Jab\n3)Leg Kick\n4)Wheel Kick'.format(player1.name))
            while True:
                answer = await client.wait_for('message',check=lambda message : message.author == ctx.author)
                try:
                    answer = int(answer.content)
                except Exception as e:
                    await ctx.send('\nInvalid input\n')

                if answer == 1:
                    print('uppercut')
                    attack_specific = 'uc'
                    attack_type = 'u'
                    for i in range(player1.crit):
                        rand_choice = random.randint(1,10)
                        if rand_choice == random.randint(1,10) or rand_choice == random.randint(1,10):
                            ## crit landed
                            crit = True
                            break
                        else:
                            crit = False
                    ## no crit landed
                    if crit:
                        damage = 75
                        damage += (damage * (player1.upper_strength / 100))
                    else:
                        damage = 50
                        damage += (damage * (player1.upper_strength / 100))

                elif answer == 2:
                    print('jab')
                    attack_type = 'u'
                    attack_specific = 'jb'
                    for i in range(player1.crit):
                        rand_choice = random.randint(1,10)
                        if rand_choice == random.randint(1,10) or rand_choice == random.randint(1,10):
                            crit = True
                            break
                        else:
                            crit = False
                    if crit:
                        damage = 37.5
                        damage += (damage * (player1.upper_strength / 100))
                    else:
                        damage = 25
                        damage += (damage * (player1.upper_strength / 100))
                elif answer == 3:
                    print('leg kick')
                    attack_type = 'l'
                    attack_specific = 'lk'
                    for i in range(player1.crit):
                        rand_choice = random.randint(1,10)
                        if rand_choice == random.randint(1,10) or rand_choice == random.randint(1,10):
                            crit = True
                            break
                        else:
                            crit = False
                    if crit:
                        damage = 37.5
                        damage += (damage * (player1.upper_strength / 100))
                    else:
                        damage = 25
                        damage += (damage * (player1.upper_strength / 100))
                elif answer == 4:
                    print('wheel kick')
                    attack_specific = 'wk'
                    attack_type = 'l'
                    for i in range(player1.crit):
                        rand_choice = random.randint(1,10)
                        if rand_choice == random.randint(1,10) or rand_choice == random.randint(1,10):
                            crit = True
                            break
                        else:
                            crit = False
                    if crit:
                        damage = 75
                        damage += (damage * (player1.upper_strength / 100))
                    else:
                        damage = 50
                        damage += (damage * (player1.upper_strength / 100))
                turn = 'c'
                attacked = 'u'
                break
        else:
            ## computer turn
            attack_type = random.randint(1,4)
            if attacked == 'u':
                ## user attacked
                if attack_type == 'u':
                    ## upper attack
                    damage -= (damage * (computer_player.upper_defense / 100))
                    if attack_specific == 'uc':
                        ## uppercut
                        multiplier = 5
                    elif attack_specific == 'jb':
                        ## jab
                        multiplier = -5
                    dodge = False
                    for i in range(computer_player.agility+multiplier):
                        rand_choice = random.randint(1,10)
                        if rand_choice == random.randint(1,10):
                            ## dodged
                            dodge = True
                            break
                        else:
                            dodge = False
                    if dodge:
                        await ctx.send('\n{}} dodged the attack!\n'.format(computer_player.name))
                    else:
                        if computer_player.upper_body_health <= 0:
                            damage += (damage * (computer_player.upper_defense / 100))
                            computer_player.hp -= damage
                        else:
                            computer_player.upper_body_health -= damage
                            await ctx.send('\n{}} takes {} damage to their upper body!'.format(computer_player.name,damage))
                else:
                    ## lower attack
                    damage -= (damage * (computer_player.lower_defense / 100))
                    if attack_specific == 'lk':
                        ## leg kick
                        multiplier = -5
                    elif attack_specific == 'wk':
                        ## wheel kick
                        multiplier = 5
                    dodge = False
                    for i in range(computer_player.agility+multiplier):
                        rand_choice = random.randint(1,10)
                        if rand_choice == random.randint(1,10):
                            dodge = True
                            break
                        else:
                            dodge = False
                    if dodge:
                        await ctx.send('\n{} dodged the attack!'.format(computer_player.name))
                    else:
                        if computer_player.lower_body_health <= 0:
                            damage += (damage * (computer_player.lower_defense / 100))
                            computer_player.hp -= damage
                        else:
                            computer_player.lower_body_health -= damage
                            await ctx.send('\n{} takes {} damage to their lower body!'.format(computer_player.name,damage))
            if computer_player.hp <= 0:
                await ctx.send('\n{} has been KO\'d! {} wins!\n'.format(computer_player.name,player1.name))
                break
            else:
                await ctx.send('\n{} attacking!'.format(computer_player.name))
                if attack_type == 1:
                    ## uppercut
                    await ctx.send('\n{} attacks with an uppercut!'.format(computer_player.name))
                    attack_type = 'u'
                    attack_specific = 'uc'
                    for i in range(computer_player.crit):
                        rand_choice = random.randint(1,10)
                        if rand_choice == random.randint(1,10) or rand_choice == random.randint(1,10):
                            crit = True
                            break
                        else:
                            crit = False
                    if crit:
                        damage = 75
                        damage += (damage * (computer_player.upper_strength / 100))
                    else:
                        damage = 50
                        damage += (damage * (computer_player.upper_strength / 100))
                elif attack_type == 2:
                    ## jab
                    await ctx.send('\n{} attacks with a jab!'.format(computer_player.name))
                    attack_type = 'u'
                    attack_specific = 'jb'
                    for i in range(computer_player.crit):
                        rand_choice = random.randint(1,10)
                        if rand_choice == random.randint(1,10) or rand_choice == random.randint(1,10):
                            crit = True
                            break
                        else:
                            crit = False
                    if crit:
                        damage = 37.5
                        damage += (damage * (computer_player.upper_strength / 100))
                    else:
                        damage = 25
                        damage += (damage * (computer_player.upper_strength / 100))
                elif attack_type == 3:
                    ## leg kick
                    await ctx.send('\n{} attacks with a leg kick!'.format(computer_player.name))
                    attack_type = 'l'
                    attack_specific = 'lk'
                    for i in range(computer_player.crit):
                        rand_choice = random.randint(1,10)
                        if rand_choice == random.randint(1,10) or rand_choice == random.randint(1,10):
                            crit = True
                            break
                        else:
                            crit = False
                    if crit:
                        damage = 37.5
                        damage += (damage * (computer_player.upper_strength / 100))
                    else:
                        damage = 25
                        damage += (damage * (computer_player.upper_strength / 100))
                elif attack_type == 4:
                    ## wheel kick
                    await ctx.send('\n{} attacks with a wheel kick!'.format(computer_player.name))
                    attack_type = 'l'
                    attack_specific = 'wk'
                    for i in range(computer_player.crit):
                        rand_choice = random.randint(1,10)
                        if rand_choice == random.randint(1,10) or rand_choice == random.randint(1,10):
                            crit = True
                            break
                        else:
                            crit = False
                    if crit:
                        damage = 75
                        damage += (damage * (computer_player.upper_strength / 100))
                    else:
                        damage = 50
                        damage += (damage * (computer_player.upper_strength / 100))
                turn = 'u'
                attacked = 'c'







def war_showdown(card1,card2):

    special_cards = {'Jack': 11, 'Queen': 12, 'King': 13, 'Ace': 14}

    card1_rank = card1.split(' ')[0]
    card2_rank = card2.split(' ')[0]

    try:
        card1_rank = int(card1_rank)
    except Exception as e:
        card1_rank = special_cards[card1_rank]

    try:
        card2_rank = int(card2_rank)
    except Exception as e:
        card2_rank = special_cards[card2_rank]

    ## ranks acquired

    if card1_rank > card2_rank:
        ## player wins
        return 1
    elif card2_rank > card1_rank:
        ## computer wins
        return 2
    else:
        ## tie
        return 3





@client.command(aliases=['maze'])
async def maze_game(ctx):

    """

    Details: The player begins at the place specified by the letter S and the player's cursor is X, they traverse through walls |
    and can possibly run into traps, which decrease their strength, if they find food(F) then they gain strength(random value),
    the goal is to use the commands of UDRL(up down right left) to reach the end of the maze signified by E

    Default board size will be 10x10

    """

    """
    
    Difficulties :
    0 - Easy [default]
    1 - Medium
    2 - Hard
    3 - Very Hard
    
    """

    difficulty = 0

    while True:
        await ctx.send('\n{} enter the difficulty level : \n0)Easy\n1)Medium\n2)Hard\n3)Very Hard'.format(ctx.message.author.mention))
        answer = await client.wait_for('message',check=lambda message: message.author == ctx.author)
        try:
            answer = int(answer.content)
            difficulty = answer
            break
        except Exception as e:
            await ctx.send('\nMalformed input : Please re-input values\n')

    board_size = 10
    tot_size = board_size*board_size

    while True:
        await ctx.send('\n{} enter the board size(only one dimension size needed[minimum size is 10], will generate NxN board)'.format(ctx.message.author.mention))
        answer = await client.wait_for('message',check=lambda message: message.author == ctx.author)
        try:
            answer = int(answer.content)
            if answer < 10:
                answer = 10
            board_size = answer
            break
        except Exception as e:
            await ctx.send('\nMalformed input : Please re-input values\n')

    ## generating board

    board = []

    await ctx.send('\nGenerating board of {}x{} size'.format(board_size,board_size))

    for i in range(board_size):
        board_sub_list = []
        for j in range(board_size):
            board_sub_list.append('o')
        board.append(board_sub_list)



    await ctx.send('\nSetting starting point')
    ## generate start point

    start_point = random.randint(0, len(board) - 1)

    while board[start_point][0] != 'o':
        start_point = random.randint(0, len(board) - 1)

    board[start_point][0] = 'S'

    ## generate end point

    await ctx.send('\nSetting end point\n')

    end_point = random.randint(0, len(board) - 1)

    while board[end_point][len(board[0]) - 1] != 'o':
        end_point = random.randint(0, len(board) - 1)

    board[end_point][len(board[0]) - 1] = 'E'

    curr_player_x = start_point
    curr_player_y = 0

    await ctx.send('\nSettings traps for board\n')

    if difficulty == 0:
        ## generate random number between a tenth of the board size and
        for i in range(tot_size // 15):
            x = random.randint(0,len(board)-1)
            y = random.randint(0,len(board[0])-1)
            while board[x][y] != 'o':
                x = random.randint(0, len(board) - 1)
                y = random.randint(0, len(board[0]) - 1)
            board[x][y] = 'T'
        ## traps set for easy
    elif difficulty == 1:
        ## medium
        for i in range(tot_size // 14):
            x = random.randint(0,len(board)-1)
            y = random.randint(0,len(board[0])-1)
            while board[x][y] != 'o':
                x = random.randint(0,len(board)-1)
                y = random.randint(0,len(board[0])-1)
            board[x][y] = 'T'
        ## traps set
    elif difficulty == 2:
        ## hard
        for i in range(tot_size // 13):
            x = random.randint(0,len(board)-1)
            y = random.randint(0,len(board[0])-1)
            while board[x][y] != 'o':
                x = random.randint(0,len(board)-1)
                y = random.randint(0,len(board[0])-1)
            board[x][y] = 'T'
        ## traps set
    elif difficulty == 3:
        ## very hard
        for i in range(tot_size // 12):
            x = random.randint(0,len(board)-1)
            y = random.randint(0,len(board[0])-1)
            while board[x][y] != 'o':
                x = random.randint(0,len(board)-1)
                y = random.randint(0,len(board[0])-1)
            board[x][y] = 'T'
        ## traps set

    ## setting food for board
    #await ctx.send(print_maze(board))

    if difficulty == 0:
        ## easy
        for i in range(tot_size // 12):
            x = random.randint(0,len(board)-1)
            y = random.randint(0,len(board[0])-1)
            while board[x][y] != 'o':
                x = random.randint(0, len(board) - 1)
                y = random.randint(0, len(board[0]) - 1)
            board[x][y] = 'F'
        ## food has been set
    elif difficulty == 1:
        ## medium
        for i in range(tot_size // 13):
            x = random.randint(0,len(board)-1)
            y = random.randint(0,len(board[0])-1)
            while board[x][y] != 'o':
                x = random.randint(0,len(board)-1)
                y = random.randint(0,len(board[0])-1)
            board[x][y] = 'F'
        ## food has been set
    elif difficulty == 2:
        ## hard
        for i in range(tot_size // 14):
            x = random.randint(0,len(board)-1)
            y = random.randint(0,len(board[0])-1)
            while board[x][y] != 'o':
                x = random.randint(0,len(board)-1)
                y = random.randint(0,len(board[0])-1)
            board[x][y] = 'F'
        ## food has been set
    elif difficulty == 3:
        ## very hard
        for i in range(tot_size // 15):
            x = random.randint(0,len(board)-1)
            y = random.randint(0,len(board[0])-1)
            while board[x][y] != 'o':
                x = random.randint(0,len(board)-1)
                y = random.randint(0,len(board[0])-1)
            board[x][y] = 'F'
        ## food has been set

    #await ctx.send(print_maze(board))


    await ctx.send('\nFood has been set on the board\n')

    ## settings walls

    if difficulty == 0:
        ## easy
        for i in range(tot_size // 12):
            v_or_h = random.randint(0,1)
            if v_or_h == 0:
                ## horizontal
                x = random.randint(0,len(board)-1)
                y = random.randint(0,len(board[0])-1)
                while board[x][y] != 'o':
                    x = random.randint(0, len(board) - 1)
                    y = random.randint(0, len(board[0]) - 1)
                board[x][y] = '-'
            elif v_or_h == 1:
                ## vertical
                x = random.randint(0,len(board)-1)
                y = random.randint(0,len(board[0])-1)
                while board[x][y] != 'o':
                    x = random.randint(0, len(board) - 1)
                    y = random.randint(0, len(board[0]) - 1)
                board[x][y] = 'I'
    elif difficulty == 1:
        ## medium
        for i in range(tot_size // 13):
            v_or_h = random.randint(0,1)
            if v_or_h == 0:
                ## horizontal
                x = random.randint(0,len(board)-1)
                y = random.randint(0,len(board[0])-1)
                while board[x][y] != 'o':
                    x = random.randint(0, len(board) - 1)
                    y = random.randint(0, len(board[0]) - 1)
                board[x][y] = '-'
            elif v_or_h == 1:
                ## vertical
                x = random.randint(0,len(board)-1)
                y = random.randint(0,len(board[0])-1)
                while board[x][y] != 'o':
                    x = random.randint(0, len(board) - 1)
                    y = random.randint(0, len(board[0]) - 1)
                board[x][y] = 'I'
    elif difficulty == 2:
        ## hard
        for i in range(tot_size // 14):
            v_or_h = random.randint(0,1)
            if v_or_h == 0:
                ## horizontal
                x = random.randint(0,len(board)-1)
                y = random.randint(0,len(board[0])-1)
                while board[x][y] != 'o':
                    x = random.randint(0, len(board) - 1)
                    y = random.randint(0, len(board[0]) - 1)
                board[x][y] = '-'
            elif v_or_h == 1:
                ## vertical
                x = random.randint(0,len(board)-1)
                y = random.randint(0,len(board[0])-1)
                while board[x][y] != 'o':
                    x = random.randint(0, len(board) - 1)
                    y = random.randint(0, len(board[0]) - 1)
                board[x][y] = 'I'
    elif difficulty == 3:
        ## very hard
        for i in range(tot_size // 15):
            v_or_h = random.randint(0,1)
            if v_or_h == 0:
                ## horizontal
                x = random.randint(0,len(board)-1)
                y = random.randint(0,len(board[0])-1)
                while board[x][y] != 'o':
                    x = random.randint(0, len(board) - 1)
                    y = random.randint(0, len(board[0]) - 1)
                board[x][y] = '-'
            elif v_or_h == 1:
                ## vertical
                x = random.randint(0,len(board)-1)
                y = random.randint(0,len(board[0])-1)
                while board[x][y] != 'o':
                    x = random.randint(0, len(board) - 1)
                    y = random.randint(0, len(board[0]) - 1)
                board[x][y] = 'I'

    await ctx.send('\nWalls have been set\n')

    #await ctx.send(print_maze(board))

    """
    
    Set so far: traps, food, walls
    
    """

    """
    
    Generated so far:
    
    Traps
    Food
    Walls
    Start
    End
    
    """

    await ctx.send('\nRules:\n1)Your player starts on the S symbol, should be located on the far-left\n2)Your goal is to get to the E(the end of the maze)\n3)Walls are signified with - and |\n4)Move your character with the u/d/l/r commands')

    curr_player_strength = 0
    if difficulty == 0:
        ## easy
        curr_player_strength = random.randint(board_size,board_size + board_size)
    elif difficulty == 1:
        ## medium
        curr_player_strength = random.randint(board_size-2,board_size+board_size-(board_size // 10))
    elif difficulty == 2:
        ## hard
        curr_player_strength = random.randint(board_size-4,board_size+board_size-(board_size // 9))
    elif difficulty == 3:
        ## very hard
        curr_player_strength = random.randint(board_size-6,board_size+board_size-(board_size // 8))

    while True:

        await ctx.send(print_maze(board))
        if curr_player_strength == 0:
            await ctx.send('\Player\'s current strength is 0 : Game Over')
            break
        await ctx.send('\nPlayer\'s current strength : {}'.format(curr_player_strength))
        await ctx.send('\nUser : Enter direction to move (u/d/l/r)')
        answer = await client.wait_for('message',check=lambda message : message.author == ctx.author)
        try:
            answer = answer.content.lower()
            if answer == 'd':
                # move down
                if curr_player_x == len(board)-1:
                    ## trying to move out of bounds
                    await ctx.send('\nAttempting to move out of bounds of the board, choose another direction\n')
                    continue
                elif board[curr_player_x+1][curr_player_y] == 'E':
                    ## reached ending
                    await ctx.send('\nYou have reached the ending!\n')
                    break
                elif board[curr_player_x+1][curr_player_y] == 'F':
                    ## moved onto food
                    await ctx.send('\nYou have reached a food object!\n')
                    if difficulty == 0:
                        ## easy
                        rand_food = random.randint(5,15)
                        await ctx.send('\nYour strength increases by {}!'.format(rand_food))
                        curr_player_strength += rand_food
                    elif difficulty == 1:
                        ## medium
                        rand_food = random.randint(4,13)
                        await ctx.send('\nYour strength increases by {}!'.format(rand_food))
                        curr_player_strength += rand_food
                    elif difficulty == 2:
                        ## hard
                        rand_food = random.randint(3,12)
                        await ctx.send('\nYour strength increases by {}!'.format(rand_food))
                        curr_player_strength += rand_food
                    elif difficulty == 3:
                        ## very hard
                        rand_food = random.randint(3,10)
                        await ctx.send('\nYour strenth increases by {}!'.format(rand_food))
                        curr_player_strength += rand_food
                    board[curr_player_x+1][curr_player_y] = 'S'
                    board[curr_player_x][curr_player_y] = 'o'
                    curr_player_x += 1
                elif board[curr_player_x+1][curr_player_y] == 'T':
                    ## moved onto trap
                    await ctx.send('\nYou have stepped on a trap!\n')
                    if difficulty == 0:
                        ## easy
                        rand_loss = random.randint(1,5)
                        curr_player_strength -= rand_loss
                        await ctx.send('\nYou have lost {} strength!'.format(rand_loss))
                    elif difficulty == 1:
                        ## medium
                        rand_loss = random.randint(3,6)
                        curr_player_strength -= rand_loss
                        await ctx.send('\nYou have lost {} strength!'.format(rand_loss))
                    elif difficulty == 2:
                        ## hard
                        rand_loss = random.randint(5,7)
                        curr_player_strength -= rand_loss
                        await ctx.send('\nYou have lost {} strength!'.format(rand_loss))
                    elif difficulty == 3:
                        ## very hard
                        rand_loss = random.randint(7,8)
                        curr_player_strength -= rand_loss
                        await ctx.send('\nYou have lost {} strength!'.format(rand_loss))
                    if curr_player_strength <= 0:
                        ## player has lost
                        await ctx.send('\n{} has lost the game, their strength dropped to {}!'.format(ctx.message.author.mention,curr_player_strength))
                        break
                    else:
                        board[curr_player_x+1][curr_player_y] = 'S'
                        board[curr_player_x][curr_player_y] = 'o'
                        curr_player_x += 1
                elif board[curr_player_x+1][curr_player_y] == '-' or board[curr_player_x+1][curr_player_y] == 'I':
                    ## trying to move into wall (expend strength to break through)
                    await ctx.send('\nYou are moving towards a wall\n')
                    if difficulty == 0:
                        ## easy
                        expense = random.randint(1,4)
                        await ctx.send('\nYou can expend {} strength to break through the wall. (Y/N)?'.format(expense))
                        while True:
                            answer = await client.wait_for('message',check=lambda message: message.author == ctx.author)
                            try:
                                answer = str(answer.content)
                                if answer.upper() == 'Y':
                                    #yes
                                    if curr_player_strength < expense:
                                        await ctx.send('\nYour player does not have enough strength to expend to break through the wall\n')
                                        break
                                    else:
                                        curr_player_strength -= expense
                                        board[curr_player_x+1][curr_player_y] = 'S'
                                        board[curr_player_x][curr_player_y] = 'o'
                                        curr_player_x += 1
                                        curr_player_strength -= 1
                                        break
                                elif answer.upper() == 'N':
                                    #no
                                    break
                                else:
                                    #invalid input
                                    await ctx.send('\Invalid input\n')
                            except Exception as e:
                                await ctx.send('\nInvalid input\n')
                                continue
                    elif difficulty == 1:
                        ## medium
                        expense = random.randint(2,5)
                        await ctx.send('\nYou can expend {} strength to break through the wall. (Y/N)?'.format(expense))
                        while True:
                            answer = await client.wait_for('message',check=lambda message: message.author == ctx.author)
                            try:
                                answer = str(answer.content)
                                if answer.upper() == 'Y':
                                    #yes
                                    if curr_player_strength < expense:
                                        await ctx.send('\nYour player does not have enough strength to expend to break through the wall\n')
                                        break
                                    else:
                                        curr_player_strength -= expense
                                        board[curr_player_x+1][curr_player_y] = 'S'
                                        board[curr_player_x][curr_player_y] = 'o'
                                        curr_player_x += 1
                                        curr_player_strength -= 1
                                        break
                                elif answer.upper() == 'N':
                                    #no
                                    break
                                else:
                                    #invalid input
                                    await ctx.send('\Invalid input\n')
                            except Exception as e:
                                await ctx.send('\nInvalid input\n')
                                continue
                    elif difficulty == 2:
                        ## hard
                        expense = random.randint(3,6)
                        await ctx.send('\nYou can expend {} strength to break through the wall. (Y/N)?'.format(expense))
                        while True:
                            answer = await client.wait_for('message',check=lambda message: message.author == ctx.author)
                            try:
                                answer = str(answer.content)
                                if answer.upper() == 'Y':
                                    #yes
                                    if curr_player_strength < expense:
                                        await ctx.send('\nYour player does not have enough strength to expend to break through the wall\n')
                                        break
                                    else:
                                        curr_player_strength -= expense
                                        board[curr_player_x+1][curr_player_y] = 'S'
                                        board[curr_player_x][curr_player_y] = 'o'
                                        curr_player_x += 1
                                        curr_player_strength -= 1
                                        break
                                elif answer.upper() == 'N':
                                    #no
                                    break
                                else:
                                    #invalid input
                                    await ctx.send('\Invalid input\n')
                            except Exception as e:
                                await ctx.send('\nInvalid input\n')
                                continue
                    elif difficulty == 3:
                        expense = random.randint(4,7)
                        await ctx.send('\nYou can expend {} strength to break through the wall. (Y/N)?'.format(expense))
                        while True:
                            answer = await client.wait_for('message',check=lambda message: message.author == ctx.author)
                            try:
                                answer = str(answer.content)
                                if answer.upper() == 'Y':
                                    #yes
                                    if curr_player_strength < expense:
                                        await ctx.send('\nYour player does not have enough strength to expend to break through the wall\n')
                                        break
                                    else:
                                        curr_player_strength -= expense
                                        board[curr_player_x+1][curr_player_y] = 'S'
                                        board[curr_player_x][curr_player_y] = 'o'
                                        curr_player_x += 1
                                        curr_player_strength -= 1
                                        break
                                elif answer.upper() == 'N':
                                    #no
                                    break
                                else:
                                    #invalid input
                                    await ctx.send('\Invalid input\n')
                            except Exception as e:
                                await ctx.send('\nInvalid input\n')
                                continue
                        ## very hard
                else:
                    await ctx.send('\nSuccessful move, no objects on space\n')
                    board[curr_player_x+1][curr_player_y] = 'S'
                    board[curr_player_x][curr_player_y] = 'o'
                    curr_player_x += 1
                    curr_player_strength -= 1
            elif answer == 'u':
                # move up
                if curr_player_x == 0:
                    ## trying to move out of bounds
                    await ctx.send('\nAttempting to move out of bounds of the board, choose another direction\n')
                    continue
                elif board[curr_player_x-1][curr_player_y] == 'E':
                    ## reached ending
                    await ctx.send('\nYou have reached the ending!\n')
                    break
                elif board[curr_player_x-1][curr_player_y] == 'F':
                    ## moved onto food
                    await ctx.send('\nYou have reached a food object\n')
                    if difficulty == 0:
                        ## easy
                        rand_food = random.randint(5,15)
                        await ctx.send('\nYour strength increases by {}!'.format(rand_food))
                        curr_player_strength += rand_food
                    elif difficulty == 1:
                        ## medium
                        rand_food = random.randint(4,13)
                        await ctx.send('\nYour strength increases by {}!'.format(rand_food))
                        curr_player_strength += rand_food
                    elif difficulty == 2:
                        ## hard
                        rand_food = random.randint(3,12)
                        await ctx.send('\nYour strength increases by {}!'.format(rand_food))
                        curr_player_strength += rand_food
                    elif difficulty == 3:
                        ## very hard
                        rand_food = random.randint(3,10)
                        await ctx.send('\nYour strenth increases by {}!'.format(rand_food))
                        curr_player_strength += rand_food
                    board[curr_player_x-1][curr_player_y] = 'S'
                    board[curr_player_x][curr_player_y] = 'o'
                    curr_player_x -= 1
                elif board[curr_player_x-1][curr_player_y] == 'T':
                    ## moved onto trap
                    await ctx.send('\nYou have stepped on a trap!\n')
                    if difficulty == 0:
                        ## easy
                        rand_loss = random.randint(1, 5)
                        curr_player_strength -= rand_loss
                        await ctx.send('\nYou have lost {} strength!'.format(rand_loss))
                    elif difficulty == 1:
                        ## medium
                        rand_loss = random.randint(3, 6)
                        curr_player_strength -= rand_loss
                        await ctx.send('\nYou have lost {} strength!'.format(rand_loss))
                    elif difficulty == 2:
                        ## hard
                        rand_loss = random.randint(5, 7)
                        curr_player_strength -= rand_loss
                        await ctx.send('\nYou have lost {} strength!'.format(rand_loss))
                    elif difficulty == 3:
                        ## very hard
                        rand_loss = random.randint(7, 8)
                        curr_player_strength -= rand_loss
                        await ctx.send('\nYou have lost {} strength!'.format(rand_loss))
                    if curr_player_strength <= 0:
                        ## player has lost
                        await ctx.send(
                            '\n{} has lost the game, their strength dropped to {}!'.format(ctx.message.author.mention,
                                                                                           curr_player_strength))
                        break
                    else:
                        board[curr_player_x - 1][curr_player_y] = 'S'
                        board[curr_player_x][curr_player_y] = 'o'
                        curr_player_x -= 1
                elif board[curr_player_x-1][curr_player_y] == '-' or board[curr_player_x-1][curr_player_y] == 'I':
                    ## trying to move into wall (expend strength to break through)
                    await ctx.send('\nYou are moving towards a wall!\n')
                    if difficulty == 0:
                        ## easy
                        expense = random.randint(1,4)
                        await ctx.send('\nYou can expend {} strength to break through the wall. (Y/N)?'.format(expense))
                        while True:
                            answer = await client.wait_for('message',check=lambda message: message.author == ctx.author)
                            try:
                                answer = str(answer.content)
                                if answer.upper() == 'Y':
                                    #yes
                                    if curr_player_strength < expense:
                                        await ctx.send('\nYour player does not have enough strength to expend to break through the wall\n')
                                        break
                                    else:
                                        curr_player_strength -= expense
                                        board[curr_player_x-1][curr_player_y] = 'S'
                                        board[curr_player_x][curr_player_y] = 'o'
                                        curr_player_x -= 1
                                        curr_player_strength -= 1
                                        break
                                elif answer.upper() == 'N':
                                    #no
                                    break
                                else:
                                    #invalid input
                                    await ctx.send('\Invalid input\n')
                            except Exception as e:
                                await ctx.send('\nInvalid input\n')
                                continue
                    elif difficulty == 1:
                        ## medium
                        expense = random.randint(2,5)
                        await ctx.send('\nYou can expend {} strength to break through the wall. (Y/N)?'.format(expense))
                        while True:
                            answer = await client.wait_for('message',check=lambda message: message.author == ctx.author)
                            try:
                                answer = str(answer.content)
                                if answer.upper() == 'Y':
                                    #yes
                                    if curr_player_strength < expense:
                                        await ctx.send('\nYour player does not have enough strength to expend to break through the wall\n')
                                        break
                                    else:
                                        curr_player_strength -= expense
                                        board[curr_player_x-1][curr_player_y] = 'S'
                                        board[curr_player_x][curr_player_y] = 'o'
                                        curr_player_x -= 1
                                        curr_player_strength -= 1
                                        break
                                elif answer.upper() == 'N':
                                    #no
                                    break
                                else:
                                    #invalid input
                                    await ctx.send('\Invalid input\n')
                            except Exception as e:
                                await ctx.send('\nInvalid input\n')
                                continue
                    elif difficulty == 2:
                        ## hard
                        expense = random.randint(3,6)
                        await ctx.send('\nYou can expend {} strength to break through the wall. (Y/N)?'.format(expense))
                        while True:
                            answer = await client.wait_for('message',check=lambda message: message.author == ctx.author)
                            try:
                                answer = str(answer.content)
                                if answer.upper() == 'Y':
                                    #yes
                                    if curr_player_strength < expense:
                                        await ctx.send('\nYour player does not have enough strength to expend to break through the wall\n')
                                        break
                                    else:
                                        curr_player_strength -= expense
                                        board[curr_player_x-1][curr_player_y] = 'S'
                                        board[curr_player_x][curr_player_y] = 'o'
                                        curr_player_x -= 1
                                        curr_player_strength -= 1
                                        break
                                elif answer.upper() == 'N':
                                    #no
                                    break
                                else:
                                    #invalid input
                                    await ctx.send('\Invalid input\n')
                            except Exception as e:
                                await ctx.send('\nInvalid input\n')
                                continue
                    elif difficulty == 3:
                        expense = random.randint(4,7)
                        await ctx.send('\nYou can expend {} strength to break through the wall. (Y/N)?'.format(expense))
                        while True:
                            answer = await client.wait_for('message',check=lambda message: message.author == ctx.author)
                            try:
                                answer = str(answer.content)
                                if answer.upper() == 'Y':
                                    #yes
                                    if curr_player_strength < expense:
                                        await ctx.send('\nYour player does not have enough strength to expend to break through the wall\n')
                                        break
                                    else:
                                        curr_player_strength -= expense
                                        board[curr_player_x-1][curr_player_y] = 'S'
                                        board[curr_player_x][curr_player_y] = 'o'
                                        curr_player_x -= 1
                                        curr_player_strength -= 1
                                        break
                                elif answer.upper() == 'N':
                                    #no
                                    break
                                else:
                                    #invalid input
                                    await ctx.send('\Invalid input\n')
                            except Exception as e:
                                await ctx.send('\nInvalid input\n')
                                continue
                else:
                    await ctx.send('\nSuccessful move, no objects on space\n')
                    board[curr_player_x - 1][curr_player_y] = 'S'
                    board[curr_player_x][curr_player_y] = 'o'
                    curr_player_x -= 1
                    curr_player_strength -= 1
            elif answer == 'l':
                # move left
                if curr_player_y == 0:
                    ## trying to move out of bounds
                    await ctx.send('\nAttempting to move out of bounds of the board, choose another direction\n')
                    continue
                elif board[curr_player_x][curr_player_y-1] == 'E':
                    ## reached ending
                    await ctx.send('\nYou have reached the ending!\n')
                    break
                elif board[curr_player_x][curr_player_y-1] == 'F':
                    ## moved onto food
                    await ctx.send('\nYou have reached a food object\n')
                    if difficulty == 0:
                        ## easy
                        rand_food = random.randint(5,15)
                        await ctx.send('\nYour strength increases by {}!'.format(rand_food))
                        curr_player_strength += rand_food
                    elif difficulty == 1:
                        ## medium
                        rand_food = random.randint(4,13)
                        await ctx.send('\nYour strength increases by {}!'.format(rand_food))
                        curr_player_strength += rand_food
                    elif difficulty == 2:
                        ## hard
                        rand_food = random.randint(3,12)
                        await ctx.send('\nYour strength increases by {}!'.format(rand_food))
                        curr_player_strength += rand_food
                    elif difficulty == 3:
                        ## very hard
                        rand_food = random.randint(3,10)
                        await ctx.send('\nYour strenth increases by {}!'.format(rand_food))
                        curr_player_strength += rand_food
                    board[curr_player_x][curr_player_y - 1] = 'S'
                    board[curr_player_x][curr_player_y] = 'o'
                    curr_player_y -= 1
                elif board[curr_player_x][curr_player_y-1] == 'T':
                    ## moved onto trap
                    await ctx.send('\nYou have stepped on a trap\n')
                    if difficulty == 0:
                        ## easy
                        rand_loss = random.randint(1, 5)
                        curr_player_strength -= rand_loss
                        await ctx.send('\nYou have lost {} strength!'.format(rand_loss))
                    elif difficulty == 1:
                        ## medium
                        rand_loss = random.randint(3, 6)
                        curr_player_strength -= rand_loss
                        await ctx.send('\nYou have lost {} strength!'.format(rand_loss))
                    elif difficulty == 2:
                        ## hard
                        rand_loss = random.randint(5, 7)
                        curr_player_strength -= rand_loss
                        await ctx.send('\nYou have lost {} strength!'.format(rand_loss))
                    elif difficulty == 3:
                        ## very hard
                        rand_loss = random.randint(7, 8)
                        curr_player_strength -= rand_loss
                        await ctx.send('\nYou have lost {} strength!'.format(rand_loss))
                    if curr_player_strength <= 0:
                        ## player has lost
                        await ctx.send(
                            '\n{} has lost the game, their strength dropped to {}!'.format(ctx.message.author.mention,
                                                                                           curr_player_strength))
                        break
                    else:
                        board[curr_player_x][curr_player_y - 1] = 'S'
                        board[curr_player_x][curr_player_y] = 'o'
                        curr_player_y -= 1
                elif board[curr_player_x][curr_player_y-1] == '-' or board[curr_player_x][curr_player_y-1] == 'I':
                    ## trying to move into wall (expend strength to break through)
                    await ctx.send('\nYou are moving towards a wall!\n')
                    if difficulty == 0:
                        ## easy
                        expense = random.randint(1,4)
                        await ctx.send('\nYou can expend {} strength to break through the wall. (Y/N)?'.format(expense))
                        while True:
                            answer = await client.wait_for('message',check=lambda message: message.author == ctx.author)
                            try:
                                answer = str(answer.content)
                                if answer.upper() == 'Y':
                                    #yes
                                    if curr_player_strength < expense:
                                        await ctx.send('\nYour player does not have enough strength to expend to break through the wall\n')
                                        break
                                    else:
                                        curr_player_strength -= expense
                                        board[curr_player_x][curr_player_y-1] = 'S'
                                        board[curr_player_x][curr_player_y] = 'o'
                                        curr_player_y -= 1
                                        curr_player_strength -= 1
                                        break
                                elif answer.upper() == 'N':
                                    #no
                                    break
                                else:
                                    #invalid input
                                    await ctx.send('\Invalid input\n')
                            except Exception as e:
                                await ctx.send('\nInvalid input\n')
                                continue
                    elif difficulty == 1:
                        ## medium
                        expense = random.randint(2,5)
                        await ctx.send('\nYou can expend {} strength to break through the wall. (Y/N)?'.format(expense))
                        while True:
                            answer = await client.wait_for('message',check=lambda message: message.author == ctx.author)
                            try:
                                answer = str(answer.content)
                                if answer.upper() == 'Y':
                                    #yes
                                    if curr_player_strength < expense:
                                        await ctx.send('\nYour player does not have enough strength to expend to break through the wall\n')
                                        break
                                    else:
                                        curr_player_strength -= expense
                                        board[curr_player_x][curr_player_y-1] = 'S'
                                        board[curr_player_x][curr_player_y] = 'o'
                                        curr_player_y -= 1
                                        curr_player_strength -= 1
                                        break
                                elif answer.upper() == 'N':
                                    #no
                                    break
                                else:
                                    #invalid input
                                    await ctx.send('\Invalid input\n')
                            except Exception as e:
                                await ctx.send('\nInvalid input\n')
                                continue
                    elif difficulty == 2:
                        ## hard
                        expense = random.randint(3,6)
                        await ctx.send('\nYou can expend {} strength to break through the wall. (Y/N)?'.format(expense))
                        while True:
                            answer = await client.wait_for('message',check=lambda message: message.author == ctx.author)
                            try:
                                answer = str(answer.content)
                                if answer.upper() == 'Y':
                                    #yes
                                    if curr_player_strength < expense:
                                        await ctx.send('\nYour player does not have enough strength to expend to break through the wall\n')
                                        break
                                    else:
                                        curr_player_strength -= expense
                                        board[curr_player_x][curr_player_y-1] = 'S'
                                        board[curr_player_x][curr_player_y] = 'o'
                                        curr_player_y -= 1
                                        curr_player_strength -= 1
                                        break
                                elif answer.upper() == 'N':
                                    #no
                                    break
                                else:
                                    #invalid input
                                    await ctx.send('\Invalid input\n')
                            except Exception as e:
                                await ctx.send('\nInvalid input\n')
                                continue
                    elif difficulty == 3:
                        expense = random.randint(4,7)
                        await ctx.send('\nYou can expend {} strength to break through the wall. (Y/N)?'.format(expense))
                        while True:
                            answer = await client.wait_for('message',check=lambda message: message.author == ctx.author)
                            try:
                                answer = str(answer.content)
                                if answer.upper() == 'Y':
                                    #yes
                                    if curr_player_strength < expense:
                                        await ctx.send('\nYour player does not have enough strength to expend to break through the wall\n')
                                        break
                                    else:
                                        curr_player_strength -= expense
                                        board[curr_player_x][curr_player_y-1] = 'S'
                                        board[curr_player_x][curr_player_y] = 'o'
                                        curr_player_y -= 1
                                        curr_player_strength -= 1
                                        break
                                elif answer.upper() == 'N':
                                    #no
                                    break
                                else:
                                    #invalid input
                                    await ctx.send('\Invalid input\n')
                            except Exception as e:
                                await ctx.send('\nInvalid input\n')
                                continue
                else:
                    await ctx.send('\nSuccessful move, no objects on space\n')
                    board[curr_player_x][curr_player_y-1] = 'S'
                    board[curr_player_x][curr_player_y] = 'o'
                    curr_player_y -= 1
                    curr_player_strength -= 1
            elif answer == 'r':
                # move right
                if curr_player_y == len(board[0])-1:
                    ## trying to move out of bounds
                    await ctx.send('\nAttempting to move out of bounds of the board, choose another direction\n')
                elif board[curr_player_x][curr_player_y+1] == 'E':
                    ## reached ending
                    await ctx.send('\nYou have reached the ending!\n')
                    break
                elif board[curr_player_x][curr_player_y+1] == 'F':
                    ## moved onto food
                    await ctx.send('\nYou have reached a food object!\n')
                    if difficulty == 0:
                        ## easy
                        rand_food = random.randint(5,15)
                        await ctx.send('\nYour strength increases by {}!'.format(rand_food))
                        curr_player_strength += rand_food
                    elif difficulty == 1:
                        ## medium
                        rand_food = random.randint(4,13)
                        await ctx.send('\nYour strength increases by {}!'.format(rand_food))
                        curr_player_strength += rand_food
                    elif difficulty == 2:
                        ## hard
                        rand_food = random.randint(3,12)
                        await ctx.send('\nYour strength increases by {}!'.format(rand_food))
                        curr_player_strength += rand_food
                    elif difficulty == 3:
                        ## very hard
                        rand_food = random.randint(3,10)
                        await ctx.send('\nYour strenth increases by {}!'.format(rand_food))
                        curr_player_strength += rand_food
                    board[curr_player_x][curr_player_y + 1] = 'S'
                    board[curr_player_x][curr_player_y] = 'o'
                    curr_player_y += 1
                elif board[curr_player_x][curr_player_y+1] == 'T':
                    ## moved onto trap
                    await ctx.send('\nYou have stepped on a trap!\n')
                    if difficulty == 0:
                        ## easy
                        rand_loss = random.randint(1, 5)
                        curr_player_strength -= rand_loss
                        await ctx.send('\nYou have lost {} strength!'.format(rand_loss))
                    elif difficulty == 1:
                        ## medium
                        rand_loss = random.randint(3, 6)
                        curr_player_strength -= rand_loss
                        await ctx.send('\nYou have lost {} strength!'.format(rand_loss))
                    elif difficulty == 2:
                        ## hard
                        rand_loss = random.randint(5, 7)
                        curr_player_strength -= rand_loss
                        await ctx.send('\nYou have lost {} strength!'.format(rand_loss))
                    elif difficulty == 3:
                        ## very hard
                        rand_loss = random.randint(7, 8)
                        curr_player_strength -= rand_loss
                        await ctx.send('\nYou have lost {} strength!'.format(rand_loss))
                    if curr_player_strength <= 0:
                        ## player has lost
                        await ctx.send(
                            '\n{} has lost the game, their strength dropped to {}!'.format(ctx.message.author.mention,
                                                                                           curr_player_strength))
                        break
                    else:
                        board[curr_player_x][curr_player_y + 1] = 'S'
                        board[curr_player_x][curr_player_y] = 'o'
                        curr_player_y += 1
                elif board[curr_player_x][curr_player_y+1] == '-' or board[curr_player_x][curr_player_y+1] == 'I':
                    ## trying to move into wall (expend strength to break through)
                    await ctx.send('\nYou are moving towards a wall!\n')
                    if difficulty == 0:
                        ## easy
                        expense = random.randint(1,4)
                        await ctx.send('\nYou can expend {} strength to break through the wall. (Y/N)?'.format(expense))
                        while True:
                            answer = await client.wait_for('message',check=lambda message: message.author == ctx.author)
                            try:
                                answer = str(answer.content)
                                if answer.upper() == 'Y':
                                    #yes
                                    if curr_player_strength < expense:
                                        await ctx.send('\nYour player does not have enough strength to expend to break through the wall\n')
                                        break
                                    else:
                                        curr_player_strength -= expense
                                        board[curr_player_x][curr_player_y + 1] = 'S'
                                        board[curr_player_x][curr_player_y] = 'o'
                                        curr_player_y += 1
                                        curr_player_strength -= 1
                                        break
                                elif answer.upper() == 'N':
                                    #no
                                    break
                                else:
                                    #invalid input
                                    await ctx.send('\Invalid input\n')
                            except Exception as e:
                                await ctx.send('\nInvalid input\n')
                                continue
                    elif difficulty == 1:
                        ## medium
                        expense = random.randint(2,5)
                        await ctx.send('\nYou can expend {} strength to break through the wall. (Y/N)?'.format(expense))
                        while True:
                            answer = await client.wait_for('message',check=lambda message: message.author == ctx.author)
                            try:
                                answer = str(answer.content)
                                if answer.upper() == 'Y':
                                    #yes
                                    if curr_player_strength < expense:
                                        await ctx.send('\nYour player does not have enough strength to expend to break through the wall\n')
                                        break
                                    else:
                                        curr_player_strength -= expense
                                        board[curr_player_x][curr_player_y + 1] = 'S'
                                        board[curr_player_x][curr_player_y] = 'o'
                                        curr_player_y += 1
                                        curr_player_strength -= 1
                                        break
                                elif answer.upper() == 'N':
                                    #no
                                    break
                                else:
                                    #invalid input
                                    await ctx.send('\Invalid input\n')
                            except Exception as e:
                                await ctx.send('\nInvalid input\n')
                                continue
                    elif difficulty == 2:
                        ## hard
                        expense = random.randint(3,6)
                        await ctx.send('\nYou can expend {} strength to break through the wall. (Y/N)?'.format(expense))
                        while True:
                            answer = await client.wait_for('message',check=lambda message: message.author == ctx.author)
                            try:
                                answer = str(answer.content)
                                if answer.upper() == 'Y':
                                    #yes
                                    if curr_player_strength < expense:
                                        await ctx.send('\nYour player does not have enough strength to expend to break through the wall\n')
                                        break
                                    else:
                                        curr_player_strength -= expense
                                        board[curr_player_x][curr_player_y + 1] = 'S'
                                        board[curr_player_x][curr_player_y] = 'o'
                                        curr_player_y += 1
                                        curr_player_strength -= 1
                                        break
                                elif answer.upper() == 'N':
                                    #no
                                    break
                                else:
                                    #invalid input
                                    await ctx.send('\Invalid input\n')
                            except Exception as e:
                                await ctx.send('\nInvalid input\n')
                                continue
                    elif difficulty == 3:
                        expense = random.randint(4,7)
                        await ctx.send('\nYou can expend {} strength to break through the wall. (Y/N)?'.format(expense))
                        while True:
                            answer = await client.wait_for('message',check=lambda message: message.author == ctx.author)
                            try:
                                answer = str(answer.content)
                                if answer.upper() == 'Y':
                                    #yes
                                    if curr_player_strength < expense:
                                        await ctx.send('\nYour player does not have enough strength to expend to break through the wall\n')
                                        break
                                    else:
                                        curr_player_strength -= expense
                                        board[curr_player_x][curr_player_y + 1] = 'S'
                                        board[curr_player_x][curr_player_y] = 'o'
                                        curr_player_y += 1
                                        curr_player_strength -= 1
                                        break
                                elif answer.upper() == 'N':
                                    #no
                                    break
                                else:
                                    #invalid input
                                    await ctx.send('\Invalid input\n')
                            except Exception as e:
                                await ctx.send('\nInvalid input\n')
                                continue
                else:
                    await ctx.send('\nSuccessful move, no objects on space\n')
                    board[curr_player_x][curr_player_y+1] = 'S'
                    board[curr_player_x][curr_player_y] = 'o'
                    curr_player_y += 1
                    curr_player_strength -= 1
            else:
                await ctx.send('\nEnter valid input\n')
        except Exception as e:
            await ctx.send('\nEnter valid input\n')


async def hand_sum_blackjackv2(ctx,hand):
    total = 0
    for eachcard in hand:
        if 'Ace' in eachcard:
            while True:
                await ctx.send('\nTurn the ace into an 11 or 1?')
                answer = await client.wait_for('message',check=lambda message: message.author == ctx.author)
                if answer.content == '11':
                    ## 11
                    total += 11
                    break
                elif answer.content == '1':
                    ## 1
                    total += 1
                    break
                else:
                    ## invalid input
                    await ctx.send('\nInvalid input\n')
        elif 'Queen' in eachcard:
            total += 10
        elif 'King' in eachcard:
            total += 10
        elif 'Jack' in eachcard:
            total += 10
        else:
            total += int(eachcard.split(' ')[0])
    return total

def hand_sum_computer_blackjackv2(hand):
    total = 0
    for eachcard in hand:
        if 'Ace' in eachcard:
            if total + 11 > 21:
                total += 1
            else:
                total += 11
        elif 'Queen' in eachcard:
            total += 10
        elif 'King' in eachcard:
            total += 10
        elif 'Jack' in eachcard:
            total += 10
        else:
            total += int(eachcard.split(' ')[0])
    return total

@client.command(aliases=['blackjack'])
async def blackjackv_two(ctx):
    await ctx.send('\nWelcome to blackjack! Rules are : \n1)Both players get dealt two cards\n2)Both players choose whether to stay or hit\n3)If both players stay, then the showdown commences\n4)Both players show their hands, and whoever is closer to 21 wins! If both players are tied, then it is a draw!\n5)At the end of the game(whenever the player chooses to end the program), the scores are tallied, and the player with the higher amount of wins, wins!\n6)A win is deducted for every loss as well')
    player_wins = 0
    computer_wins = 0
    first_game = False
    end_game = False
    while True:
        if first_game:
            ## first game has been played
            await ctx.send('\nTotal wins : COMPUTER {} | PLAYER {}'.format(computer_wins,player_wins))
            while True:
                await ctx.send('\nKeep playing? Y|N?')
                answer = await client.wait_for('message',check= lambda message: message.author == ctx.author)
                if answer.content.lower() == 'yes' or answer.content.lower() == 'y':
                    ## yes
                    break
                elif len(answer.content) == 'no' or answer.content.lower() == 'n':
                    ## no
                    end_game = True
                else:
                    ## default to yes
                    break
        if end_game:
            break

        player_hand = []
        player_total = 0
        computer_hand = []
        computer_total = 0
        stands = False


        # generate deck
        deck = generate_deck()
        await ctx.send('\nThe deck has been generated!\nShuffling seven times then dealing two cards to both players')
        # player input
        for i in range(7):
            deck = shuffle(deck)
        # dealing to player's hand
        card,deck = deal(deck)
        player_hand.append(card)
        card,deck = deal(deck)
        player_hand.append(card)

        # dealing to computer's hand

        card,deck = deal(deck)
        computer_hand.append(card)
        card,deck = deal(deck)
        computer_hand.append(card)
        await ctx.send('\nDealt hand is : {}'.format(player_hand))
        player_total = await hand_sum_blackjackv2(ctx,player_hand)
        computer_total = hand_sum_computer_blackjackv2(computer_hand)

        while True:
            if not first_game:
                first_game = True
            await ctx.send('\nPlayer goes first!\nWhat is your choice? (hit/stand)[Total : {}]'.format(player_total))
            answer = await client.wait_for('message',check=lambda message: message.author == ctx.author)
            answer = answer.content
            if type(answer) != str:
                await ctx.send('\nInvalid input\n')
                continue
            elif answer.lower() == 'hit':
                player_total = 0
                ## have to deal to player's hand
                card,deck = deal(deck)
                await ctx.send('\nYou have been dealt a {}'.format(card))
                player_hand.append(card)
                for i in range(len(player_hand)):
                    if 'Ace' in player_hand[i]:
                        while True:
                            await ctx.send('\nDo you want to transform the Ace into a 1 or 11(y/n)')
                            answer = await client.wait_for('message',check=lambda message: message.author == ctx.author)
                            answer = answer.content
                            if answer.lower() == '1':
                                # change ace to 1
                                print('')
                                player_total += 1
                                await ctx.send('\nYou have changed the Ace to an 1!')
                                break
                            elif answer.lower() == '11':
                                # change ace to 11
                                player_total += 11
                                await ctx.send('\nYou have changed the Ace to an 11!\n')
                                break
                            else:
                                await ctx.send('\nInvalid input\n')
                    else:
                        if 'King' in player_hand[i]:
                            player_total += 10
                        elif 'Queen' in player_hand[i]:
                            player_total += 10
                        elif 'Jack' in player_hand[i]:
                            player_total += 10
                        else:
                            player_total += int(player_hand[i].split(' ')[0])
                if player_total > 21:
                    ## player loses
                    await ctx.send('\nPlayer\'s hand goes over 21! Player loses!')
                    computer_wins += 1
                    break
                else:
                    await ctx.send('\nPlayer\'s total is : {}'.format(player_total))
                # player chose hit
            elif answer.lower() == 'stand':
                # player chose stand
                await ctx.send('\nPlayer stands!\n')
                if stands:
                    ## showdown
                    if player_total > computer_total:
                        ## player wins
                        await ctx.send('\n{} wins!'.format(ctx.message.author.mention))
                        player_wins += 1
                        break
                    else:
                        ## computer wins
                        await ctx.send('\n{} wins!'.format(client.user.display_name))
                        computer_wins += 1
                        break
                else:
                    stands = True
                #break
            else:
                await ctx.send('\nInvalid input\n')

            await ctx.send('\nComputer choosing their move!')

            ## generate probability of 21 in player's hand

            if stands and computer_total > player_total:
                await ctx.send('\n{} stands! {} wins!'.format(client.user.display_name,client.user.display_name))
                computer_wins += 1
                break

            user_probability = 0
            for eachcard in deck:
                if 'Queen' in eachcard:
                    if 10 + player_total == 21:
                        user_probability += 1
                elif 'King' in eachcard:
                    if 10 + player_total == 21:
                        user_probability += 1
                elif 'Jack' in eachcard:
                    if 10 + player_total == 21:
                        user_probability += 1
                elif 'Ace' in eachcard:
                    if 10 + player_total == 21 or 1 + player_total == 21:
                        user_probability += 1
                else:
                    if int(eachcard.split(' ')[0]) + player_total == 21:
                        user_probability += 1
            user_probability = (user_probability / len(deck)) * 100
            cpu_probability = 0

            print('user probability = {}'.format(user_probability))
            if user_probability > 25:
                ## generate random number to decide whether to stand or call
                print('')
                rand_number = random.randint(1,102313012)
                if _is_prime(rand_number):
                    ## even - stand
                    await ctx.send('{} stands'.format(client.user.display_name))
                    if stands:
                        ## showdown
                        result = computer_total > player_total
                        if result:
                            ## computer wins
                            await ctx.send('\n{} wins!'.format(client.user.display_name))
                            computer_wins += 1
                            break
                        else:
                            ## player wins
                            await ctx.send('\n{} wins!'.format(ctx.message.author.mention))
                            player_wins += 1
                            break
                    else:
                        stands = True
                else:
                    ## odd - call
                    computer_total = 0
                    await ctx.send('{} calls'.format(client.user.display_name))
                    card,deck = deal(deck)
                    computer_hand.append(card)
                    ## generate cpu sum
                    for i in range(len(computer_hand)):
                        if 'Ace' in computer_hand[i]:
                            if computer_total + 11 > 21:
                                ## make it deal a 1
                                computer_total += 1
                            else:
                                computer_total += 11
                        elif 'Queen' in computer_hand[i]:
                            computer_total += 10
                        elif 'King' in computer_hand[i]:
                            computer_total += 10
                        elif 'Jack' in computer_hand[i]:
                            computer_total += 10
                        else:
                            computer_total += int(computer_hand[i].split(' ')[0])
                    if computer_total > 21:
                        ## computer busts, game ends
                        await ctx.send('{}\'s total goes over 21, {} wins!'.format(client.user.display_name,ctx.message.author.mention))
                        player_wins += 1
                        break
                    stands = False
            else:
                ## generate cpu_probability to decide whether to stand or call

                for eachcard in deck:
                    if 'Ace' in eachcard:
                        if 1 + computer_total == 21:
                            cpu_probability += 1
                        elif 11 + computer_total == 21:
                            cpu_probability += 1
                    elif 'Queen' in eachcard:
                        if 10 + computer_total == 21:
                            cpu_probability += 1
                    elif 'King' in eachcard:
                        if 10 + computer_total == 21:
                            cpu_probability += 1
                    elif 'Jack' in eachcard:
                        if 10 + computer_total == 21:
                            cpu_probability += 1
                    else:
                        if int(eachcard.split(' ')[0]) + computer_total == 21:
                            cpu_probability += 1
                cpu_probability = (cpu_probability / len(deck)) * 100
                print('cpu probability = {}'.format(cpu_probability))
                if cpu_probability > 15 or (stands and computer_total < player_total):
                    ## call
                    await ctx.send('\n{} calls'.format(client.user.display_name))
                    card,deck = deal(deck)
                    computer_hand.append(card)
                    ## generate cpu sum
                    computer_total = 0

                    for i in range(len(computer_hand)):
                        if 'Ace' in computer_hand[i]:
                            if computer_total + 11 > 21:
                                ## make it deal a 1
                                computer_total += 1
                            else:
                                computer_total += 11
                        elif 'Queen' in computer_hand[i]:
                            computer_total += 10
                        elif 'King' in computer_hand[i]:
                            computer_total += 10
                        elif 'Jack' in computer_hand[i]:
                            computer_total += 10
                        else:
                            computer_total += int(computer_hand[i].split(' ')[0])
                    if computer_total > 21:
                        ## computer busts, game ends
                        await ctx.send('{}\'s total goes over 21, {} wins!'.format(client.user.display_name,ctx.message.author.mention))
                        player_wins += 1
                        break
                    stands = False
                else:
                    ## stand
                    await ctx.send('\n{} stands'.format(client.user.display_name))
                    if stands:
                        ## showdown
                        if computer_total > player_total:
                         ## computer wins
                            await ctx.send('\n{} wins!'.format(client.user.display_name))
                            computer_wins += 1
                            break
                        else:
                            ## player wins
                            await ctx.send('\n{} wins!'.format(ctx.message.author.mention))
                            player_wins += 1
                            break
                    else:
                        stands = True
                    continue
            print('Computer total = {}'.format(computer_total))







        # computer input


@client.command(aliases=['database'])
async def database_access(ctx):

    client1 = pymongo.MongoClient(get_conn_string())

    await ctx.send('Enter the name of the database to access')

    while True:
        answer = await client.wait_for('message',check= lambda message: message.author == ctx.author)
        break

    try:
        db = client1['{}'.format(answer.content)]
        list_coll = db.list_collection_names()
        await ctx.send('List of collection names is : {}'.format(' '.join(list_coll)))
    except Exception as e:
        print('Exception handled')


@client.command(aliases=['guessword'])
async def guess_word(ctx):



    the_soup = bs4.BeautifulSoup(requests.get('https://randomword.com/').content,'html.parser')

    divs = the_soup.find_all('div')

    words = []

    for eachdiv in divs:
        try:
            if eachdiv['id'] == 'random_word':
                words.append(eachdiv.string)
        except Exception as e:
            continue

    the_guess_word = words[0]

    pprint(the_guess_word)
    empty_word = ['<>'] * len(the_guess_word)
    pprint(empty_word)

    await ctx.send('Random word has been generated! Time to guess the word, each <> representes an letter')

    guesses = 0

    while True:

        await ctx.send('Guesses : {}'.format(guesses))
        await ctx.send(' '.join(empty_word))
        if empty_word.count('<>') == 0:
            ## player has won!
            await ctx.send('You have won with {} guesses'.format(guesses))
            break

        while True:

            await ctx.send('Guess a letter!')
            answer = await client.wait_for('message',check= lambda message : message.author == ctx.author)
            guesses += 1
            answer = answer.content
            if not answer.isalpha() or len(answer) > 1:
                ## invalid input
                await ctx.send('invalid input')
                continue
            else:
                break

        for i in range(len(the_guess_word)):
            if the_guess_word[i] == answer:
                empty_word[i] = answer


def sort_cards(card):
    cards = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, 'Jack': 10, 'Queen': 11, 'King': 12, 'Ace': 13}
    return cards[card.split(' ')[0]]

@client.command(aliases=['99'])
async def ninety_nine(ctx):
    spec_cards = {'Jack': 11, 'Queen': 12}

    """

    :param ctx:
    :return:
    Game rules: point total starts at 0, and then the deck is split to each player, each player puts down one card in the pot
    Exceptions:
        4 : reverses play, meaning that the player who played it goes again
        9 : pass, the player who played it, the point total does not go up
        10: subtracts 10 points from total
        King : takes the total automatically to 99
        Ace : adds either 1 or 11 points
    """

    player_wins = 0
    computer_wins = 0

    await ctx.send('Welcome to the game of 99!\nThe rules are : Game rules: point total starts at 0, and then the deck is split to each player, each player puts down one card in the pot\nExceptions:\n4 : reverses play, meaning that the player who played it goes again\n9 : pass, the player who played it, the point total does not go up\n10: subtracts 10 points from total\nKing : takes the total automatically to 99\nAce : adds either 1 or 11 points\n')

    ## displayed rules, now deal cards

    while True:
        await ctx.send('Beginning game')

        await ctx.send('\nShuffling deck\n')

        deck = generate_deck()

        for i in range(random.randint(7,50)):
            deck = shuffle(deck)
        ## split deck to each player

        player_hand = []
        computer_hand = []

        for i in range(len(deck)//2):
            card,deck = deal(deck)
            player_hand.append(card)
        for i in range(len(deck)):
            card,deck = deal(deck)
            computer_hand.append(card)

        player_hand = sorted(player_hand, key = sort_cards)

        ### deck has been split

        total_points = 0

        cards_at_disposal = {}

        while True:
            ## main game loop

            await ctx.send('\nTotal points : {}\n'.format(total_points))

            ## generate player cards at their disposal
            for eachcard in player_hand:
                rank = eachcard.split(' ')[0]
                if rank not in cards_at_disposal:
                    cards_at_disposal[rank] = 1
                else:
                    cards_at_disposal[rank] = cards_at_disposal[rank] + 1
            ## collected cards at disposal
            disposal_string = '--- CARDS AT DISPOSAL : {}---\n'.format(len(player_hand))
            for eachkey in cards_at_disposal:
                disposal_string += '{} : {}\n'.format(eachkey,cards_at_disposal[eachkey])
            await ctx.send(disposal_string)

            while True:
                await ctx.send('\nEnter card to play\n')
                answer = await client.wait_for('message',check= lambda message: message.author == ctx.author)
                answer = answer.content
                if answer not in cards_at_disposal:
                    ## invalid answer
                    await ctx.send('invalid answer')
                else:
                    break

            card_list = [x for x in player_hand if answer in x]
            player_hand.remove(card_list[0])
            cards_at_disposal = {}

            if answer == '4':
                await ctx.send('{} passes with playing 4!'.format(ctx.message.author.mention))
            elif answer == '9':
                await ctx.send('{} passes with playing 9!'.format(ctx.message.author.mention))
            elif answer == '10':
                await ctx.send('{} reduces the total by 10 points by playing 10!'.format(ctx.message.author.mention))
                if total_points < 10:
                    total_points = 0
                else:
                    total_points -= 10
            elif answer == 'King':
                await ctx.send('{} takes the total immediately to 99 by playing King!'.format(ctx.message.author.mention))
                total_points = 99
            elif answer == 'Ace':
                ## check if user wants to play 1 or 11
                while True:
                    await ctx.send('\nEnter 1 or 11 to play the ace with that point value')
                    answer = await client.wait_for('message',check=lambda message: message.author == ctx.author)
                    answer = answer.content
                    try:
                        answer = int(answer)
                        if answer != 1 and answer != 11:
                            await ctx.send('\nInvalid answer\n')
                        else:
                            if answer == 1:
                                await ctx.send('\n{} plays ace with a point value of 1!'.format(ctx.message.author.mention))
                                total_points += 1
                            else:
                                await ctx.send('\n{} plays ace with a point value of 11!'.format(ctx.message.author.mention))
                                total_points += 11
                    except Exception as e:
                        ## invalid answer
                        await ctx.send("\nInvalid answer\n")
            else:
                total_points += int(answer)

            await ctx.send('\nComputer turn\n')

            """
            Save 4's and 10's, go for King's immediately, save Ace's, if no kings available, go for number cards not 4s, 10s, and Aces
            
            """

            num_fours = [x for x in computer_hand if '4' in x]
            num_tens = [x for x in computer_hand if '10' in x]
            num_kings = [x for x in computer_hand if 'King' in x]
            num_aces = [x for x in computer_hand if 'Ace' in x]
            num_nums = [x for x in computer_hand if '4' not in x and '10' not in x and 'King' not in x and 'Ace' not in x]
            found_num_card = False

            if len(num_kings) > 0:
                ## play king
                await ctx.send('\nComputer plays King! Total goes to 99')
                total_points = 99
                computer_hand.remove(num_kings[0])
            elif len(num_nums) > 0 and total_points != 99:
                ## play number card, randomly place
                for i in range(len(num_nums)):
                    found_num_card = False
                    card = num_nums[i]
                    rank = card.split(' ')[0]
                    if rank in spec_cards:
                        play_value = spec_cards[rank]
                    else:
                        play_value = int(rank)
                    if total_points + play_value <= 99:
                        ## valid card
                        found_num_card = True
                        break
                if not found_num_card and len(num_kings) == 0 and len(num_fours) == 0 and len(num_tens) == 0:
                    if len(num_aces) > 0:
                        ## verify if ace is applicable
                        print('')
                    else:
                        ## no aces, no valid cards
                        ## player wins
                        await ctx.send('\nPlayer wins!\n')
                        break ## begin another round
                else:
                    print('card = {}'.format(card))
                    total_points += play_value
                    computer_hand.remove(card)
            elif len(num_fours) > 0:
                ## play four card
                rand_card = random.choice(num_fours)
                computer_hand.remove(rand_card)
                await ctx.send('\nComputer skips turn via playing 4')
            elif len(num_tens) > 0:
                ## play ten card
                rand_card = random.choice(num_tens)
                computer_hand.remove(rand_card)
                await ctx.send('\nComputer skips turn via playing 10')
            elif len(num_aces) > 0:
                ## play ace
                if total_points + 11 <= 99:
                    ## play 11
                    rand_card = random.choice(num_aces)
                    total_points += 11
                    computer_hand.remove(rand_card)
                    await ctx.send('\nComputer decided to play ace with point value of 11')
                elif total_points + 1 <= 99:
                    ## play 1
                    rand_card = random.choice(num_aces)
                    total_points += 1
                    computer_hand.remove(rand_card)
                    await ctx.send('\nComputer decided to play ace as 1 point value')
                else:
                    ## player wins!
                    await ctx.send('Player wins!')
                    player_wins += 1
                    break






























client.run(get_token()) ## make sure to delete before committing