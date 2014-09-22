MIRLInventory
=============

Simple Inventory program to track checked out items

##Purpose

This is to be a simplified, person-based checkout system for loaning items to students in the MachineInteligenceRoboticsLab. In the final form, this program will email people when they are checking items out, assign due dates, and perform basic custodial warning functions in an attempt to get back the items that are taken by people.

##Instalation

Tested on debian based systems. To install, we must take care of some dependencies. 

>sudo apt-get install python-tk python-imaging python-imaging-tk

After that, simply clone the repository

>git clone https://github.com/glop102/MIRLInventory

To run the program

>python main.py
>  **or**
>./main.py