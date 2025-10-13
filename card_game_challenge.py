from random import randint

#class representing a card
class Card():
    #__init__
    def __init__(self, suit, value, rank, absolute_rank):
        self.suit = suit
        self.value = value
        self.rank = rank
        self.absolute_rank = absolute_rank

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
        self.score = 0
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

        #calculate absolute_rank value: Hearts = + 30, Spades = +20, Diamonds = +10 { + rank
        if suit == 'Hearts':
            absolute_rank = rank + 300
        elif suit == 'Spades':
            absolute_rank = rank + 200
        elif suit == 'Diamonds':
            absolute_rank = rank + 100
        else:
            absolute_rank = rank

        #new card
        card = Card(suit, value, rank, absolute_rank)
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
        player.hand = sorted(player.hand, key=lambda card : card.absolute_rank)

#function to check user input for number
def ask_player_for_card_index(player, player_hand, leading_suit, current_trick, hearts_are_broken, can_play_hearts):

    print("\nPlease input number of card to play...\n")

    #set player_input to empty string
    player_input = ""

    #set input_is_valid_number to false
    input_is_valid_number = False


    #loop until valid number selected
    while not input_is_valid_number or not chosen_card_allowed:  
        #capture input
        player_input = input()


        #Check if input is valid and within the bounds of the player's hand:
        #check if input is numeric
        if not player_input.isnumeric():
            print('\nPlease input a valid number...\n')


        #check if outside range of hand values
        elif int(player_input) < 0 or int(player_input) > len(player_hand) - 1:
            print('\nPlease input a number corresponding to a card you have...\n')


        #if player is going first
        elif len(current_trick) == 0:
            #if player has other suits , and hearts are not broken, they must play one of those
            if not hearts_are_broken and player_has_other_suits(player) and player_hand[int(player_input)].suit == 'Hearts':
                print(f"\nHearts are not yet broken and you have other suits. You must select one of those...\n")
            #if hearts not broken but player has no other suits, print that
            elif not hearts_are_broken and not player_has_other_suits(player) and player_hand[int(player_input)].suit == 'Hearts':
                print(f"\nHearts are not yet broken, but you only have Hearts so you can play that...\n")

            #so long as no banned actions take place, exit the loop
            else:
                #exit loop
                input_is_valid_number = True
                chosen_card_allowed = True

        #if player is not going first
        elif len(current_trick) != 0:
            #check if player has leading suit and if so the suit of their chosen card must match, else they can pick whatever
            if player_has_leading_suit(player, leading_suit) and player_hand[int(player_input)].suit != leading_suit:
                print(f"\nYou have at least one card that is {leading_suit}. You must select one of those...\n")
            #check if player 
            elif not can_play_hearts(hearts_are_broken, player, leading_suit) and player_hand[int(player_input)].suit == "Hearts":
                print(f"\nYou cannot select Hearts yet. Please select a different suit..\n.")

            #so long as no banned actions take place, exit the loop
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

#check if hearts_can_be_played
def can_play_hearts(hearts_are_broken, current_player, leading_suit):
    #if hearts are broken, can play hearts \ or they don't have the lead suit \ or they ONLY have hearts
    if hearts_are_broken or not player_has_leading_suit(current_player, leading_suit) or not player_has_other_suits:
        return True
    #else return false
    return False

#check if player has any suit other than hearts
def player_has_other_suits(current_player):
    #loop over cards and return True if any other suit found
    for card in current_player.hand:
        return card.suit != 'Hearts' 

#3 cards passwed between players at start of round
def card_swap(player_list):
    print("\nPlease select 3 cards to give to the player ahead of you...\n")
    #swap pot list
    cards_to_swap = []
    #for each player
    for player in player_list:
        #for human player
        if player.name == 'Player 1':
            #ask for index of first, second, then third card
            swap_card_indexes = []
            swap_card_absolute_ranks = []

            #set player_input to empty string
            player_input = ""

            #show player's current hand
            card_count = 0

            for card in player.hand:
                print(f"[{card_count}]\t{card.value} {card.suit}")
                card_count += 1

            #loop until valid number selected
            while len(swap_card_indexes) != 3: 

                print(f"\nPlease select card number {len(swap_card_indexes) +1} to swap...\n")

                #capture input
                player_input = input()

                #Check if input is valid and within the bounds of the player's hand:
                #check if input is numeric
                if not player_input.isnumeric():
                    print('\nPlease input a valid number...\n')

                #check if outside range of hand values
                elif int(player_input) < 0 or int(player_input) > len(player.hand) - 1:
                    print('\nPlease input a number corresponding to a card you have...\n')

                #check if card_index already in swap_card_indexes
                elif int(player_input) in swap_card_indexes:
                    print('\nCard already selected, please select another...')

                #so long as no banned actions take place, forward the loop
                else:
                    #add index to list
                    swap_card_indexes.append(int(player_input))
                    swap_card_absolute_ranks.append(player.hand[int(player_input)].absolute_rank)

                    #inform user
                    print(f"\nYou have chosen to give:\n")
                    for index in swap_card_indexes:
                        print(f"The {player.hand[index].value} of {player.hand[index].suit}")

            #add cards at chosen indexes to the list
            for index in swap_card_indexes:
                cards_to_swap.append(player.hand[index])
                
            for rank in swap_card_absolute_ranks:
                player.hand = [card for card in player.hand if card.absolute_rank != rank]

        #for bot player
        else:
            #list to store randomly selected bot card indexes
            swap_card_indexes = []
            swap_card_absolute_ranks = []
            #loop 3 times to select indexes
            loop_counter = 1
            while loop_counter <= 3:

                #if player has queen of spades, swap it
                if has_queen_of_spades(player.hand) and len(swap_card_indexes) == 0:
                    index_counter = 0
                    for card in player.hand:
                        if card.absolute_rank == 211:
                            swap_card_indexes.append(index_counter)
                            swap_card_absolute_ranks.append(player.hand[index_counter].absolute_rank)
                            loop_counter += 1
                        index_counter += 1
                else:
                    #add a random int between 0 and 12, ensuring only unique numbers are added
                    random_index = randint(0, 12)
                    if random_index not in swap_card_indexes:
                        swap_card_indexes.append(random_index)
                        swap_card_absolute_ranks.append(player.hand[random_index].absolute_rank)
                        loop_counter += 1

            #inform user
            print(f"\n{player.name} has chosen to give:\n")
            for index in swap_card_indexes:
                print(f"The {player.hand[index].value} of {player.hand[index].suit}")

            #add cards to the list and remove from player's hand
            for index in swap_card_indexes:
                cards_to_swap.append(player.hand[index])
            
            for rank in swap_card_absolute_ranks:
                player.hand = [card for card in player.hand if card.absolute_rank != rank]

            #print informative message to terminal
            print(f"\n{player.name} has selected 3 cards to swap.\n")

    #assign new cards to each player in "clockwise" order
    cards_to_swap_counter = 0
    for card in cards_to_swap :
        if cards_to_swap_counter < 3 :
            player_list[1].hand.append(card)
        elif cards_to_swap_counter < 6 :
            player_list[2].hand.append(card)
        elif cards_to_swap_counter < 9 :
            player_list[3].hand.append(card)
        else:
            print(f"Player 1 received the {card.value} of {card.suit}")
            player_list[0].hand.append(card)
        #update counter
        cards_to_swap_counter += 1

#controls the running of the game
def run_game():

    #get deck
    deck = get_deck()

    #get player list
    player_list = get_players()

    #deal cards to players
    deal_cards(player_list, deck)

    #turn counter, after 13 turns the game ends
    turn_counter = 0

    #set Hearts Are Broken to False to start
    hearts_are_broken = False
    hearts_are_broken_message_printed = False

    #do the card swap
    card_swap(player_list)

    #get index of player that has the 2 of clubs
    current_player_index = who_has_2_clubs(player_list)

    #organise player hands again to ensure they are neat
    for player in player_list:
        #sort player hands by suit for clarity
        player.hand = sorted(player.hand, key=lambda card : card.absolute_rank)

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
            player_take_turn(current_player, current_trick, leading_suit, current_player_index, hearts_are_broken, can_play_hearts)

            #check if hearts are broken
            if current_trick[-1].get('card').suit == "Hearts":
                if not hearts_are_broken_message_printed:
                    print(f"\n{current_player.name} has played the {current_trick[-1].get('card').value} of {current_trick[-1].get('card').suit}.\n\nHEARTS HAVE BEEN BROKEN!")
                hearts_are_broken = True
                hearts_are_broken_message_printed = True
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
    print('\nTHE GAME IS OVER!')
    show_score(player_list)

#prints the results of the game to the terminal - tots up points and orders players accordingly
def show_score(player_list):
    #loop over all players and count up scores
    for player in player_list:
        count_score_for_player(player)
    #check if player got all hearts and the queen of spades and adjust scores if so
    bonus_points(player_list)

    #who bonus pointed if anyone
    bonus_pointer = who_bonus_pointed(player_list)

    #print leaderboard to the screen
    print("The Final Scores:\n")
    position = 1
    for player in sorted((player_list), key=lambda player: player.score):
        print(f"[{position}]: {player.name} with {player.score} points!\n")
        #print player's cards to validate scores
        print(f"\t{player.name}'s cards:\n")
        for trick in player.tricks:
            for card in trick:
                print("\t", card.value, card.suit)
                if card.suit == 'Hearts':
                    print("\t\t\t+1 point")
                if card.suit == 'Spades' and card.value == 'Q':
                    print("\t\t\t+13 points")
        print("\n")
        
        #if someone bonus pointed, 
        if bonus_pointer >= 0:
            #if player is the one to bonus point, print -26 points
            if player_list[bonus_pointer] == player:
                print('\tAll Hearts and Q Spades')
                print("\t\t\t-26 points")
            #print +26 points for all other players
            else:
                print(f"{player_list[bonus_pointer].name} got all Hearts and Queen of Spades")
                print("\t\t\t+26 points\n")
        position += 1

#little function to tot up each player's scores
def count_score_for_player(player):
    #loop over tricks and tot up the score
    for trick in player.tricks:
        #loop over each card and add points for hearts or queen of spades
        for card in trick:
            if card.suit == 'Hearts':
                player.score += 1
            elif card.suit == 'Spades' and card.value == "Q":
                player.score += 13

#return index of player who earned bonus points or -1 if none did
def who_bonus_pointed(player_list):
    #set index_counter to
    player_index_counter = 0
    bonus_winning_player_index = -1

    #loop each player
    for player in player_list:
        #if player has all hearts and the queen of spades, return true and set winning
        if all_hearts_queen_spades(player):
            print(f"\n{player.name} got all of the Hearts and the Queen of Spades! Everyone else gains 26 points!")
            bonus_winning_player_index = player_index_counter
            break
        #update counter
        player_index_counter += 1
    
    return bonus_winning_player_index

#little function to check if any player got ALL hearts and the queen of spades, and if so every other player gets 26 points and they get 0
def bonus_points(player_list):

    #check if anyone won and if so who
    bonus_winning_player_index = who_bonus_pointed(player_list)

    #if winner found, add and subtract points appropriately
    if bonus_winning_player_index >= 0:
        #add 26 points to every player
        for player in player_list:
            player.score += 26

        #subtract 52 points from winning player
        player_list[bonus_winning_player_index].score -= 52

#checks if player has all hearts and the queen of spades
def all_hearts_queen_spades(player):
    #List of player's cards
    card_list = []
    for trick in player.tricks:
        for card in trick:
            card_list.append(card)

    #check if cards include queen of spades
    if has_queen_of_spades(card_list):
        #.pop queen of spades
        queenless_card_list = [card for card in card_list if card.suit != 'Spades' and card.value != 'Q']
        print("has_queen_of_spades")
        for card in card_list:
            print(card.value, card.suit)
        #check if queenless_card_list is all hearts
        if only_hearts(queenless_card_list):
            return True

#checks if card_list contains the queen of spades
def has_queen_of_spades(card_list):
    #if queen of spades found, return true
        # return len([card for card in card_list if card.suit == 'Spades' and card.value == 'Q']) == 1

        for card in card_list:
            if card.suit == 'Spades' and card.value == 'Q':
                return True
        
        return False

#check if list is all hearts
def only_hearts(card_list):
    #if any other suit found, return false
    for card in card_list:
            if card.suit != 'Hearts':
                return False
        
    return True

#controls the turn flow for a player
def player_take_turn(current_player, current_trick, leading_suit, current_player_index, hearts_are_broken, can_play_hearts):
    print(f"\n{current_player.name}, what card would you like to play?\n")
    #print player's cards
    current_player.show_hand()
    #if human, ask to select card
    if current_player_index == 0:
        play_card(current_player, ask_player_for_card_index(current_player, current_player.hand, leading_suit, current_trick, hearts_are_broken, can_play_hearts), current_trick, current_player_index)
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
                print(f"\n{current_player.name} doesn't have any {leading_suit} and so can play what they like!")
                #Bot can play any card if it is not the first turn AND they do not have the leading suit
                play_card(current_player, randint(0, len(current_player.hand) -1), current_trick, current_player_index)
            #ELSE the bot is leading, they can ONLY play hearts if they have no other suits
            else:
                #check if bot has any suit other than hearts
                if not hearts_are_broken and player_has_other_suits(current_player):
                    #loop over hand to get indexes of all cards that are NOT hearts
                    print(f"\nHearts are not broken and {current_player.name} has cards of a different suit. They must choose one of those...")
                    not_hearts_indexes = []
                    counter = 0
                    for card in current_player.hand:
                        if card.suit != 'Hearts':
                            not_hearts_indexes.append(counter)

                        counter += 1
                    
                    
                    #bot plays a card that is NOT Hearts from list of indexes of not_hearts_indexes
                    play_card(current_player, not_hearts_indexes[randint(0, len(not_hearts_indexes) -1)], current_trick, current_player_index)
                #otherwise, bot has no choice but to play hearts, ie can pick whatever card they want
                else:
                    if not player_has_other_suits(current_player):
                        print(f"\n{current_player.name} only has hearts! They can play one of those...")
                    play_card(current_player, randint(0, len(current_player.hand) -1), current_trick, current_player_index)

run_game()

#TASKS

#absolute rank of queen of spades is 211


#bot - lose q spades whenever possible
# when can lose it:
# can swap at the beginning of the game

# dont have leading suit && has Q Spades

# is spades and ace of spades and or king of spades have been played

#bot - if possible, dont play q spades or high heart

#bot - try not to win tricks

#can play queen of spades

#check if player can burn queen - only can do so if not leading
def can_burn_queen_spades(player, current_trick, leading_suit):

    #if they don't have queen of spades: false
    if not has_queen_of_spades(player.hand):
        return False
  
    #if current trick has the king or ace of spades
    for card in current_trick:
        #check if spades
        if card.suit == 'Spades':
            #check if king or ace
            if card.value == 'A' or card.value == 'K':
                return True
        
    #if player does not have leading suit
    if not player_has_leading_suit(player, leading_suit) and len(current_trick) != 0:
        return True
  
    #fall back 
    return False

