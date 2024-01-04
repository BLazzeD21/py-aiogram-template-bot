import aiosqlite


class DatabaseMethods:
    def __init__(self) -> None:
        self.database: aiosqlite.Connection
        self.cursor: aiosqlite.Cursor

    async def connect(self):
        self.database = await aiosqlite.connect("models/users.db")
        self.cursor = await self.database.cursor()

    async def close(self):
        await self.cursor.close()
        await self.database.close()

    async def create_tables(self) -> None:
        await self.cursor.execute(
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
        await self.database.commit()

    async def insert_user(self, item_data: tuple, user_id: int, username: str) -> None:
        query: str = (
            "INSERT INTO profiles (user_id, username, name, age, gender, description, photo_unique_id, photo_id) "
            "VALUES (:user_id, :username, :name, :age, :gender, :description, :photo_unique_id, :photo_id)"
        )
        await self.cursor.execute(
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
        await self.database.commit()

    async def get_profile(self, user_id: int) -> tuple | bool:
        query: str = "SELECT * FROM profiles WHERE user_id = :user_id"
        await self.cursor.execute(query, {"user_id": user_id})
        response: tuple = await self.cursor.fetchone()
        if response:
            return response
        else:
            return False

    async def update_user(self, user_id: int, username: str, item_data: tuple) -> None:
        query: str = (
            "UPDATE profiles SET username=:username, name=:name, age=:age, gender=:gender, "
            "description=:description, photo_id=:photo_id, photo_unique_id=:photo_unique_id WHERE user_id=:user_id"
        )
        await self.cursor.execute(
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
        await self.database.commit()

    async def get_profiles(self) -> list[tuple]:
        query: str = "SELECT * FROM profiles"
        await self.cursor.execute(query)
        response: list[tuple] = await self.cursor.fetchall()
        return response

    async def delete_profile(self, user_id: int) -> None:
        query: str = "DELETE FROM profiles WHERE user_id=:user_id"
        await self.cursor.execute(query, {"user_id": user_id})
        await self.database.commit()
