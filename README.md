# Breakthru

## Introduction
As a part of the course [Intelligent Search and Games](https://www.maastrichtuniversity.nl/meta/414419/intelligent-search-games), the student implements a board game that uses an AI to play against another AI or a human being.

This repository contains the implementation of Breakthru, an abstract board game for two players. The programming language used is Python 3.6 and the library Pygame. The goal of this work is to learn how to apply advanced search techniques like Minimax, Alpha-beta, Negamax, Principal Variation Search (PVS), and Hash tables as data structures.


## Code structure
- Images directory contains the images used in the games menu
- AI.py contains the AI's strategy and the movement that the machine can do on the board.
- main.py run the game and display the menu to select the options available( Human vs Human, Human vs AI, AI vs Human, and AI vs AI).
- RulesAction.py contains the rules of the game that the players have to follow.


## Game
The game starts with the first menu, in which the user has to select the kind of players.
![alt text](https://raw.githubusercontent.com/diegoWatanabe/breakthru/master/screenshots/first_menu.PNG)

The second menu is to select which player starts the game, Gold or Silver.
![alt text](https://raw.githubusercontent.com/diegoWatanabe/breakthru/master/screenshots/second_menu.PNG)

After that, the game starts. In this case, the two AI are playing each other.
![alt text](https://media0.giphy.com/media/SNiM98RnVC9mohnowK/giphy.gif?cid=790b76115cd31df5087c182221aa3908eb446e983d413bc2&rid=giphy.gif&ct=g)


After

## Limitations
Due to the machine restrictions and the deepest search that we are able to do in the machine is 2. Another point to take into account is that Python is a interpreted language which makes it slower in recursive tasks comparing to another language like Java.
