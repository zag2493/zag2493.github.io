# Zach Garrison


# Dictionary for rooms
rooms = {
    'Rec Room': {'North': 'Sleeping Quarters', 'South': 'Decontamination', 'East': 'Mess Hall', 'West': 'Med Bay',
                 'item': 'Nothing'},
    'Decontamination': {'North': 'Rec Room', 'South': 'Terrarium', 'East': 'Water Treatment', 'West': 'Lab',
                        'item': 'Empty Laser Weapon'},
    'Terrarium': {'North': 'Decontamination', 'item': 'The Alien!'},
    'Lab': {'North': 'Med Bay', 'East': 'Decontamination', 'item': 'Recording'},
    'Med Bay': {'North': 'Cargo Hold', 'South': 'Lab', 'East': 'Rec Room', 'item': 'Medical Supplies'},
    'Cargo Hold': {'South': 'Med Bay', 'East': 'Sleeping Quarters', 'item': 'MKIV Suit'},
    'Sleeping Quarters': {'South': 'Rec Room', 'East': 'Bathroom', 'West': 'Cargo Hold', 'item': 'Artifact'},
    'Bathroom': {'South': 'Mess Hall', 'West': 'Sleeping Quarters', 'item': 'MKV Helmet'},
    'Mess Hall': {'North': 'Bathroom', 'South': 'Water Treatment', 'West': 'Rec Room', 'item': 'Ammo'},
    'Water Treatment': {'North': 'Mess Hall', 'West': 'Decontamination', 'item': 'Shield Charge'}
}


# Add Directions Here
def show_instructions():
    print('---------------')
    print('Welcome to Lost Lab')  # Add Name of Game
    print('Collect all 8 Items to Win the Game, or Be Prepared to Face the Alien!')
    print('Move Commands: North, South, East, West')
    print('Add to Inventory: Get "Item Name" ')
    print('---------------')


# Start Player In Rec Room
starting_room = 'Rec Room'
current_room = starting_room

show_instructions()
inventory = []

# Start Loop Giving Status
while True:
    print('You are in the {}'.format(current_room))
    print('Inventory:', inventory)
    if 'item' in rooms[current_room]:
        print('You See ' + rooms[current_room]['item'])
    if len(inventory) != 8 and rooms[current_room]['item'] == 'The Alien!':
        print('You were not prepared, The Alien has defeated you!')
        break
    if len(inventory) == 8 and rooms[current_room]['item'] == 'The Alien!':
        print('You Did It! You have conquered The Alien!')
        break

    # Movement
    move = input('Enter Your Move: ').strip().title()
    print('---------------')

    # To Move To Next Room and Begin Item Pickup
    if move in rooms[current_room]:
        current_room = rooms[current_room][move]
    elif move.startswith('Get') and 'item' in rooms[current_room]:
        entered_item = move.split(' ', 1)[1]  # Get the item specified by the user
        expected_item = rooms[current_room]['item']
        if entered_item.lower() == expected_item.lower():
            if expected_item not in inventory:
                inventory.append(expected_item)
                print(f'You got {expected_item} and added it to your inventory.')
            else:
                print('You already have this item.')
        else:
            print(f'You cannot get {entered_item}. The expected item is {expected_item}.')
    else:
        print('Invalid Move, You can not go that way!')
