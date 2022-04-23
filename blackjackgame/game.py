# Stephanie Pocci
# CPSC 386-03
# 2022-04-04
# spokey@csu.fullerton.edu
# @stephaniePocci
#
# Lab 06-00
#
# The module file game.py holds all the functions for the game logic.
#

"""Game.py declares the behaviors for the game's logic."""
import pickle
from blackjackgame.player import AI
from blackjackgame.cards import card_value
from blackjackgame.player import Player
from blackjackgame.cards import stringify_card
from blackjackgame.cards import Deck
from blackjackgame.cards import get_rank
from blackjackgame.cards import hand_sum


def to_file(pickle_file, players):
    """This function opens a pickle file and writes to it."""
    with open(pickle_file, 'wb') as file_handle:
        pickle.dump(players, file_handle, pickle.HIGHEST_PROTOCOL)


def from_file(pickle_file):
    """This function retrieves data from the pickle file."""
    with open(pickle_file, 'rb') as file_handle:
        players = pickle.load(file_handle)
    return players


class Blackjack():
    """The Blackjack class runs the game's logic."""
    def __init__(self):
        self._players = []

    def run(self):
        """The run function loops the entire game behavior."""
        database = []
        # the temporary list where player info is stored
        players = self._players
        print('~~ Welcome to Blackjack! ~~')
        num_of_players = int(input('How many players are there? '))
        try:
            # try to open pickle_database.pckl file
            database.extend(from_file('pickle_database.pckl'))
            for i in range(num_of_players):
                name = input('Please enter Player {}\'s name: '.format(i+1))
                try:
                    # Try to find name in database
                    player_found = False
                    for j in range(len(database)):
                        # parse the entire pickle file
                        if name == database[j].name():
                            # if there is a name match in pickle database:
                            print('Welcome back Player {}!'.format(name))
                            if database[j].balance() <= 0:
                                # check if player still has balance
                                print(
                                      '{} has 0 balance, here is a small '
                                      'donation of 10000!'
                                      .format(database[j].name())
                                     )
                                database[j].modify_balance(10000)
                                # add $10,000 if out of balance
                            player_found = True
                            players.append(database[j])
                            # add new player information to the database

                    if not player_found:
                        # creates a new player character
                        players.append(Player(name, 10000))

                except IndexError:
                    players.append(Player(name, 10000))

        except EOFError:
            # if there is nothing in the pickle file yet
            database = []
            # instantiate list of characters for game
            for _ in range(num_of_players):
                # create a new player for # of players entered
                name = input('Please enter Player {}\'s name: '.format(_ + 1))
                players.append(Player(name, 10000))

        print(' ')

        deck = Deck()
        # initializes the deck

        while True:
            # while the game is still playing
            players.append(AI())
            # add AI to end of game's player list

            for i in range(len(players) - 1):
                # instantiate bets and splits to 0/none
                players[i].modify_side_bet(0)
                players[i].mod_has_split(False)
                if players[i].balance() <= 0:
                    print(
                          '{} has 0 balance, here is a small '
                          'donation of 10000!'.format(players[i].name())
                          )
                    players[i].modify_balance(10000)

            if deck.needs_shuffling():
                # checks if the cards need to be shuffled
                deck = Deck()
                deck1 = Deck()
                for _ in range(8):
                    deck.merge(deck1)
                deck.shuffle(15)
                # shuffles the cards 11 times
                deck.cut()

            for i in range(len(players) - 1):
                # asks each player what bets they would like to place
                if players[i].name() != players[-1].name():
                    print(repr(players[i]))
                    balance = players[i].balance()
                    bet = players[i].bet(balance)
                    players[i].modify_balance(-bet)
            print('{} will now begin dealing\n'.format(players[-1].name()))
            # notify players that the dealer will begin dealing

            for i in range(2):
                # deal the cards to each of the players
                for j in range(len(players)):
                    players[j].deal_to_hand(deck.deal())
                    players[j].modify_hand_string(
                        stringify_card(players[j].hand_index(i))
                    )
                    # asks the player if they would like to split
                    if i == 1:
                        if players[j].name() != players[-1].name():
                            if get_rank(players[j].hand_index(0)) == get_rank(
                                players[j].hand_index(1)
                            ):
                                print(
                                      '{} has two cards of same rank.'
                                      .format(players[j].name())
                                     )
                                players[j].mod_has_split(
                                    players[j].split(
                                        players[j].bet_amount(),
                                        players[j].balance(),
                                        deck.deal(),
                                    )
                                )

            print(
              # dealer shows their first card
              '{}\'s Hand: [\'{}\']\n'
              .format(players[-1].name(), players[-1].string_hand_index(0))
                 )

            # asks player if they would like insurance
            if (
                card_value(players[-1].hand_index(0)) == 10
                or card_value(players[-1].hand_index(0)) == 11
                or card_value(players[-1].hand_index(0)) == 1
               ):
                for i in range(len(players) - 1):
                    want_insurance = input('Dealer: Do you want insurance? \
                                            (Y/N): ')
                    if want_insurance in ('Y', 'y'):
                        balance = players[i].balance()
                        side_bet = players[i].side_bet(balance)
                        players[i].modify_balance(-side_bet)

            # will occur if player wins insurance
            if hand_sum(players[-1].hand()) == 21:
                print(repr(players[-1]))
                print('{} has blackjack!\n'.format(players[-1].name()))
                for i in range(len(players) - 1):
                    if players[i].name() != players[-1].name():
                        balance = players[i].balance()
                        side_bet = players[i].side_bet_amount()
                        if players[i].side_bet_amount() > 0:
                            print(
                                '{} won ${}!'
                                .format(
                                    players[i].name(),
                                    side_bet * 2
                                 )
                                )
                            players[i].modify_balance(side_bet * 2)
            else:
                for i in range(len(players) - 1):
                    if players[i].name() != players[-1].name():
                        side_bet = players[i].side_bet_amount()
                        balance = players[i].balance()
                        if side_bet > 0:
                            print(
                                  '{} lost ${}.\n'
                                  .format(players[i].name(), side_bet)
                                 )

                # the main game logic
                for i in range(len(players) - 1):
                    print(repr(players[i]))
                    print('{} has {}\n'
                          .format(
                              players[i].name(),
                              hand_sum(players[i].hand())
                          )
                          )

                    # handles the double-down
                    blackjack = False
                    # check if player has a blackjack
                    blackjack = players[i].blackjack(players[i].hand())
                    if blackjack:
                        continue
                    player_option = players[i].want_hit()
                    double_down = False
                    if player_option in ('Y', 'y'):
                        double_down = players[i].double_down(deck.deal())

                    # allows players to get another card
                    game_active = True
                    while game_active and not double_down and\
                            player_option in ('Y', 'y'):
                        game_active = players[i].hit(
                            deck.deal(), player_option
                        )
                        players[i].mod_hand_sum_1(
                            hand_sum(players[i].hand())
                        )
                        if hand_sum(players[i].hand()) < 21:
                            player_option = players[i].want_hit()

                    # allows player to hit on their other hand
                    # after a split
                    if players[i].has_split():
                        blackjack = players[i].blackjack(
                            players[i].other_hand()
                        )
                        if blackjack:
                            continue
                        player_option = players[i].want_hit()

                        double_down_split = False
                        # allows player to double down on their other hand
                        if player_option in ('Y', 'y'):
                            double_down_split = players[i].double_down_split(
                                deck.deal()
                            )

                        game_active = True
                        while (
                            game_active
                            and not double_down_split
                            and player_option in ('Y', 'y')
                        ):
                            game_active = players[i].hit_other_hand(
                                deck.deal(), player_option)
                            players[i].mod_hand_sum2(hand_sum(
                                players[i].other_hand()))
                            if hand_sum(players[i].other_hand()) < 21:
                                player_option = players[i].want_hit()

                # reveals the dealer's second card
                print(repr(players[-1]))
                # CPU plays
                game_active = True
                while game_active:
                    game_active = players[-1].hit(deck.deal())

                # pays out players at end of the game
                dealer_score = hand_sum(players[-1].hand())
                if not game_active and dealer_score <= 21:
                    for i in range(len(players) - 1):
                        player_score = hand_sum(players[i].hand())
                        if players[i].has_split():
                            player_score2 = hand_sum(
                                players[i].other_hand())

                            if (
                                player_score > dealer_score
                                and player_score2 > dealer_score
                            ):
                                players[i].modify_balance(
                                    players[i].bet_amount() * 2)
                                print(
                                      '{} won ${}!'
                                      .format(
                                           players[i].name(),
                                           players[i].bet_amount() * 2
                                      )
                                     )

                            elif player_score > dealer_score or \
                                    player_score2 > dealer_score:
                                if double_down or double_down_split:
                                    players[i].modify_balance(
                                        players[i].bet_amount() * 1.5
                                        # payout if one hand wins
                                        # and the other hand doesnt
                                    )
                                else:
                                    players[i].modify_balance(
                                        players[i].bet_amount()
                                    )
                                    print(
                                          '{} broke even.'
                                          .format(players[i].name())
                                        )

                            elif player_score == dealer_score and\
                                    player_score2 == dealer_score:
                                players[i].modify_balance(players[i].
                                                          bet_amount())
                                print('{} Pushed.'.format(players[i].name()))

                        if player_score > dealer_score:
                            if player_score <= 21:
                                players[i].modify_balance(
                                    players[i].bet_amount() * 2
                                    # payout bet x 2 b/c of split
                                )
                                print(
                                      '{} won ${}!'
                                      .format(
                                          players[i].name(),
                                          players[i].bet_amount() * 2
                                      )
                                     )

                        elif player_score == dealer_score:
                            players[i].modify_balance(players[i].bet_amount())
                            print('{} Pushed.'.format(players[i].name()))

                        else:
                            print(
                                  '{} loses ${}.'
                                  .format(
                                      players[i].name(),
                                      players[i].bet_amount()
                                  )
                            )
                else:
                    for i in range(len(players) - 1):
                        players[i].modify_balance(players[i].bet_amount() * 2)
                        print(
                              '{} won ${}!'
                              .format(
                                  players[i].name(),
                                  players[i].bet_amount() * 2
                              )
                             )

            player_choice = input('Continue playing? (Y/N)')
            # ask players if they want to continue playing
            print(' ')
            # clear the dealer's hand
            players[-1].hand_clear()
            players[-1].string_hand_clear()
            players.pop()
            # remove AI from list
            for i in range(len(players)):
                # clears player information for next round
                # ensures it wont be stored in pickle file
                players[i].hand_clear()
                players[i].other_hand_clear()
                players[i].string_hand_clear()
                players[i].string_other_hand_clear()

            # store information in pickle file
            if player_choice not in ('Y', 'y'):
                to_file('pickle_database.pckl', players)
                # clear player information for next round
                players.clear()
                break
