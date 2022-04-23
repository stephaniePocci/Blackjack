# Stephanie Pocci
# CPSC 386-03
# 2022-04-04
# spokey@csu.fullerton.edu
# @stephaniePocci
#
# Lab 06-00
#
# Player.py creates the Player and AI classes.
#

"""Player.py handles the logic for the Players and AI."""
from blackjackgame.cards import hand_sum
from blackjackgame.cards import stringify_card


class Player:
    """Player class controls the behavior of the Player characters."""
    def __init__(self, name, bankroll):
        self._name = name
        self._balance = bankroll
        self._bet = 0
        self._side_bet = 0  # in this case only insurance and double down
        self._hand = []
        self._string_hand = []
        self._hand_sum1 = 0
        self._other_hand = []
        self._string_other_hand = []
        self._hand_sum2 = 0
        self._has_split = False

    def name(self):
        """Getter function for name of player."""
        return self._name

    def __repr__(self):
        """The display of player information."""
        return ('Player: {}\n'
                'Balance: {} Bet: {} '
                'Side bet: {}\n'
                'Hand: {}\n'
                'Side hand: {}\n'.format(self._name, self._balance, self._bet,
                                         self._side_bet, self._string_hand,
                                         self._string_other_hand))

    def __str__(self):
        """Returns the name of the player as a string."""
        return self._name

    def balance(self):
        """Getter function for the player's total balance."""
        return self._balance

    def modify_balance(self, amount):
        """Returns the modified balance of the player."""
        return self.set_balance(self._balance + amount)

    def set_balance(self, value):
        """Setter function for the new balance of a player."""
        self._balance = value
        # value = new balance of the player
        print('Balance was set to {}'.format(self._balance))
        return self._balance

    def bet(self, balance):
        """Allows player to input how much they would like to bet."""
        self._bet = int(
            input("{}: How would you like to bet? ".format(self._name))
        )
        while self._bet > balance or self._bet <= 0:
            # if the bet amount is larger than their balance
            print("Insufficient funds.")
            self._bet = int(
                input("{}: How much do you want to bet? ".format(self._name))
            )
        # returns bet amount
        return self._bet

    def bet_amount(self):
        """Getter function for the player's bet amount."""
        return self._bet

    def modify_side_bet(self, amount):
        """Setter function for new amount of the side bet."""
        self._side_bet = amount
        # amount = new bet amount
        return self._side_bet

    def side_bet(self, balance):
        """Function asks user for their bet on their other hand."""
        self._side_bet = int(
            input("{}: How much would you like to bet? ".format(self._name))
        )
        print(' ')
        while self._side_bet > balance or self._side_bet <= 0:
            print("Insufficient funds.")
            self._side_bet = int(
                input("{} How much would you like to bet? ".format(self._name))
            )
            print(' ')
        # return the side bet of the player
        return self._side_bet

    def side_bet_amount(self):
        """Getter function for player's side bet."""
        return self._side_bet

    def hand(self):
        """Getter function for the cards in main hand."""
        return self._hand

    def deal_to_hand(self, deal):
        """Function allows cards to be dealt."""
        self._hand.extend(deal)
        return self._hand

    def hand_index(self, value):
        """Getter function for the hand's index."""
        return self._hand[value]

    def modify_hand_string(self, stringify):
        """Getter function for the string of the main hand."""
        self._string_hand.append(stringify)
        return self._string_hand

    def string_hand_index(self, value):
        """Getter function for the hand's index in string form."""
        return self._string_hand[value]

    def mod_hand_sum_1(self, value):
        """Getter function for the modified hand value."""
        self._hand_sum1 += value
        return self._hand_sum1

    def mod_hand_sum_2(self, value):
        """Getter function for the modified other hand value."""
        self._hand_sum2 += value
        return self._hand_sum2

    def other_hand(self):
        """Getter function for the cards in the player's other hand."""
        return self._other_hand

    def double_down(self, deal):
        """Asks the player if they would like to double-down."""
        double_down = input('Double down? (Y/N): ')
        if double_down in ('Y', 'y'):
            self.modify_balance(-self.bet_amount())
            self._bet = self._bet * 2
            self._hand.extend(deal)
            self._string_hand.append(stringify_card(self._hand[-1]))
            print('Hand: {}'.format(self._string_hand))
            print('{} has {}'.format(self._name, hand_sum(self._hand)))

            if hand_sum(self._hand) > 21:
                print('Busted!\n')
                return True

            elif hand_sum(self._hand) == 21:
                print('Blackjack!\n')
                return True

            print(' ')
            return True

        return False

    def double_down_split(self, deal):
        """Asks the player if they would like to double-down on a split."""
        double_down = input('Double down? (Y/N): ')
        if double_down in ('Y', 'y'):
            self.modify_balance(-self.bet_amount())
            self._other_hand.extend(deal)
            self._string_other_hand.append(
                stringify_card(self._other_hand[-1])
            )
            print('Side hand: {}'.format(self._string_other_hand))
            print('{} has {}.'.format(self._name, hand_sum(self._other_hand)))

            if hand_sum(self._other_hand) > 21:
                print('Busted!\n')
                return True

            elif hand_sum(self._other_hand) == 21:
                print('Blackjack!\n')
                return True
            print(' ')
            return True

        return False

    def want_hit(self):
        """Asks the player if they would like another card."""
        player_action = input(
            '{}: Do you want to hit? (Y/N) '.format(self._name)
        )
        print(' ')
        if player_action in ('Y', 'y'):
            player_action = 'y'
        else:
            player_action = 'n'
        return player_action

    def hit(self, deal, player_action):
        """Checks if player busted or has blackjack."""
        if player_action in ('Y', 'y'):
            self._hand.extend(deal)
            self._string_hand.append(stringify_card(self._hand[-1]))
            print('{}\'s Hand: {}'.format(self._name, self._string_hand))
            # displays information on their main hand
            print('{} has {}'.format(self._name, hand_sum(self._hand)))

            if hand_sum(self._hand) > 21:
                print('Busted!\n')
                return False
            elif hand_sum(self._hand) == 21:
                print('Blackjack!\n')
                return False
            print(' ')

        else:
            print('{} stays at {}\n'.format(self._name, hand_sum(self._hand)))
        return True

    def hit_other_hand(self, deal, player_action):
        """Checks if player busted or has blackjack in their other hand."""
        if player_action in ('Y', 'y'):
            self._other_hand.extend(deal)
            self._string_other_hand.append(
                stringify_card(self._other_hand[-1])
            )
            print('Side hand: {}'.format(self._string_other_hand))
            # displays information on their other hand
            print('{} has {}'.format(self._name, hand_sum(self._other_hand)))

            if hand_sum(self._other_hand) > 21:
                print('Busted!\n')
                return False

            elif hand_sum(self._other_hand) == 21:
                print('Blackjack!\n')
                return False

        else:
            print('{} stays at {}\n'.format(
                self._name, hand_sum(self._other_hand))
            )
        return True

    def split(self, bet, balance, deal):
        """Asks a player if they would like to split."""
        player_action = input("{}: Do you want to split? (Y/N) "
                              .format(self._name))
        if player_action in ('Y', 'y'):
            if bet <= balance:
                balance = balance - bet
                bet += bet
                # doubles the bet to match the main hand's bet for other hand
                self._other_hand.extend(self._hand[1])
                self._string_other_hand.append(
                    stringify_card(self._other_hand[0])
                )
                self._hand.pop(1)
                self._string_hand.pop(1)
                self._hand.extend(deal)
                self._other_hand.extend(deal)
                self._string_hand.append(
                    stringify_card(self._hand[1])
                )
                self._string_other_hand.append(
                    stringify_card(self._other_hand[1])
                )
                # transfers card from main hand to other hand
                self._has_split = True
                print('{}\'s Hand: {}'.format(self._name, self._string_hand))
                print('Side hand: {}'.format(self._string_other_hand))
            else:
                print('Not enough funds to do a split.')
        return self._has_split

    def has_split(self):
        """Getter function for if a player has a split."""
        return self._has_split

    def mod_has_split(self, value):
        """Setter function for when a player has a split."""
        self._has_split = value
        return self._has_split

    def hand_clear(self):
        """Clears the hand of the current player."""
        self._hand.clear()
        return self._hand

    def string_hand_clear(self):
        """Clears the string for the hand of the current player."""
        self._string_hand.clear()
        return self._string_hand

    def other_hand_clear(self):
        """Clears the other hand of the current player."""
        self._other_hand.clear()
        return self._other_hand

    def string_other_hand_clear(self):
        """Clears the other hand of the current player."""
        self._string_other_hand.clear()
        return self._string_other_hand

    def blackjack(self, hand):
        """Checks if the condition of Blackjack has been met."""
        if hand_sum(hand) == 21:
            print('Blackjack!')
            return True
        return False


class AI:
    """AI class controls the behavior of the AI."""
    def __init__(self):
        self._string_hand = []
        self._name = "HAL9000"
        self._hand = []

    def __repr__(self):
        """The display of the dealer's information."""
        return 'Player: {}\n Hand: {}\n'.format(self._name, self._string_hand)

    def name(self):
        """Getter function for the name of the dealer."""
        return self._name

    def hand(self):
        """Getter function for the hand of the dealer."""
        return self._hand

    def hand_index(self, value):
        """Getter function for the value of the dealer's hand."""
        return self._hand[value]

    def deal_to_hand(self, deal):
        """Deals a card to the dealer."""
        self._hand.extend(deal)
        return self._hand

    def modify_hand_string(self, stringify):
        """Setter function for the new string of the dealer's hand."""
        self._string_hand.append(stringify)
        return self._string_hand

    def string_hand_index(self, value):
        """Returns the new string of the hand."""
        return self._string_hand[value]

    def hit(self, deal):
        """The hit function determines the AI's logic."""
        game_over = False
        while hand_sum(self._hand) < 17:
            # only hit dealer if their hand is below 17
            self._hand.extend(deal)
            self._string_hand.append(stringify_card(self._hand[-1]))
            print('{} hand: {}'.format(self._name, self._string_hand))

        if hand_sum(self._hand) > 21:
            print('Busted!\n')
        elif hand_sum(self._hand) == 21:
            print('Blackjack!\n')
        else:
            print('{} stays at {}'.format(self._name, hand_sum(self._hand)))

        return game_over

    def hand_clear(self):
        """Clears the hand of the dealer."""
        self._hand.clear()
        return self._hand

    def string_hand_clear(self):
        """Clears the string of the dealer's hand."""
        self._string_hand.clear()
        return self._string_hand

    def blackjack(self, hand):
        """Checks if the dealer's hand meets the Blackjack requirements."""
        if hand_sum(hand) == 21:
            print('Blackjack!')
            return True
        return False
