# Initiative Tracker
# Version 0.2
# 
# Newly Added:
# -GUI
#
# By: Gabe Williams

# This class sets up the combatant object. 
# This object holds the name and the roll of the combatant.
from symbol import argument
import PySimpleGUI as sg

class Combatant:
    def __init__(self, name, roll):
        self.name = name
        self.roll = roll
    def __str__(self):
        return f"{self.name} ({self.roll})"
    def __repr__(self):
        return repr((self.name, self.roll))
    
#Menu Options:
#1. Create a new List - starting from an empty list
#2. Edit the current List - do the same process but with a current list
#3. Quit the application - type quit and it prints and ends the program
def initiative_creator(name, roll, initiative_order):
    # Take that input (Name and Initiative Roll) and put it into a list
    initiative_order.append(Combatant(name, int(roll)))
    # Sort that list in descending order for the moment
    initiative_order.sort(key=lambda x: x.roll, reverse=True)
    return initiative_order

def display_list(updated_list):
    #updates the listbox element with the new list contents
    window['-DISPLAY LIST-'].update(updated_list)
    msg = "List updated successfully!"
    window['-MSG-'].update(msg)

def update_list(index, name, roll):
    # Find the index of the edited row

    # Update the row with a new entry

    # Send a message saying that the row has been updated
    msg = "Entry has been updated successfully!"
    window['-MSG-'].update(msg)


# Create the initiative list
initiative_list = []

# Creating both sides of the layout.
# Input Side
input_column = [
    [
        sg.Text("Combatant's Name"),
        sg.InputText(key= "-NAME-")
    ],
    [
        sg.Text("Combatant's Initiative Roll"),
        sg.InputText(key= "-ROLL-")
    ],
    [sg.Submit()],
    [
    sg.Text("Welcome! Please Enter your Combatant's Names and Initiative Rolls", key="-MSG-")
    ],
]

# Display Initiave List
display_column = [
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-DISPLAY LIST-"
        )
    ],
    [
        sg.Button("Edit", key="-EDIT-"),
        sg.Button("Delete", key="-DELETE-") 
    ],
]

#Full Layout
layout = [
    [
        sg.Column(input_column),
        sg.VSeparator(),
        sg.Column(display_column),
    ]
]

#Main window
window = sg.Window("Initiative Tracker", layout)

#Event Loop
while True:
    event, values = window.read()
     
    # End program if user closes window or
    # presses the OK button
    if event == sg.WIN_CLOSED:
        break
    elif event == "Submit":
        name_value = values["-NAME-"]
        roll_value = values["-ROLL-"]
        initiative_list = initiative_creator(name_value, roll_value, initiative_list)
        display_list(initiative_list)
    elif event == "-DISPLAY LIST-":
        selection = values[event]
        if selection:
            item = selection[0]
            index = window['-DISPLAY LIST-'].get_indexes()[0]
            print(index)
            #Put the selection's name and roll in the text fields
            #Figure out a way to allow for edits (Maybe check for an index?)

        
#Close after loop is done
window.close()





 
