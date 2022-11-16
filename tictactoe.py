import sqlite3

class tictactoe():

    def main(self, game, turn):
        for i in range(0, 9):
            if (game["cells"][i] != 0 and game["cells"][i] != 1 \
            and game["cells"][i] != -1):
                return {"error": 1}
        if game and turn >= 0 and turn < 9:
            if game["cells"][turn] != 0 and game["cells"][turn] != 1:
                game["cells"][turn] = game["turn"]
            else:
                return {"error": 1}
        else:
            return {"error": 1}
        return tictactoe.check_win(self, game["cells"])

    def check_win(self, cell):
        if (cell[0] == cell[1] == cell[2] != -1) \
        or (cell[3] == cell[4] == cell[5] != -1) \
        or (cell[6] == cell[7] == cell[8] != -1) \
        or (cell[0] == cell[3] == cell[6] != -1) \
        or (cell[1] == cell[4] == cell[7] != -1) \
        or (cell[2] == cell[5] == cell[8] != -1) \
        or (cell[0] == cell[4] == cell[8] != -1) \
        or (cell[2] == cell[4] == cell[6] != -1):
            return True
        return False

class db():

    def __init__(self, db):
        self.connection = sqlite3.connect(db)
        self.cursor = self.connection.cursor()

    def create_game(self):
        with self.connection:
            result = self.cursor.execute("INSERT INTO `games` DEFAULT VALUES")
            return result.lastrowid

    def update_status(self, game_id, status):
        if (status < 0 or status > 3):
            return False
        with self.connection:
            self.cursor.execute("UPDATE `games` SET status = ? WHERE id = ?", (status, game_id))
            return True

    def update_players(self, game_id, player_1_id, player_2_id):
        if (player_1_id < 1 or player_2_id < 1):
            return False
        with self.connection:
            self.cursor.execute("UPDATE `games` SET player_1_id = ?, player_2_id = ? WHERE id = ?", (player_1_id, player_2_id, game_id))
            return True

    def update_cells(self, game_id, cells_id, cells_value):
        if cells_value != 0 and cells_value != 1:
            return False
        if cells_id < 0 or cells_id > 8:
            return False
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `games` WHERE id = ?", (game_id,))
            result = result.fetchall()
            if len(result) != 1:
                return False
            cells = result[0][6]
            cells = [int(i) for i in cells.split(",")]
            cells[cells_id] = cells_value
            cells = ", ".join([str(i) for i in cells])
            self.cursor.execute("UPDATE `games` SET cells = ? WHERE id = ?", (cells, game_id))
            return True

    def update_turn(self, game_id, turn):
        if (turn != 0 and turn != 1):
            return False
        with self.connection:
            self.cursor.execute("UPDATE `games` SET turn = ? WHERE id = ?", (turn, game_id))
            return True

    def update_win(self, game_id, win):
        if (win != 0 and win != 1):
            return False
        with self.connection:
            self.cursor.execute("UPDATE `games` SET player_win = ? WHERE id = ?", (win, game_id))
            return True

    def get_game(self, game_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `games` WHERE id = ?", (game_id,))
            result = result.fetchall()
            if len(result) != 1:
                return False
            result = result[0]
            game_data = {}
            game_data["player_1_id"] = result[1]
            game_data["player_2_id"] = result[2]
            game_data["status"] = result[3]
            game_data["player_win"] = result[4]
            game_data["turn"] = result[5]
            game_data["cells"] = []
            [game_data["cells"].append(int(i)) for i in result[6].split(",")]
            return game_data
