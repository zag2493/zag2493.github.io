import timeit
from LostLabEnhanced import Player, Room, Game


def measure_inventory_performance():
    setup = '''
from LostLabEnhanced import Player, Room
player_list = Player(Room("Test"), 1)
player_set = Player(Room("Test"), 1)
player_list.inventory = ["Item" + str(i) for i in range(1000)]
player_set.inventory = {"Item" + str(i) for i in range(1000)}
'''
    list_time = timeit.timeit('"Item999" in player_list.inventory', setup=setup, number=10000)
    set_time = timeit.timeit('"Item999" in player_set.inventory', setup=setup, number=10000)
    print(f"List lookup time: {list_time:.6f} seconds")
    print(f"Set lookup time: {set_time:.6f} seconds")
    return list_time, set_time


def measure_shortest_path_performance():
    setup = '''
from LostLabEnhanced import Game
game = Game()
game.player.current_room = game.rooms["Rec Room"]
'''
    # Measure pathfinding without required items (Med Bay weight=100)
    no_items_time = timeit.timeit('game.shortest_path("Cargo Hold")', setup=setup, number=1000)
    print(f"Shortest path (no items, Cargo Hold, 1000 runs): {no_items_time:.6f} seconds")
    # Measure pathfinding with required items (Med Bay weight=1)
    with_items_setup = setup + '''
game.player.inventory = {"MKIV Suit", "MKV Helmet"}
'''
    with_items_time = timeit.timeit('game.shortest_path("Cargo Hold")', setup=with_items_setup, number=1000)
    print(f"Shortest path (with items, Cargo Hold, 1000 runs): {with_items_time:.6f} seconds")
    return no_items_time, with_items_time


def measure_hazard_check_performance():
    setup = '''
from LostLabEnhanced import Player, Room
room = Room("Med Bay", item="Medical Supplies", required_items={"MKIV Suit", "MKV Helmet"})
player = Player(room, 1)
'''
    # Measure hazard check without required items (sorting occurs)
    no_items_time = timeit.timeit('player.move("west")', setup=setup, number=1000)
    print(f"Hazard check (no items, 1000 runs): {no_items_time:.6f} seconds")
    # Measure hazard check with required items (no sorting needed)
    with_items_setup = setup + '''
player.inventory = {"MKIV Suit", "MKV Helmet"}
'''
    with_items_time = timeit.timeit('player.move("west")', setup=with_items_setup, number=1000)
    print(f"Hazard check (with items, 1000 runs): {with_items_time:.6f} seconds")
    return no_items_time, with_items_time


if __name__ == '__main__':
    print("Inventory Performance:")
    measure_inventory_performance()
    print("\nGraph Pathfinding Performance:")
    measure_shortest_path_performance()
    print("\nHazard Check Performance:")
    measure_hazard_check_performance()
