from pymongo import MongoClient
import random


# help functions
def get_one_line(id_):
    dic = {}
    dic["id"] = id_
    return dic

def get_n_line(id_list):
    final = []
    for item in id_list:
        final.append(get_one_line(item))
    return final


class mongoAtlas(object):
    def __init__(self):
        self.client = MongoClient(
            "[your mongoDB Atlas url]")
        self.db = self.client.movie_id
        self.to_go = self.db.to_go
        self.done = self.db.done

# get all the ids to go
    def get_ids(self):
        return self.to_go.find().limit(100).skip(random.randint(100, 2000))

# once the id is finished, move it to the done collection
    def update_id(self, id_):
        self.done.insert_one(get_one_line(id_))
        self.to_go.remove(get_one_line(id_))