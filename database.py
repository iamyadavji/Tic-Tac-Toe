import mysql.connector

class TicTacToeDB:
    def __init__(self):
        self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database=""
        )
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        try:
            create_table_query = """
                CREATE TABLE IF NOT EXISTS game_score (
                    player1 VARCHAR(255),
                    score1 INT,
                    player2 VARCHAR(255),
                    score2 INT
                )
            """
            self.cursor.execute(create_table_query)
            self.connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def save_score(self, player1, score1, player2, score2):
        try:
            insert_query = "INSERT INTO game_score (player1, score1, player2, score2) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(insert_query, (player1, score1, player2, score2))
            self.connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def close_connection(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()

if __name__ == "__main__":
    # Example of using TicTacToeDB class
    db = TicTacToeDB()
    db.save_score("Player1", 3, "Player2", 2)
    db.close_connection()
