from pymongo import MongoClient

if __name__ == "mongo_handler":
    def insert_many(coll_name, dict_list):
        with MongoClient(host='localhost', port=27017) as db_client:
            db = db_client.imdb_movies
            coll = db[coll_name]

            coll.insert_many(dict_list)

    def fetch_all(coll_name):
        document_list = []
        with MongoClient(host='localhost', port=27017) as db_client:
            db = db_client.imdb_movies
            coll = db[coll_name]
            cursor = coll.find({}, {'_id': 0})

            for cur in cursor:
                document_list.append(cur)

        return document_list
