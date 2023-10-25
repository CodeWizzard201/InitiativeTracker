# Initiative Tracker
# Version 0.3
# 
# Newly Added:
# -Ability to Save
# -Ability to Delete
#
# By: Gabe Williams

# This class sets up the combatant object. 
# This object holds the name and the roll of the combatant.
import PySimpleGUI as sg
import os

class Combatant:
    def __init__(self, name, roll):
        self.name = name
        self.roll = roll
    def __str__(self):
        return f"{self.name} ({self.roll})"
    def __repr__(self):
        return repr((self.name, self.roll))
#Functions    
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
    # Find the index of the edited row and delete it from the list
    delete_entry(index)

    # Update the row with a new entry
    initiative_list.append(Combatant(name,int(roll)))
    initiative_list.sort(key=lambda x: x.roll, reverse=True)

    # Send a message saying that the row has been updated
    msg = "Entry has been updated successfully!"
    window['-MSG-'].update(msg)

def delete_entry(index):
    if initiative_list:
        initiative_list.pop(index)

def clear_list():
    initiative_list.clear()

def save_list():
    msg = "Saving List..."
    window['-MSG-'].update(msg)
    file = sg.filedialog.asksaveasfile(defaultextension='.txt', filetypes=[
        ("Text file", '.txt'),
        ("CSV file", '.csv'),
        ("All files", '.*')
    ])
    [file.write("%s\n" % item) for item in initiative_list]
    
    file.close()
    msg = "List Saved!"
    window['-MSG-'].update(msg)

def load_list():
    msg = "Loading List..."
    window['-MSG-'].update(msg)
    # Allows user to select a file to load a preset list from
    file = sg.filedialog.askopenfile(mode = 'r', filetypes =[
        ("Text file", '.txt'),
        ("CSV file", '.csv'),
        ("All files", '.*')
    ])
    #If the file has content, unpack it into a list to send back to the initiative_list
    if file:
        #Clear Initiative list
        clear_list()
        temp_list = []
        for line in file:
            content = line.strip()
            loadedList = content.split('\n')
            #Take each element and split 'Name, (Roll)' into 'Name' and '(Roll)'
            for element in loadedList:
                splitData = element.split(' ')
                splitData[1] = splitData[1].replace("(","").replace(")","")
                #Use the creator to recreate the new list of initiative rolls
                temp_list = initiative_creator(splitData[0], int(splitData[1]), temp_list)
                print(temp_list)

        return temp_list
    file.close()
    msg = "List Loaded!"
    window['-MSG-'].update(msg)
    pass


# Create the initiative list
initiative_list = []
working_directory = os.getcwd()

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
        sg.Button("Save", key="-SAVE-"),
        sg.Button("Load", key="-LOAD-"),
        sg.Button("Edit", key="-EDIT-"),
        sg.Button("Delete", key="-DELETE-"),
        sg.Button("Clear All", key="-CLEAR ALL-") 
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
        #TODO ask if the user wants to save their list IF there is at least one entry
        break
    #Adds new entry to list
    elif event == "Submit":
        name_value = values["-NAME-"]
        roll_value = values["-ROLL-"]
        initiative_list = initiative_creator(name_value, roll_value, initiative_list)
        display_list(initiative_list)
    #Saves to a file designated by user
    elif event == "-SAVE-":
        save_list()
    #Loads from file overwriting the current list of entries
    elif event == "-LOAD-":
        # get the list from the file and overwrite the current list
        # overwrite prompt if you want to save the current list first
        initiative_list = load_list()
        display_list(initiative_list)
    elif event == "-EDIT-":
        #Catch errors if there is no selection
        try:
            edited_name = sg.popup_get_text("Enter the Modified Name:", title="Edit Entry")
            edited_roll = sg.popup_get_text("Enter the Modified Roll:", title="Edit Entry")
            update_list(index, edited_name, edited_roll)
        except NameError:
            msg = "There is no selection!"
            window["-MSG-"].update(msg)
        display_list(initiative_list)
    elif event == "-DELETE-":
        #Catch errors if there is no selection
        try:
            delete_entry(index)
            display_list(initiative_list)
        except NameError:
            msg = "There is no selection!"
            window["-MSG-"].update(msg)
    elif event == "-DISPLAY LIST-":
        selection = values[event]
        if selection:
            item = selection[0]
            index = window['-DISPLAY LIST-'].get_indexes()[0]
    elif event == "-CLEAR ALL-":
        confirmation = sg.popup_yes_no("Are you sure you want to clear the list?", title="Clear All")
        if confirmation:
            clear_list()
            display_list(initiative_list)
        
#Close after loop is done
window.close()