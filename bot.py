import telebot
from random import choice
from basicfunction import assign_roles, notify_users, WereWolfAction, seerAction, robberAction, troubleMakerAction, drunkAction,insomniacAction,masonsAction
TOKEN = '788644730:AAGj0SoF2lq6bHjpDy8DOL8znIE_EJ4XebQ'
bot = telebot.TeleBot(TOKEN)
URL = 'http://api.telegram.org/bot{0}/getUpdates'.format(TOKEN)
players = {} #Id and Player name
player_in_game = {} #ID and Game name
game = False
player_card={}# Original cards
end_card={}#Cards with the changes
cards_in_the_center=[]
start = False
list_of_games=[] #Number of games
url_audio='Prueba.ogg'
##############################################
werewolf=False
seer=False
seer_center=False
seer_player=False
robber=False
troubleMaker=False
drunk=False
##############################################
@bot.message_handler(commands=['start'])
def hello(message):
    global players
    global start
    global game
    global player_in_game
    start = True
    players.update({message.chat.id: message.chat.first_name})
    bot.send_message(message.chat.id, 'Introduce the game name')
    while(game is False):
        pass
    game = False
    bot.send_message(message.chat.id, 'The players are: ')
    for element in players:
        if player_in_game[element] == player_in_game[message.chat.id]:
            bot.send_message(message.chat.id, players[element])
        else:
            pass
    notify_user(message.chat.first_name, message.chat.id,
                player_in_game[message.chat.id])
    start = False
    with open(url_audio,'rb') as audio:
        bot.send_audio(message.chat.id,audio)



def notify_user(player_name, key_current_user, game_name):
    for key, value in players.items():
        if key is not key_current_user and player_in_game[key] == game_name:
            bot.send_message(key, 'New player '+player_name+' has joined')
        else:
            pass

@bot.message_handler(commands=['end'] )
def endGame(message):
    notify_users(end_card,players,bot)
    pass
def get_game_name(message):
    global list_of_games
    game=message.text.split(' ')[0]
    if game not in list_of_games: 
        list_of_games.append(game)
    return game


def add_player_to_a_game(message, game_name):
    global player_in_game
    player_in_game.update({message.chat.id: game_name})
########Seer################################################
@bot.message_handler(func=lambda message: True and seer is True)
def lookOtherCards(message):
    global seer_center,seer_player
    global seer

    try:
        option=int(message.text)
        if option is 1:
            bot.send_message(message.chat.id,'You have selected to look two cards from the center')
            seer_center=True
            seer=False
            bot.send_message(message.chat.id,'Enter a number between 1-3')
        if option is 2:
            bot.send_message(message.chat.id,'You have selected to look one player card.')
            bot.send_message(message.chat.id,'Send the name of the player you want to look the card')
            bot.send_message(message.chat.id,'The players are:')
            for key,player in players.items():
                if key is not message.chat.id:#Arreglar esta mierda
                    bot.send_message(message.chat.id,player)
                    seer=False
                    seer_player=True
    except ValueError as identifier:
        bot.send_message(message.chat.id,'Incorrect value, choose between 1 and 2')

cont_seer=0
@bot.message_handler(func=lambda message: True and seer_player is True)
def look_for_a_card(message):
    global seer_player,seer
    correct=False
    for key,value in players.items():
        if value==message.text:
            correct=True
            bot.send_message(message.chat.id,'The card of '+str(value)+" was a "+player_card.get(key))
    if correct is True:
        seer_player=False
        bot.send_message(message.chat.id,'Your turn has ended')
    else:
        bot.send_message(message.chat.id,'Incorrect player name, please write one name from the list')

@bot.message_handler(func=lambda message: True and seer_center is True)
def read_from_the_center(message):
    global cont_seer
    global seer_center
    try:
        number=int(message.text)-1
        bot.send_message(message.chat.id,'The card is a '+cards_in_the_center[number])
        cont_seer+=1
        if cont_seer is 2:
            seer_center=False
            bot.send_message(message.chat.id,'Your tourn has ended')
        
    except ValueError as identifier:
        bot.send_message(message.chat.id,'')

############################################################################################
#TroubleMaker
players_troublemaker=[]
@bot.message_handler(func=lambda message: True and troubleMaker is True)
def troubleMakerMessage(message):
    global troubleMaker
    global players_troublemaker
    global end_card
    correct=False
    if len(players_troublemaker) is not 2:
        for key,value in players.items():
            if value==message.text:
                players_troublemaker.append(key)
                correct=True
                if len(players_troublemaker) is 2:
                    troubleMakerMessage(message)
                elif len(players_troublemaker) is 1:
                    bot.send_message(message.chat.id,"You have to select another player card.")
            
        #bot.send_message(message.chat.id,'Queda 1')
    else:
        troubleMaker=False
        correct=True
        card=end_card.get(players_troublemaker[0])
        end_card.update({players_troublemaker[0]:end_card.get(players_troublemaker[1])})
        end_card.update({players_troublemaker[1]:card})
        bot.send_message(message.chat.id,'Your tourn is has ended')
    if correct is False:
        bot.send_message(message.chat.id,"Wrong name")

############################################################################################
#Robber
@bot.message_handler(func=lambda message: True and robber is True)
def robberSelection(message):
    global robber,end_card
    for key,value in players.items():
        if value==message.text:
            card=end_card.get(key)
            end_card.update({key:end_card.get(message.chat.id)})
            end_card.update({message.chat.id:card})
            bot.send_message(message.chat.id,"You are now a "+end_card.get(message.chat.id))
            robber=False

############################################################################################
#Drunk
@bot.message_handler(func=lambda message: True and drunk is True)
def drunkChange(message):
    global drunk
    global cards_in_the_center,end_card
    try:
        number=int(message.text)-1
        card=cards_in_the_center[number]
        cards_in_the_center[number]=end_card.get(message.chat.id)
        end_card.update({message.chat.id:card})
        drunk=False
    except ValueError:
        bot.send_message(message.chat.id,"Incorrect value")
        pass
############################################################################################
#Werewolf action need to be parched
@bot.message_handler(func=lambda message: True and werewolf is True)
def selectCard(message):
    global werewolf
    try:
        number=int(message.text)-1
        bot.send_message(message.chat.id,'The card is a '+cards_in_the_center[number])
        werewolf=False
        if seer is False:
            bot.send_message(message.chat.id,'Your tourn has end')
        
    except:
        bot.send_message(message.chat.id,'Incorrect value enter a number between 1-3')
@bot.message_handler(func=lambda message: True and game is False and start is True)
def handling_messages(message):
    global game
    game_name = get_game_name(message)
    add_player_to_a_game(message, game_name)
    bot.send_message(message.chat.id, ' Hello player ' +
                     message.chat.first_name+' welcome to the game '+game_name)
    game = True

@bot.message_handler(commands=['Go'])
def dividePlayersIntoGames(message):
    global werewolf,seer,robber,troubleMaker,drunk
    global cards_in_the_center,player_card,end_card
    cards_in_the_center={}
    if len(player_in_game)>=4: # Must be edited
        player_roles_each_game=[]
        game_list=[]
        for game in list_of_games:
            game_list.append(game)
            for key,value in player_in_game.items():
                if game == value:
                    game_list.append(key)
            player_roles_each_game.append(game_list)
            game_list=[]
        for element in player_roles_each_game:
            player_card=assign_roles(element,bot)
            end_card=player_card.copy()
            werewolf,cards_in_the_center= WereWolfAction(players,bot)
            while werewolf is True:
                pass
            masonsAction(players,bot,player_card)
            seer,cards_in_the_center=seerAction(players,bot)
            while seer is True or seer_center is True or seer_player is True:
                pass
            robber=robberAction(players,bot)
            while robber is True:
                pass
            troubleMaker=troubleMakerAction(players,bot)
            while troubleMaker is True:
                pass
            drunk=drunkAction(players,bot)
            while drunk is True:
                pass
            insomniacAction(players,bot,end_card)
    else:
        print('Error')


def filter_players(game):
    auxiliary_dictionary_of_players={}
    for key,value in player_in_game.items():
        if value==game:
            auxiliary_dictionary_of_players.update({key:value})
    return auxiliary_dictionary_of_players

def select_card_for_each_player(auxiliary_dictionary,auxiliary_cards):
    for index in range(0,len(player_in_game.items())+3):
        if len(auxiliary_cards)==3:
            break
        key,value=choice(list(auxiliary_dictionary.items()))
        auxiliary_dictionary.pop(key)
        key_card,value_card=choice(list(auxiliary_cards.items()))
        auxiliary_cards.pop(key_card)
        bot.send_message(key,'Your card is a '+ key_card)

if __name__ == "__main__":
    bot.polling()
