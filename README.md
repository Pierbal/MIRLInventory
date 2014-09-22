MIRLInventory
=============

Simple Inventory program to track checked out items

##Purpose

This is to be a simplified, person-based checkout system for loaning items to students in the MachineInteligenceRoboticsLab. In the final form, this program will email people when they are checking items out, assign due dates, and perform basic custodial warning functions in an attempt to get back the items that are taken by people.

##Features

1. People List with basic information such as email
2. Highlighing of items that a person has checked out
3. Automatic Email when a person checks in/out an item
4. Does not allow people to check out more items than in the system
5. Automaticly Emails people with overdue items every 4 hours (will allow changing defaults soon)
6. Fully featured Admin window protected by a password. (will allow changing defaults soon)

##Instalation

Tested on debian based systems. To install, we must take care of some dependencies. 

>sudo apt-get install python-tk python-imaging python-imaging-tk

After that, simply clone the repository

>git clone https://github.com/glop102/MIRLInventory

To run the program

>python main.py
>
>  **or**
>
>./main.py