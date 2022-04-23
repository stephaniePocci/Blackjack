# Stephanie Pocci
# CPSC 386-03
# 2022-04-04
# spokey@csu.fullerton.edu
# @stephaniePocci
#
# Lab 06-00
#
# Cards.py creates the cards for use within the game.
#

"""Cards.py creates a Deck class to handle the game's deck."""
from collections import namedtuple
from random import shuffle
from random import randrange

Card = namedtuple('Card', ['rank', 'suit'])


def stringify_card(card):
    """Turns the cards into readable strings."""
    return '{} of {}'.format(card.rank, card.suit)


Card.__str__ = stringify_card


class Deck:
    """The Deck class controls the logic of the game's deck."""

    ranks = ['Ace'] + [str(x) for x in range(2, 11)] \
        + 'Jack Queen King'.split()
    # creates the sets of cards for the game
    suits = '♣ ♥ ♠ ♦'.split()
    values = list(range(1, 11)) + [10, 10, 10]
    values_dict = dict(zip(ranks, values))
    # creates a dictionary of the values of each card

    def __init__(self, cut_card_position_min=0, cut_card_position_max=0):
        """This function initializes the deck of cards for the game."""
        if cut_card_position_max == 0 and cut_card_position_min == 0:
            self._cut_card_position = 0
        # insert the cut card in the designated cut card position
        self._cards = [Card(rank, suit)
                       for suit in self.suits
                       for rank in self.ranks]

    # _ before variable means it is a protected variable

    def cards(self):
        """A getter function for _cards."""
        return self._cards

    def __getitem__(self, position):
        """A getter function for the position of the card in the deck."""
        return self._cards[position]

    def needs_shuffling(self):
        """Returns true if the deck needs to be shuffled."""
        return len(self._cards) <= self._cut_card_position

    def __len__(self):
        """Getter function for the length of the deck."""
        return len(self._cards)

    def shuffle(self, shuffle_amount):
        """This function shuffles the cards/decks."""
        for _ in range(shuffle_amount):
            # default n is 1, but you can pass in parameter
            shuffle(self._cards)

    def cut(self):
        """This function generates the location of the cut card."""
        self._cut_card_position = randrange(60, 80)
        return self._cut_card_position

    def merge(self, other_deck):
        """This function merges the given decks together."""
        self._cards = self._cards + other_deck.cards()

    def deal(self, shuffle_amount=1):
        """This function deals the cards to the players and dealer."""
        return [self._cards.pop(0) for _ in range(shuffle_amount)]

    def __str__(self):
        return '\n'.join(map(str, self._cards))
    # This __str__ joins the deck together in a string.


def get_rank(card):
    """Getter function for the rank of a card."""
    return card.rank


def card_value(card):
    """Getter function for the value of a card."""
    return Deck.values_dict[card.rank]


def hand_sum(hand):
    """This function sums up the values of all the cards in hand."""
    total = 0
    for card in hand:
        total += card_value(card)
    if sum(map(lambda card: card.rank == 'Ace', hand)) and total + 10 <= 21:
        total += 10
    # lambda creates an anonymous function that declares a behavior
    # within an existing function
    return total
