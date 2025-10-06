import unittest
import sqlite3
from LostLabEnhanced import Room, Player, Game


class TestLostLab(unittest.TestCase):
    def setUp(self):
        # Initialize a game setup and clear database for each test
        self.game = Game()
        self.player = self.game.player
        self.rooms = self.game.rooms
        # Clear database to ensure test isolation
        with sqlite3.connect("lostlab.db") as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM player")
            cur.execute("DELETE FROM inventory")
            cur.execute("DELETE FROM rooms")
            cur.execute("DELETE FROM logs")
            conn.commit()
        # Reinitialize rooms table and player
        self.game.db_init()
        self.player.id = self.game.get_or_create_player("Hero")

    def test_room_initialization(self):
        # Test Room class initialization
        room = Room("Test Room", item="Test Item")
        self.assertEqual(room.name, "Test Room")
        self.assertEqual(room.item, "Test Item")
        self.assertEqual(room.exits, {})

    def test_room_add_exit(self):
        # Test adding and retrieving exits
        room1 = Room("Room 1")
        room2 = Room("Room 2")
        room1.add_exit("north", room2)
        self.assertEqual(room1.get_exit("north"), room2)
        self.assertIsNone(room1.get_exit("south"))

    def test_valid_player_move(self):
        # Test moving to valid room
        self.player.current_room = self.rooms["Rec Room"]
        result = self.player.move("north")
        self.assertEqual(self.player.current_room.name, "Sleeping Quarters")
        self.assertEqual(result, "You moved to Sleeping Quarters.")

    def test_invalid_player_move(self):
        # Test moving invalid direction
        self.player.current_room = self.rooms["Rec Room"]
        result = self.player.move("up")
        self.assertEqual(self.player.current_room.name, "Rec Room")
        self.assertEqual(result, "You can't go that way!")

    def test_move_case_insensitive(self):
        # Test moving with case-insensitive direction
        self.player.current_room = self.rooms["Rec Room"]
        result = self.player.move("NorTH")
        self.assertEqual(self.player.current_room.name, "Sleeping Quarters")
        self.assertEqual(result, "You moved to Sleeping Quarters.")

    def test_valid_player_take_item(self):
        # Test picking up valid item
        self.player.current_room = self.rooms["Med Bay"]
        result = self.player.take_item("Medical Supplies")
        self.assertIn("Medical Supplies", self.player.inventory)
        self.assertIsNone(self.rooms["Med Bay"].item)
        self.assertEqual(result, "You picked up Medical Supplies.")

    def test_player_take_item_duplicate(self):
        # Test picking up item already in player's inventory
        self.player.current_room = self.rooms["Med Bay"]
        self.player.inventory.add("Medical Supplies")
        result = self.player.take_item("Medical Supplies")
        self.assertEqual(len(self.player.inventory), 1)
        self.assertEqual(result, "You already have this item.")

    def test_invalid_player_take_item(self):
        # Test picking up invalid item
        self.player.current_room = self.rooms["Med Bay"]
        result = self.player.take_item("Wrong Item")
        self.assertEqual(len(self.player.inventory), 0)
        self.assertEqual(result, "There is no Wrong Item here.")

    def test_player_take_item_case_insensitive(self):
        # Test case-insensitive item pickup
        self.player.current_room = self.rooms["Med Bay"]
        result = self.player.take_item("medical Supplies")
        self.assertIn("Medical Supplies", self.player.inventory)
        self.assertIsNone(self.rooms["Med Bay"].item)
        self.assertEqual(result, "You picked up Medical Supplies.")

    def test_take_nothing_item(self):
        # Test trying to pick up nothing in Rec Room
        self.player.current_room = self.rooms["Rec Room"]
        result = self.player.take_item("Nothing")
        self.assertEqual(result, "There is no Nothing here.")
        self.assertEqual(len(self.player.inventory), 0)

    def test_game_win_condition(self):
        # Test winning condition (8 items, face Alien)
        self.player.current_room = self.rooms["Terrarium"]
        self.player.inventory = {
            "Empty Laser Weapon", "Recording", "Medical Supplies", "MKIV Suit",
            "Artifact", "MKV Helmet", "Ammo", "Shield Charge"
        }
        self.assertTrue(self.game.check_victory())
        self.assertFalse(self.game.check_defeat())

    def test_game_lose_condition(self):
        # Test losing condition (less than 8 items, encounter Alien)
        self.player.current_room = self.rooms["Terrarium"]
        self.player.inventory = {"Medical Supplies", "MKIV Suit"}
        self.assertFalse(self.game.check_victory())
        self.assertTrue(self.game.check_defeat())

    def test_game_exit_connections(self):
        # Test some room exits to ensure correct setup
        self.assertEqual(self.rooms["Rec Room"].get_exit("north").name, "Sleeping Quarters")
        self.assertEqual(self.rooms["Terrarium"].get_exit("north").name, "Decontamination")
        self.assertIsNone(self.rooms["Terrarium"].get_exit("south"))

    def test_shortest_path_valid(self):
        # Test shortest path to Terrarium
        self.player.current_room = self.rooms["Rec Room"]
        result = self.game.shortest_path("Terrarium")
        self.assertEqual(result, "Shortest path to Terrarium: Rec Room -> Decontamination -> Terrarium")

    def test_shortest_path_invalid(self):
        # Test shortest path to nonexistent room
        result = self.game.shortest_path("Nonexistent Room")
        self.assertEqual(result, "Room 'Nonexistent Room' does not exist.")

    def test_shortest_path_no_path(self):
        # Test shortest path where no path exists
        self.game.graph.remove_edge("Decontamination", "Terrarium")
        self.player.current_room = self.rooms["Rec Room"]
        result = self.game.shortest_path("Terrarium")
        self.assertEqual(result, "No path to Terrarium.")
        self.game.graph.add_edge("Decontamination", "Terrarium", weight=1)

    def test_db_save_load(self):
        # Set up game state
        self.player.current_room = self.rooms["Med Bay"]

        # Ensure rooms table in DB matches current rooms
        with sqlite3.connect("lostlab.db") as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM rooms")
            for room_name, room in self.rooms.items():
                cur.execute("INSERT INTO rooms (name, item) VALUES (?, ?)", (room_name, room.item))
            conn.commit()

        # Player picks up item (updates in-memory room)
        self.player.take_item("Medical Supplies")
        self.rooms["Lab"].item = "Recording"  # Make a change to another room

        # Save game state
        result = self.game.save_to_db()
        self.assertEqual(result, "Game saved to database.")

        # Simulate restarting game with same player
        player_id = self.player.id
        new_game = Game()
        new_game.player = Player(new_game.rooms["Rec Room"], player_id)

        # Load game state
        result = new_game.load_from_db()
        self.assertEqual(result, "Game loaded from database.")

        # Assert room item and player inventory state
        self.assertEqual(new_game.player.current_room.name, "Med Bay")
        self.assertEqual(new_game.player.inventory, {"Medical Supplies"})
        self.assertIsNone(new_game.rooms["Med Bay"].item)  # Med Bay item removed when picked up
        self.assertEqual(new_game.rooms["Lab"].item, "Recording")  # Lab item unchanged

    def test_db_log_action(self):
        # Test logging actions to database
        self.game.log_action("test", "Test action")
        with sqlite3.connect("lostlab.db") as conn:
            cur = conn.cursor()
            cur.execute("SELECT action, details FROM logs WHERE player_id = ?", (self.player.id,))
            result = cur.fetchone()
            self.assertIsNotNone(result)
            self.assertEqual(result[0], "test")
            self.assertEqual(result[1], "Test action")

    def test_db_no_player_data(self):
        # Test loading when no player data exists
        with sqlite3.connect("lostlab.db") as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM player WHERE id = ?", (self.player.id,))
            conn.commit()
        result = self.game.load_from_db()
        self.assertEqual(result, "Error: No saved data for this player.")

    def test_hazard_room_access(self):
        # Test accessing MEd Bay without required items
        self.player.current_room = self.rooms["Rec Room"]
        result = self.player.move("west")
        self.assertEqual(self.player.current_room.name, "Rec Room")
        self.assertEqual(result, "Cannot enter Med Bay: missing MKIV Suit, MKV Helmet.")
        # Add required items and retry
        self.player.inventory = {"MKIV Suit", "MKV Helmet"}
        result = self.player.move("west")
        self.assertEqual(self.player.current_room.name, "Med Bay")
        self.assertEqual(result, "You moved to Med Bay.")

    def test_weighted_shortest_path_hazard(self):
        # Test pathfinding avoids Med Bay without required items
        self.player.current_room = self.rooms["Cargo Hold"]
        self.player.inventory = set()
        result = self.game.shortest_path("Lab")
        # Without items, path avoids Med Bay (weight=100)
        self.assertEqual(result, "Shortest path to Lab: Cargo Hold -> Sleeping Quarters -> Rec Room -> "
                                 "Decontamination -> Lab")
        # With items, direct path through Med Bay is chosen
        self.player.inventory = {"MKIV Suit", "MKV Helmet"}
        result = self.game.shortest_path("Lab")
        self.assertEqual(result, "Shortest path to Lab: Cargo Hold -> Med Bay -> Lab")


if __name__ == '__main__':
    unittest.main()
