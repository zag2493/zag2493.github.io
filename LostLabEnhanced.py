import sqlite3  # Used for databases Reference: https://docs.python.org/3/library/sqlite3.html
import networkx as nx  # Added for graph modeling Reference: https://networkx.org/documentation/stable/tutorial.html
import tkinter as tk  # Added for Graphic Interface, Reference: https://docs.python.org/3/library/tkinter.html
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt  # Show statistical data Reference: https://matplotlib.org/
import re  # added for regex


class Room:
    # Represents rooms in game with exits and their items
    def __init__(self, name, item=None, required_items=None):
        self.name = name
        self.item = item
        self.exits = {}
        self.required_items = required_items if required_items is not None else set()

    def add_exit(self, direction, room):
        # Add exit to another room in specified direction
        self.exits[direction.lower()] = room

    def get_exit(self, direction):
        # Get room in specified direction if exists
        return self.exits.get(direction.lower())


class Player:
    # Represent player with current room and their inventory
    def __init__(self, current_room, player_id=None):
        self.current_room = current_room
        self.inventory = set()
        self.id = player_id  # Links to Database

    def move(self, direction):
        # Move to room based on specific direction if allowed
        next_room = self.current_room.get_exit(direction)
        if next_room:
            missing = next_room.required_items - self.inventory
            if missing:
                # Sort missing items
                missing_sorted = sorted(missing)
                error_message = f"Cannot enter {next_room.name}: missing {', '.join(missing_sorted)}."
                # Popup warning for hazard
                messagebox.showwarning(
                    "Hazard Alert",
                    f"You cannot enter {next_room.name}!\nMissing required items: {', '.join(missing)}.\n"
                    "The room contains hazardous conditions!"
                )
                return error_message
            self.current_room = next_room
            return f"You moved to {self.current_room.name}."
        return "You can't go that way!"

    def take_item(self, item):
        # Pickup item in current room
        if self.current_room.item and self.current_room.item.lower() == item.lower():
            if self.current_room.item not in self.inventory:
                item_taken = self.current_room.item
                self.inventory.add(item_taken)
                self.current_room.item = None
                return f"You picked up {item_taken}."
            return "You already have this item."
        return f"There is no {item} here."


class Game:
    # Manage game state, logic, database, and GUI
    def __init__(self):
        self.rooms = {}
        self.graph = nx.Graph()  # Initialize NetworkX graph
        self.room_positions = {}
        self.setup_rooms()
        self.db_init()
        self.player = Player(self.rooms['Rec Room'], self.get_or_create_player("Hero"))
        self.target_items = 8

    # Setup Database
    def db_init(self):
        # Initialize SQLite database with required tables players, inventory, rooms, and logs.
        try:
            with sqlite3.connect("lostlab.db") as conn:
                conn.execute("PRAGMA foreign_keys = ON")  # Turn on Foreign key enforcement
                cur = conn.cursor()
                # Create table for players with ID, name, current room, and creation timestamp
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS player (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL UNIQUE,
                        current_room TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                # Create table for inventory linked to players
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS inventory (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        player_id INTEGER NOT NULL,
                        item TEXT NOT NULL,
                        acquired_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (player_id) REFERENCES player(id) ON DELETE CASCADE
                    )
                """)
                # Create table for rooms and their items
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS rooms (
                        name TEXT PRIMARY KEY,
                        item TEXT
                    )
                """)
                # Create log table to record player actions
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        player_id INTEGER,
                        action TEXT NOT NULL,
                        details TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (player_id) REFERENCES player(id)
                    )
                """)
                # Initialize rooms table only if empty
                cur.execute("SELECT COUNT(*) FROM rooms")
                if cur.fetchone()[0] == 0:
                    for room_name, room in self.rooms.items():
                        cur.execute("INSERT INTO rooms (name, item) VALUES (?, ?)", (room_name, room.item))
                conn.commit()
        except sqlite3.Error as e:
            print(f"Database initialization error: {e}")

    def get_or_create_player(self, name):
        # Retrieve existing player by name or create a new one.
        try:
            with sqlite3.connect("lostlab.db") as conn:
                cur = conn.cursor()
                cur.execute("SELECT id FROM player WHERE name = ?", (name,))
                row = cur.fetchone()
                if row:
                    return row[0]
                cur.execute("INSERT INTO player (name, current_room) VALUES (?, ?)", (name, "Rec Room"))
                player_id = cur.lastrowid
                conn.commit()
                return player_id
        except sqlite3.Error as e:
            print(f"Error creating/retrieving player: {e}")
            return None

    def save_to_db(self):
        # Save game state to database.
        try:
            with sqlite3.connect("lostlab.db") as conn:
                cur = conn.cursor()
                # Update players current room
                cur.execute("UPDATE player SET current_room = ? WHERE id = ?",
                            (self.player.current_room.name, self.player.id))
                # Remove all previous inventory items for player
                cur.execute("DELETE FROM inventory WHERE player_id = ?", (self.player.id,))
                # Insert current inventory items
                for item in self.player.inventory:
                    cur.execute("INSERT INTO inventory (player_id, item) VALUES (?, ?)",
                                (self.player.id, item))
                # Update the items in all rooms
                for room_name, room in self.rooms.items():
                    cur.execute("UPDATE rooms SET item = ? WHERE name = ?",
                                (room.item, room_name))
                conn.commit()
                # Record save in log table
                self.log_action("save", f"Game saved at {self.player.current_room.name}")
                return "Game saved to database."
        except sqlite3.Error as e:
            return f"Error saving game: {e}"

    def load_from_db(self):
        # Load game state from database.
        try:
            with sqlite3.connect("lostlab.db") as conn:
                cur = conn.cursor()
                # Load players current room
                cur.execute("SELECT current_room FROM player WHERE id = ?", (self.player.id,))
                row = cur.fetchone()
                if not row:
                    return "Error: No saved data for this player."
                if row[0] not in self.rooms:
                    return f"Error: Saved room '{row[0]}' not found."
                self.player.current_room = self.rooms[row[0]]

                # Load players inventory
                self.player.inventory.clear()
                cur.execute("SELECT item FROM inventory WHERE player_id = ?", (self.player.id,))
                for (item,) in cur.fetchall():
                    self.player.inventory.add(item)

                # Load items for all rooms
                cur.execute("SELECT name, item FROM rooms")
                for name, item in cur.fetchall():
                    if name in self.rooms:
                        self.rooms[name].item = item

                # Record this load in log table
                self.log_action("load", f"Game loaded at {self.player.current_room.name}")
                return "Game loaded from database."
        except sqlite3.Error as e:
            return f"Error loading game: {e}"

    def log_action(self, action, details):
        # Log player actions to database.
        try:
            with sqlite3.connect("lostlab.db") as conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO logs (player_id, action, details) VALUES (?, ?, ?)",
                            (self.player.id, action, details))
                conn.commit()
        except sqlite3.Error as e:
            print(f"Error logging action: {e}")

    def plot_win_lose(self):
        # Visualize frequency of win vs. lose outcomes.
        try:
            with sqlite3.connect("lostlab.db") as conn:
                cur = conn.cursor()
                cur.execute("SELECT action, COUNT(*) FROM logs WHERE action IN ('win', 'lose') GROUP BY action")
                data = cur.fetchall()
                if not data:
                    return "No win/lose data to visualize."
                outcomes = [row[0].capitalize() for row in data]
                counts = [row[1] for row in data]
                plt.figure(figsize=(6, 4), facecolor='#2E2E2E')
                plt.bar(outcomes, counts, color=['#4CAF50', '#F44336'], width=0.4)
                plt.xlabel('Outcome', color='white')
                plt.ylabel('Frequency', color='white')
                plt.title('Win vs. Lose Outcomes', color='white')
                plt.gca().set_facecolor('#3C3C3C')
                plt.gca().tick_params(colors='white')
                plt.tight_layout()
                plt.show()
                return "Win/lose visualization displayed."
        except sqlite3.Error as e:
            return f"Error visualizing win/lose data: {e}"

    def highlight_path(self, target_room, canvas, duration=3000):
        # Highlight the shortest path to the target room on the canvas.
        canvas.delete("path")
        try:
            path = nx.shortest_path(self.graph, self.player.current_room.name, target_room, weight='weight')
            for room1, room2 in zip(path[:-1], path[1:]):
                x1, y1 = self.room_positions[room1]
                x2, y2 = self.room_positions[room2]
                canvas.create_line(x1, y1, x2, y2, fill="#F44336", width=3, tags="path")

            canvas.after(duration, lambda: canvas.delete("path"))

        except nx.NetworkXNoPath:
            pass

    def setup_rooms(self):
        # Initialize rooms and exits
        rooms_data = {
            'Rec Room': {'item': None, 'required_items': set()},
            'Decontamination': {'item': 'Empty Laser Weapon', 'required_items': set()},
            'Terrarium': {'item': 'The Alien!', 'required_items': set()},
            'Lab': {'item': 'Recording', 'required_items': set()},
            'Med Bay': {'item': 'Medical Supplies', 'required_items': {'MKIV Suit', 'MKV Helmet'}},
            'Cargo Hold': {'item': 'MKIV Suit', 'required_items': set()},
            'Sleeping Quarters': {'item': 'Artifact', 'required_items': set()},
            'Bathroom': {'item': 'MKV Helmet', 'required_items': set()},
            'Mess Hall': {'item': 'Ammo', 'required_items': set()},
            'Water Treatment': {'item': 'Shield Charge', 'required_items': set()}
        }

        for name, data in rooms_data.items():
            self.rooms[name] = Room(name, data['item'], data['required_items'])
            self.graph.add_node(name)  # Add room as a node in graph

        self.room_positions = {
            'Rec Room': (400, 140),
            'Sleeping Quarters': (400, 40),
            'Decontamination': (400, 240),
            'Terrarium': (400, 330),
            'Mess Hall': (550, 140),
            'Bathroom': (550, 40),
            'Water Treatment': (550, 240),
            'Med Bay': (250, 140),
            'Lab': (250, 240),
            'Cargo Hold': (250, 40)
        }

        exits = {
            'Rec Room': {'north': 'Sleeping Quarters', 'south': 'Decontamination',
                         'east': 'Mess Hall', 'west': 'Med Bay'},
            'Decontamination': {'north': 'Rec Room', 'south': 'Terrarium',
                                'east': 'Water Treatment', 'west': 'Lab'},
            'Terrarium': {'north': 'Decontamination'},
            'Lab': {'north': 'Med Bay', 'east': 'Decontamination'},
            'Med Bay': {'north': 'Cargo Hold', 'south': 'Lab', 'east': 'Rec Room'},
            'Cargo Hold': {'south': 'Med Bay', 'east': 'Sleeping Quarters'},
            'Sleeping Quarters': {'south': 'Rec Room', 'east': 'Bathroom', 'west': 'Cargo Hold'},
            'Bathroom': {'south': 'Mess Hall', 'west': 'Sleeping Quarters'},
            'Mess Hall': {'north': 'Bathroom', 'south': 'Water Treatment', 'west': 'Rec Room'},
            'Water Treatment': {'north': 'Mess Hall', 'west': 'Decontamination'}
        }
        for room_name, room_exits in exits.items():
            for direction, target_room in room_exits.items():
                self.rooms[room_name].add_exit(direction, self.rooms[target_room])
                weight = 1
                if not self.graph.has_edge(room_name, target_room):
                    self.graph.add_edge(room_name, target_room, weight=1)

    def show_instructions(self):
        # Display Instructions
        return (
            'Collect all 8 items to win the game, or be prepared to face the Alien\n'
            'Use the movement buttons to navigate: North, South, East, West\n'
            'Enter the item name and click "Get Item" to add to inventory\n'
            'Select a room from the dropdown and click "Find Path" for the shortest route\n'
            'Enter a filename and click "Save" or "Load" to manage game state\n'
            'Click "Exit" to quit'
        )

    def shortest_path(self, target_room):
        """ Suggest the shortest path to a targeted room using Dijkstra algorithm
            choice for Dijkstra is based on using weight but also to potentially add more complexity to the game later,
            if added complexity was not in play a Breadth-First search may be a potentially better fit. """
        try:
            if target_room not in self.rooms:
                return f"Room '{target_room}' does not exist."

            # Update edge weights: only Med Bay is hazardous
            for room1, room2, data in self.graph.edges(data=True):
                # Check if either side is Med Bay
                if 'Med Bay' in (room1, room2):
                    # If player is missing required items for Med Bay, assign high weight
                    missing_items = self.rooms['Med Bay'].required_items - self.player.inventory
                    data['weight'] = 100 if missing_items else 1
                else:
                    data['weight'] = 1  # normal room

            # Compute the shortest path using updated weights
            path = nx.shortest_path(
                self.graph,
                source=self.player.current_room.name,
                target=target_room,
                weight='weight'
            )
            return f"Shortest path to {target_room}: {' -> '.join(path)}"

        except nx.NetworkXNoPath:
            return f"No path to {target_room}."
        except nx.NodeNotFound:
            return f"Room '{target_room}' does not exist."

    def check_victory(self):
        # Check if the player has won (8 items and in Terrarium)
        if (
                len(self.player.inventory) == self.target_items
                and self.player.current_room.name == "Terrarium"
        ):
            self.log_action("win", "Player defeated the Alien with all items!")
            return True
        return False

    def check_defeat(self):
        # Check if the player has lost (less than 8 items in Terrarium)
        if (
                len(self.player.inventory) != self.target_items
                and self.player.current_room.name == "Terrarium"
        ):
            self.log_action("lose", "Player was defeated by the Alien!")
            return True
        return False

    def play_gui(self):
        # Run game with Tkinter Interface
        root = tk.Tk()
        root.title("Lost Lab")
        root.geometry("1000x800")
        root.configure(bg="#2E2E2E")  # Dark Theme Background

        # TTK style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TButton", font=("Segoe UI", 10), padding=10, background="#2196F3", foreground="white")
        style.map("TButton", background=[('active', '#1976D2')])
        style.configure("TCombobox", font=("Segoe UI", 10), padding=5)
        style.configure("TLabel", font=("Segoe UI", 12), background="#2E2E2E", foreground="white")
        style.configure("TFrame", background="#3C3C3C")

        # Create Grid Configuration
        root.rowconfigure(0, weight=0)  # Instructions
        root.rowconfigure(1, weight=0)  # Status
        root.rowconfigure(2, weight=1)  # Canvas
        root.rowconfigure(3, weight=0)  # Controls
        root.columnconfigure(0, weight=1)

        # Display Instructions
        instructions_outer_frame = ttk.Frame(root)
        instructions_outer_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        instructions_outer_frame.columnconfigure(0, weight=1)

        instructions_frame = ttk.Frame(instructions_outer_frame, padding=10, relief="groove")
        instructions_frame.grid(row=0, column=0, padx=10, pady=5, sticky="n")  # Center with sticky="n"
        instructions_title = ttk.Label(instructions_frame, text="Lost Lab: Instructions",
                                       font=("Segoe UI", 14, "bold"))
        instructions_title.pack(pady=(0, 5))
        instructions_text = tk.Text(instructions_frame, height=6, width=60, bg="#3C3C3C", fg="white",
                                    font=("Segoe UI", 12), wrap="word", borderwidth=0)
        instructions_text.insert("1.0", self.show_instructions())
        instructions_text.config(state="disabled")  # Read-only
        instructions_text.pack(pady=5, padx=5)

        # Status frame
        status_frame = ttk.Frame(root, padding=10, relief="groove")
        status_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        room_label = ttk.Label(status_frame, text=f"Current Room: {self.player.current_room.name}")
        room_label.pack(pady=2)
        inventory_label = ttk.Label(status_frame, text="Inventory: Empty")
        inventory_label.pack(pady=2)
        item_label = ttk.Label(status_frame, text="You see: None")
        item_label.pack(pady=2)

        # Map Canvas Reference: https://www.geeksforgeeks.org/python/python-tkinter-canvas-widget/
        canvas_frame = ttk.Frame(root, padding=10, relief="groove")
        canvas_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        canvas_frame.rowconfigure(0, weight=1)
        canvas_frame.columnconfigure(0, weight=1)
        canvas = tk.Canvas(canvas_frame, width=800, height=600, bg="#3C3C3C", highlightthickness=0)
        canvas.grid(row=0, column=0)
        canvas_frame.grid_propagate(False)
        canvas_frame.update_idletasks()

        # Draw rooms and their exits, Canvas Reference
        room_oval_ids = {}
        item_text_ids = {}
        for room, pos in self.room_positions.items():
            x, y = pos
            oval = canvas.create_oval(x - 40, y - 40, x + 40, y + 40,
                                      fill="#2196F3" if room == self.player.current_room.name else "#616161",
                                      outline="white", width=2)
            canvas.create_text(x, y, text=room, font=("Segoe UI", 10, "bold"), fill="white")
            room_oval_ids[room] = oval  # Save room id for updates
            # Draw item if present - commented out, used for testing
            # Prevent spoiling alien location
            # item = self.rooms[room].item
            # item_text = canvas.create_text(x, y + 15, text=item if item else "", font=("Arial", 7), fill="red")
            # item_text_ids[room] = item_text

        # Color edges
        for room1, room2, _ in self.graph.edges(data=True):
            x1, y1 = self.room_positions[room1]
            x2, y2 = self.room_positions[room2]
            canvas.create_line(x1, y1, x2, y2, fill="white", width=2)

        # Add Compass - top right corner
        # Reference:
        # https://www.geeksforgeeks.org/python/python-tkinter-create-different-type-of-lines-using-canvas-class/
        compass_x, compass_y = 650, 50
        canvas.create_text(compass_x, compass_y - 40, text="Compass", font=("Segoe UI", 10, "bold"), fill="white")
        canvas.create_line(compass_x, compass_y, compass_x, compass_y - 20, arrow=tk.LAST, fill="white", width=2)
        canvas.create_text(compass_x, compass_y - 25, text="N", font=("Segoe UI", 8), fill="white")  # North
        canvas.create_line(compass_x, compass_y, compass_x, compass_y + 20, arrow=tk.LAST, fill="white", width=2)
        canvas.create_text(compass_x, compass_y + 25, text="S", font=("Segoe UI", 8), fill="white")  # South
        canvas.create_line(compass_x, compass_y, compass_x + 20, compass_y, arrow=tk.LAST, fill="white", width=2)
        canvas.create_text(compass_x + 25, compass_y, text="E", font=("Segoe UI", 8), fill="white")  # East
        canvas.create_line(compass_x, compass_y, compass_x - 20, compass_y, arrow=tk.LAST, fill="white", width=2)
        canvas.create_text(compass_x - 25, compass_y, text="W", font=("Segoe UI", 8), fill="white")  # West

        # Control frame - organize all controls
        controls_frame = ttk.Frame(root, padding=10, relief="groove")
        controls_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=(10, 20))

        # Reference design: https://www.geeksforgeeks.org/python/using-lambda-in-gui-programs-in-python/
        # Movement buttons
        nav_frame = ttk.Frame(controls_frame)
        nav_frame.pack(pady=3)
        ttk.Button(nav_frame, text="North", command=lambda: handle_action("north")).pack(side=tk.LEFT, padx=5)
        ttk.Button(nav_frame, text="South", command=lambda: handle_action("south")).pack(side=tk.LEFT, padx=5)
        ttk.Button(nav_frame, text="East", command=lambda: handle_action("east")).pack(side=tk.LEFT, padx=5)
        ttk.Button(nav_frame, text="West", command=lambda: handle_action("west")).pack(side=tk.LEFT, padx=5)

        # Item pickup
        item_frame = ttk.Frame(controls_frame)
        item_frame.pack(pady=3)
        item_entry = ttk.Entry(item_frame, width=20, font=("Segoe UI", 10))
        item_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(item_frame, text="Get Item",
                   command=lambda: handle_action(f"get {item_entry.get()}")).pack(side=tk.LEFT, padx=5)

        # Pathfinding
        path_frame = ttk.Frame(controls_frame)
        path_frame.pack(pady=3)
        path_var = tk.StringVar()
        path_dropdown = ttk.Combobox(path_frame, textvariable=path_var, values=list(self.rooms.keys()), width=20)
        path_dropdown.pack(side=tk.LEFT, padx=5)
        ttk.Button(path_frame, text="Find Path",
                   command=lambda: handle_action(f"path {path_var.get()}")).pack(side=tk.LEFT, padx=5)

        # Save/load/exit
        game_controls_frame = ttk.Frame(controls_frame)
        game_controls_frame.pack(pady=3)
        ttk.Button(game_controls_frame, text="Save", command=lambda: handle_action("save")).pack(side=tk.LEFT, padx=5)
        ttk.Button(game_controls_frame, text="Load", command=lambda: handle_action("load")).pack(side=tk.LEFT, padx=5)
        ttk.Button(game_controls_frame, text="Visualize Win/Lose",
                   command=lambda: handle_action("winlose")).pack(side=tk.LEFT, padx=5)
        ttk.Button(game_controls_frame, text="Exit", command=root.destroy).pack(side=tk.LEFT, padx=5)

        # Status Bar
        status_bar = ttk.Label(root, text="", font=("Segoe UI", 10), background="#2E2E2E", foreground="white")
        status_bar.grid(row=4, column=0, sticky="ew")

        def update_gui():
            # Update map on game state
            room_label.config(text=f"Current Room: {self.player.current_room.name}")
            inventory_label.config(
                text=f"Inventory: {', '.join(self.player.inventory) if self.player.inventory else 'Empty'}")
            item_label.config(
                text=f"You See: {self.player.current_room.item if self.player.current_room.item else 'None'}")
            for room, oval_id in room_oval_ids.items():
                canvas.itemconfig(oval_id, fill="#2196F3" if room == self.player.current_room.name else "#616161")
            # Commented out to not spoil alien location
            # for room, text_id in item_text_ids.items():
            #    item = self.rooms[room].item
            #    canvas.itemconfig(text_id, text=item if item else "")
            # Victory Condition
            if self.check_victory():
                messagebox.showinfo("Victory", "You did it! You have conquered the Alien!")
                root.destroy()
            elif self.check_defeat():
                messagebox.showerror("Defeat", "You were not prepared! The Alien has defeated you!")
                root.destroy()

        def handle_action(action):
            # Handle all user actions and update interface
            try:
                # Move Player
                if action in ['north', 'south', 'east', 'west']:
                    result = self.player.move(action)
                # Item Pickup
                elif action.startswith('get '):
                    item = action[4:].strip()
                    if not item:
                        raise ValueError("Please specify an item to get.")
                    if not re.match(r'^[a-zA-Z\s]+$', item):
                        raise ValueError("Item name must contain only letters and spaces.")
                    result = self.player.take_item(item)
                # Shortest Path
                elif action.startswith('path '):
                    target = action[5:].strip().title()
                    if not target:
                        raise ValueError("Please specify a room.")
                    result = self.shortest_path(target)
                    self.highlight_path(target, canvas)
                # Save Game
                elif action == 'save':
                    result = self.save_to_db()
                # Load Game
                elif action == 'load':
                    result = self.load_from_db()
                elif action == 'winlose':
                    result = self.plot_win_lose()
                else:
                    raise ValueError("Invalid action.")
                status_bar.config(text=result)
                update_gui()
            except ValueError as e:
                status_bar.config(text=str(e))

        update_gui()
        root.mainloop()


if __name__ == '__main__':
    game = Game()
    game.play_gui()
