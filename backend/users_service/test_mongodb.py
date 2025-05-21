from pymongo import MongoClient

MONGODB_URI = "mongodb+srv://taskflow:R3Co0hNU414lomzP@cluster0.an2dj.mongodb.net/taskFlow?retryWrites=true&w=majority&appName=Cluster0"

def test_connection():
    client = MongoClient(MONGODB_URI)
    db = client["taskFlow"]
    users_collection = db["users"]

    user = users_collection.find_one()
    if user:
        print("Usuari trobat:", user)
    else:
        print("No s'han trobat usuaris a la col·lecció.")

if __name__ == "__main__":
    test_connection()
