import tictactoe

tictactoe_db = tictactoe.db("games.db")

game_tictactoe = tictactoe.tictactoe()

id = tictactoe_db.create_game()

while tictactoe_db.get_game(id)["status"] == 0:
    turn = int(input("Turn: "))
    result = tictactoe_db.get_game(id)
    game = {}
    game["turn"] = result["turn"]
    game["cells"] = result["cells"]
    result = game_tictactoe.main(game, turn)
    if result == {"error": 1}:
        print("error")
    if result:
        tictactoe_db.update_cells(id, turn, tictactoe_db.get_game(id)["turn"])
        result = tictactoe_db.update_status(id, 1)
    else:
        tictactoe_db.update_cells(id, turn, tictactoe_db.get_game(id)["turn"])
        if tictactoe_db.get_game(id)["turn"] == 0:
            tictactoe_db.update_turn(id, 1)
        else:
            tictactoe_db.update_turn(id, 0)

print("Win " + str(tictactoe_db.get_game(id)["turn"]))
