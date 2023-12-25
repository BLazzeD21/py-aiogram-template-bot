import sqlite3

class DatabaseMethods:
  def __init__(self):
        self.database = sqlite3.connect('models/users.db')
        self.cursor = self.database.cursor()

  def create_tables(self):
    self.cursor.execute("CREATE TABLE IF NOT EXISTS profiles("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "user_id TEXT, "
                "username TEXT, "
                "name TEXT, "
                "age INTEGER, "
                "gender TEXT, "
                "description TEXT, "
                "photo_id TEXT, "
                "photo_unique_id TEXT) ")
    self.database.commit()
  
  def insert_user(self, item_data, user_id, username):
    query = "INSERT INTO profiles (user_id, username, name, age, gender, description, photo_unique_id, photo_id) " \
            "VALUES (:user_id, :username, :name, :age, :gender, :description, :photo_unique_id, :photo_id)"
    self.cursor.execute(query, {
        'user_id': user_id,
        'username': username,
        'name': item_data['name'],
        'age': item_data['age'],
        'gender': item_data['gender'],
        'description': item_data['description'],
        'photo_unique_id': item_data['photo_unique_id'],
        'photo_id': item_data['photo_id']
    })
    self.database.commit()

  def get_profile(self, user_id):
    query = "SELECT * FROM profiles WHERE user_id = :user_id"
    self.cursor.execute(query, {'user_id': user_id})
    response = self.cursor.fetchone()
    if response:
        return response
    else:
        return False
    
  def update_user(self, user_id, username, item_data):
    query = "UPDATE profiles SET username=:username, name=:name, age=:age, gender=:gender, " \
            "description=:description, photo_id=:photo_id, photo_unique_id=:photo_unique_id WHERE user_id=:user_id"
    self.cursor.execute(query, {
        'user_id': user_id,       
        'username': username,
        'name': item_data['name'],
        'age': item_data['age'],
        'gender': item_data['gender'],
        'description': item_data['description'],
        'photo_id': item_data['photo_id'],
        'photo_unique_id': item_data['photo_unique_id'],
    })
    self.database.commit()

  # def get_all_products(self):
  #   query = "SELECT * FROM products"
  #   self.cursor.execute(query)
  #   response = self.cursor.fetchall()
  #   return response
  
  # def show_product(self, name: str):
  #   query = "SELECT * FROM products WHERE name = :name"
  #   self.cursor.execute(query, {'name': name})
  #   response = self.cursor.fetchone()
  #   return response
