import json
import sys
# # Load the game map from the file and validate it

with open(sys.argv[1]) as f:
    game_map = json.load(f)
for room in game_map:
    if 'name' not in room:
        print("Error: Room missing name")
        sys.exit(1)
    if 'desc' not in room:
        print("Error: Room missing desc")
        sys.exit(1)
    if 'exits' not in room:
        print("Error: Room missing exits")
        sys.exit(1)

    # Check that each exit points to a valid room index
    for direction, room_index in room['exits'].items():
        if not isinstance(room_index, int) or room_index < 0 or room_index >= len(game_map):
            print(f"Error: Invalid exit in room {room['name']}: {direction} -> {room_index}")
            sys.exit(1)
# Initialize the game world
current_room = 0
inventory = []
directions=["north","south","east","west","northwest","southwest","northeast","southeast"]

room= game_map[current_room]
print(f"> {room['name']}\n")
print(f"{room['desc']}\n")
if('items' in room and room['items'] !=[]):
    print("Items:",", ".join(room['items']))
    print()
print("Exits:", " ".join(room['exits']))
print()

while True:
        try: 
            command = input("What would you like to do? ").strip().lower()
        #  handle_input(command)
        # Parse the input and execute the command
            if command.lower().startswith("go"):
                direction = command[3:].lower()
                if(command.strip() == 'go'):
                    print("Sorry, you need to 'go' somewhere.")
                elif direction in (dir.lower() for dir in room['exits']):
                    print(f"You go {direction}.\n")
                    for dir in room['exits']:
                        if dir.lower() == direction:
                            direction=dir
                    current_room = room['exits'][direction]
                    room= game_map[current_room]
                    print(f"> {room['name']}\n")
                    print(f"{room['desc']}\n")
                    if('items' in room):
                          print("Items:",", ".join(room['items']).lower())
                          print()
                    print("Exits:", " ".join(room['exits']).lower())
                    print()
                else:
                    l=[]
                    f=0
                    for exit in room['exits']:
                        if exit.lower().startswith(direction):
                            l.append(exit)
                            f=1
                    if f==1:
                        print("Did you want me to go ","or ".join(l))
                    else:
                        print(f"There's no way to go {direction}.")

            elif command.lower().startswith('get'): 
                if(command.strip().lower() == 'get'):
                    print("Sorry, you need to 'get' something.")
                elif 'items' not in room:
                    print(f"There's no {command[4:]} anywhere.")
                elif(command[4:].lower() in (item.lower() for item in room['items'])):
                    item= command[4:].lower()
                    for i in room['items']: 
                        if i.lower == item:
                            item=i
                    inventory.append(item)
                    room['items'].remove(item)
                    print(f"You pick up the {item}.")
                else:
                    print(f"There's no {command[4:]} anywhere.")

            elif command.lower() == "look":
                print(f"> {room['name']}\n")
                print(f"{room['desc']}\n")
                
                
                if('items' in room and room['items'] !=[]):
                    print("Items:",", ".join(room['items']))
                    print()
                print("Exits:", " ".join(room['exits']))
                print()
            elif command.lower() == "inventory":
                if item in inventory!=[]:
                    print("Inventory:")
                    for item in inventory:
                    
                        print(f"  {item}")
                else:
                    print("You're not carrying anything.")

            elif command.lower().startswith("drop"):
                item=command[5:].lower()
                if "items" not in room and item in (i.lower() for i in inventory):
                    for i in inventory:
                        if i.lower()==item:
                            item=i
                    room["items"]=[item]
                    inventory.remove(item)
                    print("You drop the ",item)
                elif item in (i.lower() for i in inventory):
                    for i in inventory:
                        if i.lower()==item:
                            item=i
                    inventory.remove(item)
                    room['items'].append(item)
                    print("You drop the",item)
                elif len(inventory)==0:
                    print("Sorry, your inventory is empty, so cannot drop.")
                else:
                    print("Sorry ",item," is not in inventory.")

            elif command.lower() == "boss open":
                if "magic wond" in inventory and "sword" in inventory:
                    print("Congatulation!! You win.")
                else:
                    print("Sorry! You lose. Try again.")
                break

            elif command.lower() == "help":
                print("You can run the following commands:")
                print("  go ...\t")
                print("  get ...\t")
                print("  look\t")
                print("  inventory\t")
                print("  drop\t")
                print("  boss open\t")
                print("  help\t")
                print("  quit\t")
            
            elif command.lower().startswith("quit"):
                print("Goodbye!")
                break
            else:
                direction=command
                if direction in (dir.lower() for dir in room['exits']):
                    print(f"You go {direction}.\n")
                    for dir in room['exits']:
                        if dir.lower() == direction:
                            direction=dir
                    current_room = room['exits'][direction]
                    room= game_map[current_room]
                    print(f"> {room['name']}\n")
                    print(f"{room['desc']}\n")
                    if('items' in room):
                        print("Items:",", ".join(room['items']))
                        print("")
                        print("Exits:", " ".join(room['exits']))
                        print("")
                elif command.lower() in directions and command.lower() not in room['exits']:
                        print(f"There's no way to go {command}")
                else:
                    l=[]
                    f=0
                    for exit in room['exits']:
                        if exit.lower().startswith(direction):
                            l.append(exit)
                            f=1
                    if f==1:
                        print("Did you want me to go ","or ".join(l))
                    else:
                        print("Please enter vaid command.")
        except EOFError:
            print("\nUse 'quit' to exit.")
