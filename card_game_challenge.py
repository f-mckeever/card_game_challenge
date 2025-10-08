#Card object, number and suit
#52 instances of card /\

#Shuffle function to randomly deal cards to 4 players

#Player object, hand consisting of cards?

#Can print player's hand to the terminal


#Class representing a Card

#number / value is randomly assigned AND suit is randomly assigned
from random import randint, shuffle

#class representing a card
class Card():
    #__init__
    def __init__(self, suit, value, rank):
        self.suit = suit
        self.value = value
        self.rank = rank

    #print what card is
    def what(self):
        print(self.value, self.suit)

#class representing a player
class Player():
    #__init__
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.tricks = []
    #print hand
    def show_hand(self):

        print(f"{self.name}'s Cards:\n")
        card_number = 0
        for card in self.hand:
            print(f"[{card_number}]\t" + card.value + ' ' + card.suit)
            card_number += 1

#returns a list of all unique cards in a deck
def get_deck():
    #all suits and values
    values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K',]
    suits = ['Hearts', 'Spades', 'Clubs', 'Diamonds']
    #empty deck list to start
    deck = []
    #52 card count
    card_count = 52
    #loop down card_count and add unique, randomised cards into deck
    while card_count > 0:
        #new value and new suit
        suit = suits[randint(0, 3)]
        value = values[randint(0, 12)]

        #add card rank based on its assigned value
        if value == 'A':
            rank = 13
        elif value == 'K':
            rank = 12
        elif value == 'Q':
            rank = 11
        elif value == 'J':
            rank = 10
        else:
            rank = int(value) - 1

        #new card
        card = Card(suit, value, rank)
        #if card is unique, add it to deck
        if is_unique(card, deck):
            #add to deck
            deck.append(card)
            #update card count
            card_count -= 1
    #return deck
    return deck

#helper function to check if card is unique
def is_unique(card_to_check, deck):
    #set unique to true
    is_unique = True
    #loop over deck and update is_unique appropriately
    for card in deck:
        if card_to_check.value == card.value and card_to_check.suit == card.suit:
            is_unique = False
    #return is_unique
    return is_unique

#returns list of players, with cards
def get_players():
    #empty player list
    players = []
    #player_count
    player_count = 1
    #loop player count and create players
    while player_count < 5:
        #name and instantiate new player
        player_name = f"Player {player_count}"
        player = Player(player_name)
        #add player to players
        players.append(player)
        #update player_count
        player_count += 1
    #return players
    return players

#assigns all cars to players
def deal_cards(players, deck):
    #overall_card_counter
    overall_card_count = 0

    #loop over each player
    for player in players:
        #assign 13 cards to each
        card_count = 0
        while card_count < 13:
            player.hand.append(deck[overall_card_count])
            #update card_count and overall_card_count
            card_count += 1
            overall_card_count += 1
        #sort player hands by suit for clarity
        player.hand = sorted(player.hand, key=lambda card : card.suit)

#function to check user input for number
def ask_player_for_card_index(player, player_hand, leading_suit, current_trick):

    print("\nPlease input number of card to play...\n")

    #set player_input to empty string
    player_input = ""

    #set input_is_valid_number to false
    input_is_valid_number = False

    #set chosen_card_allowed to False unless it is the first turn in the trick
    chosen_card_allowed = False
    if len(current_trick) == 0:
        chosen_card_allowed = True

    #loop until valid number selected
    while not input_is_valid_number or not chosen_card_allowed:  
        #capture input
        player_input = input()
        #check if input is numeric
        if not player_input.isnumeric():
            print('\nPlease input a valid number...\n')
        #check if outside range of hand values
        elif int(player_input) < 0 or int(player_input) > len(player_hand):
            print('\nPlease input a number corresponding to a card you have...\n')
        #check if player has leading suit and if so the suit of their chosen card must match, else they can pick whatever
        elif player_has_leading_suit(player, leading_suit) and player_hand[int(player_input)].suit != leading_suit:
            print(f"\nYou have at least one card that is {leading_suit}. You must select one of those...\n")
        else: 
            #exit loop
            input_is_valid_number = True
            chosen_card_allowed = True

    #return the int value of the input
    return int(player_input)

#returns index of player that has the 2 of clubs and so can go first
def who_has_2_clubs(player_list):
    #start with index 0 and update until finding the 2 of clubs
    player_2_clubs_index = 0
    #loop over players
    for player in player_list:
        #loop over cards
        for card in player.hand:
            #if 2 of clubs present, return else update player_2_clubs_index and move to next player
            # print(card.suit, card.value)
            if card.suit == "Clubs" and card.value == '2':
                print(f"\nPlayer {player_2_clubs_index + 1} has the 2 of clubs and goes first!")
                return player_2_clubs_index
        player_2_clubs_index += 1
    #return the index lol
    return player_2_clubs_index

#checks if a player has a card of the leading suit in their hand
def player_has_leading_suit(player, leading_suit):
    #loop over hand and return true if player has a card of the leading suit
    for card in player.hand:
        if card.suit == leading_suit:
            return True    
    return False

#play a card
def play_card(current_player, card_index, current_trick, current_player_index):
    print(f"\n{current_player.name} played the {current_player.hand[card_index].value} of {current_player.hand[card_index].suit}!\n")
    current_trick.append({
        'card': current_player.hand[card_index],
        'player_index' : current_player_index})
        
    current_player.hand.pop(card_index)

    print("Current trick: \n")
    for played_card in current_trick:
        print(played_card.get('card').value, played_card.get('card').suit)

#Player's turn:
#Show cards, ask what card to play
#Player input number
#check if valid number, repeat
#call play_card 

#Bots turn
#random int between 0 and length of hand - 1

def run_game():

    #list to apply ranked values to each card value
    card_values_ranked = []
    #get deck
    deck = get_deck()

    #get player list
    player_list = get_players()

    #deal cards to players
    deal_cards(player_list, deck)

    #turn counter, after 13 turns the game ends
    turn_counter = 0

    #get index of player that has the 2 of clubs
    current_player_index = who_has_2_clubs(player_list)

    while turn_counter < 13:

        print(f"\nIt's turn {turn_counter + 1}!")

        #the starting player for the round
        current_player = player_list[current_player_index]
    
        #list of cards from current trick
        current_trick = []

        #leading suit of trick
        leading_suit = ''

        #Start each trick at 0
        trick_counter = 0

        #Loop turn until 4 cards played - each trick
        while trick_counter < 4:
            #call player_take_turn
            player_take_turn(current_player, current_trick, leading_suit, current_player_index)
            #set leading suit if necessary
            if len(current_trick) == 1:
                leading_suit = current_trick[0].get('card').suit
                print(f"\nThe leading suit is now {leading_suit}!")

            #update trick counter
            trick_counter +=1
            #move to next player in list or loop back to the start, reassign current player for appropriate index
            if current_player_index == 3:
                current_player_index = 0
                current_player = player_list[current_player_index]
            else:
                current_player_index += 1
                current_player = player_list[current_player_index]
                
        #print trick
        print("\nTrick Completed!\n")
            
        #trick won by player with highest card of the leading suit

        #set winning card to first one
        winning_card = current_trick[0].get('card')
        counter = 0
        winning_card_index = 0
        #loop through current_trick and see if any cards of the same suit (leading_suit) have a higher value
        for played_card in current_trick:
            #check if card is correct suit
            if played_card.get('card').suit == leading_suit and played_card.get('card').rank > winning_card.rank:
                winning_card = played_card.get('card')
                winning_card_index = counter
            #increase counter   
            counter += 1
        
        #Print nice message and add trick to winners tricks list
        print(f"The {current_trick[winning_card_index].get('card').value} of {current_trick[winning_card_index].get('card').suit} is the winning card, {player_list[current_trick[winning_card_index].get('player_index')].name} wins this round!")
        #List comprehension to get list of just card objects from trick to store in winnin player's tricks list
        current_trick_cards = [card.get('card') for card in current_trick]
        player_list[current_trick[winning_card_index].get('player_index')].tricks.append(current_trick_cards)

        #set current_player to winning player for next trick
        current_player_index = current_trick[winning_card_index].get('player_index')

        #update the turn counter
        turn_counter += 1
    
    #The end of the game
    print('\nTHE GAME IS OVER\n')


#if player has a card in leading suit, one of those MUST be played
#if not, any card can be played

def player_take_turn(current_player, current_trick, leading_suit, current_player_index):
    print(f"\n{current_player.name}, what card would you like to play?\n")
    #print player's cards
    current_player.show_hand()
    #if human, ask to select card
    if current_player_index == 0:
        play_card(current_player, ask_player_for_card_index(current_player, current_player.hand, leading_suit, current_trick), current_trick, current_player_index)
    #if bot, randomly select the card
    else:
        #check if bot has leading suit
        if player_has_leading_suit(current_player, leading_suit):
            #collect indexes for cards of leading suit in bot's hand
            match_leading_suit_indexes = []
            #loop over hand to find them
            index_counter = 0
            for card in current_player.hand:
                if card.suit == leading_suit:
                    match_leading_suit_indexes.append(index_counter)
                index_counter += 1
            #play card from one of those index values
            print(f"\n{current_player.name} has {leading_suit} and so must play one!")
            play_card(current_player, randint(match_leading_suit_indexes[0], match_leading_suit_indexes[-1]), current_trick, current_player_index)
        #otherwise just play random card
        else:
            if len(current_trick) != 0: 
                print(f"\n{current_player.name} doesn't have any{leading_suit} and so can play what they like!")

            play_card(current_player, randint(0, len(current_player.hand) -1), current_trick, current_player_index)



#check if bot has a card of leading suit:
#if so they must play it
#
run_game()

#TASKS


