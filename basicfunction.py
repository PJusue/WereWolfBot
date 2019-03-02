from random import choice
cards={'WereWolf':'','Seer':'','Rober':'','TroubleMaker':'','Mason':'','Minion':'','Drunk':'','Villager':''}
player_card={}
cards_in_the_center=[]
def assign_roles(players_in_one_game,bot):
    global player_card
    global cards_in_the_center
    new_cards_list=cards_in_play(len(players_in_one_game)-1)
    for element in players_in_one_game[1:]:
        key_card,card=choice(list(new_cards_list.items()))
        player_card.update({element:key_card})
        bot.send_message(element,key_card)
        new_cards_list.pop(key_card)
    for index in range(0,3,1):
        key_card_center,card_center=choice(list(new_cards_list.items()))
        cards_in_the_center.append(key_card_center)
        new_cards_list.pop(key_card_center)
        bot.send_message(12557094,"The card "+ key_card_center+ 'was added to the center')
    return player_card
def notify_users(players,player_names,bot):
    for key,value in players.items():
        for key1,value1 in player_names.items():
            bot.send_message(key1,"The player "+player_names.get(key)+" is a "+value)


def seerAction(list_players,bot):
    global cards_in_the_center
    seer=0
    for key,value in player_card.items():
        if value=='Seer':
            seer=key
            bot.send_message(seer,'You are the seer.')
            bot.send_message(seer,'You can select to see two cards of the center or one of the other player')
            bot.send_message(seer,'Send 1 for look two cards of the center and 2 for look at one player card')
            return True,cards_in_the_center
        else:
            pass
    return False,cards_in_the_center

def robberAction(list_players,bot):
    for key,value in player_card.items():
        if value =='Robber':
            bot.send_message(key,'You are the robber, please select the player you want to steal his/her card')
            bot.send_message(key,'Send the name of the player you want to look the card')
            bot.send_message(key,'The players are:')
            print(list_players)
            for key1,player in list_players.items():
        #if key is not message.chat.id:#Arreglar esta mierda
                bot.send_message(key,player)
            return True
    return False

def drunkAction(list_players,bot):
    for key,value in player_card.items():
        if value=='Drunk':
            bot.send_message(key,'You are the drunk, please change your card with one in the center')
            bot.send_message(key,'Enter 1, 2 or 3 for select the card in the center.')
            return True
    return False
def troubleMakerAction(list_players,bot):
    for key,value in player_card.items():
        if value=='TroubleMaker':
            bot.send_message(key,'You are the troublemaker, please change the cards of two OTHER players')
            bot.send_message(key,'The players are:')
            print(list_players)
            for key1,player in list_players.items():
        #if key is not message.chat.id:#Arreglar esta mierda
                bot.send_message(key,player)
            return True
    return False

def insomniacAction(list_players,bot,end_cards):
    for key,value in player_card.items():
        if value=='Insomniac':
            bot.send_message(key,'Now you are the '+end_cards.get(key))

def masonsAction(list_players,bot,player_card):
    mason=[]
    for key,value in player_card.items():
        if value=='Mason' or value=='MaSon':
            mason.append(key)
            if len(mason) is 2:
                bot.send_message(mason[1],'The other mason is '+list_players.get(mason[0]))
                bot.send_message(mason[0],'The other mason is '+list_players.get(mason[1]))
    if len(mason) is 1:
        bot.send_message(mason[0],'You are the only mason')
def WereWolfAction(list_players,bot):
    werewolfs=[]  
    global cards_in_the_center
    minion=0
    for key,value in player_card.items():
        if value =='Werewolf' or value=='WereWolf':
            werewolfs.append(key)
        elif value=='Minion':
            minion=key
    if len(werewolfs)==2:
        bot.send_message(werewolfs[0],'The user '+list_players.get(werewolfs[1])+' is a wolf')
        bot.send_message(werewolfs[1],'The user '+list_players.get(werewolfs[0])+' is a wolf')
        if minion is not 0:
            bot.send_message(minion,'The users '+list_players.get(werewolfs[0])+' and '+list_players.get(werewolfs[1]))
        return False,cards_in_the_center
    elif len(werewolfs)==1:
        bot.send_message(werewolfs[0],'You are the only wolf')
        bot.send_message(werewolfs[0],'enter a number between 1-3')
        if minion is not 0:
            bot.send_message(minion,'The user '+list_players.get(werewolfs[0])+' is a wolf')
        return True,cards_in_the_center
    else:
        bot.send_message(12557094,'There are not wolfs')
        return False,cards_in_the_center


#Depends of the number of player it selects different cards
def cards_in_play(number_of_players):
    cards_in_the_game={}
    cards_in_the_game.update({'Werewolf':''})
    cards_in_the_game.update({'WereWolf':''})
    cards_in_the_game.update({'Seer':''})
    cards_in_the_game.update({'TroubleMaker':''})
    cards_in_the_game.update({'Insomniac':''})
    cards_in_the_game.update({'Robber':''})
    cards_in_the_game.update({'Minion':''})
    if number_of_players>=5:
        cards_in_the_game.update({'Drunk':''})
    if number_of_players>=6:
        cards_in_the_game.pop('Insomniac')
        cards_in_the_game.update({'Mason':''})
        cards_in_the_game.update({'mason':''})
    if number_of_players>=7:
        cards_in_the_game.update({'Tanner':''})
        
    return cards_in_the_game
