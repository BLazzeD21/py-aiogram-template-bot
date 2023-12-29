from sqlite3 import Connection, Cursor
import sqlite3


class DatabaseMethods:
    def __init__(self) -> None:
        self.database: Connection = sqlite3.connect("models/users.db")
        self.cursor: Cursor = self.database.cursor()

    def create_tables(self) -> None:
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS profiles("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "user_id INTEGER, "
            "username TEXT, "
            "name TEXT, "
            "age INTEGER, "
            "gender TEXT, "
            "description TEXT, "
            "photo_id TEXT, "
            "photo_unique_id TEXT)"
        )
        self.database.commit()

    def insert_user(self, item_data: tuple, user_id: int, username: str) -> None:
        query: str = (
            "INSERT INTO profiles (user_id, username, name, age, gender, description, photo_unique_id, photo_id) "
            "VALUES (:user_id, :username, :name, :age, :gender, :description, :photo_unique_id, :photo_id)"
        )
        self.cursor.execute(
            query,
            {
                "user_id": user_id,
                "username": username,
                "name": item_data["name"],
                "age": item_data["age"],
                "gender": item_data["gender"],
                "description": item_data["description"],
                "photo_unique_id": item_data["photo_unique_id"],
                "photo_id": item_data["photo_id"],
            },
        )
        self.database.commit()

    def get_profile(self, user_id: int) -> tuple | bool:
        query: str = "SELECT * FROM profiles WHERE user_id = :user_id"
        self.cursor.execute(query, {"user_id": user_id})
        response: tuple = self.cursor.fetchone()
        if response:
            return response
        else:
            return False

    def update_user(self, user_id: int, username: str, item_data: tuple) -> None:
        query: str = (
            "UPDATE profiles SET username=:username, name=:name, age=:age, gender=:gender, "
            "description=:description, photo_id=:photo_id, photo_unique_id=:photo_unique_id WHERE user_id=:user_id"
        )
        self.cursor.execute(
            query,
            {
                "user_id": user_id,
                "username": username,
                "name": item_data["name"],
                "age": item_data["age"],
                "gender": item_data["gender"],
                "description": item_data["description"],
                "photo_id": item_data["photo_id"],
                "photo_unique_id": item_data["photo_unique_id"],
            },
        )
        self.database.commit()

    def get_profiles(self) -> list[tuple]:
        query: str = "SELECT * FROM profiles"
        self.cursor.execute(query)
        response: list[tuple] = self.cursor.fetchall()
        return response
