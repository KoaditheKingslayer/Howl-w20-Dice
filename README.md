# Howl w20 Dice

Thanks for your interest in Howl. I created Howl to be a Discord bot that can be used for rolling parsed dice in the ruleset of Werewolf: The Apocalypse 20th 
anniversary edition. It's the product of a single night and a few hours of coding work in its current iteration, but it accomplishes the goals that I had set 
out to accomplish. 

## Features 

Howl automatically parses the dice rolls that are given to it in a way that gives useful outputs for players and Storytellers alike. Howl can accept a number 
of optional arguments as part of the /roll command that will display extra information for the roll, or alter how the roll is parsed. 

## Rule-Set

In this edition, the following are the stand-out rules. 

![#f03c15](https://www.iconsdb.com/icons/download/color/f03c15/circle-16.png) Any die rolled that equals or exceeds the stated difficulty are considered Success Dice.

![#f03c15](https://www.iconsdb.com/icons/download/color/f03c15/circle-16.png) Any die that rolls a 1 scores a Failure Dice. Failure Dice subtract from the overall number of generated Successes.

![#f03c15](https://www.iconsdb.com/icons/download/color/f03c15/circle-16.png) A Botch occurs only if zero Success Dice are rolled, and one or more Failure Dice are rolled. 

![#f03c15](https://www.iconsdb.com/icons/download/color/f03c15/circle-16.png) 10's count as two successes when a Specialty is used. Failure Dice do not cancel out a rolled 10, but rather cancel out 
one of the successes from a Specialty 10. (Note: "Bonus" Successes from 10's will appear in brackets as [10] when output in Discord. 

## Commands and Parameters

### /roll
The basic command requires the Parameters Pool: and Difficulty: 

Pool can be any number. 

Difficulty can be any number between 3 and 10. 

### Additional Parameters

Character: Sets a name to display in the output for the character you are rolling for. 

Notes: Can be used to describe the roll (traits involved, action being taken) and have that read out in the parsed roll. 

Specialty: If specified (any text will read as true, but common use is to write the name of the Specialty) this converts every rolled 10 to two Net Successes. 

Willpower: True (defaults to False when not set) adds 1 to the Net successes. 
