#! /usr/bin/env python3
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

""" This module calls to run the entire game. """
from blackjackgame.game import Blackjack


if __name__ == '__main__':
    GAME = Blackjack()
    GAME.run()
