from pymongo import MongoClient

if __name__ == "mongo_handler":
    def insert_many(coll_name, dict_list):
        db_client = MongoClient(host='localhost', port=27017)
        db = db_client.imdb_movies
        coll = db[coll_name]

        coll.insert_many(dict_list)

        db_client.close()

    def fetch_all(coll_name):
        db_client = MongoClient(host='localhost', port=27017)
        db = db_client.imdb_movies
        coll = db[coll_name]

        cursor = coll.find({}, {'_id': 0})

        document_list = []
        for cur in cursor:
            document_list.append(cur)

        db_client.close()

        return document_list
