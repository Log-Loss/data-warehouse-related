from Crawler.getWebPage import get_web_content
import json
import logging
import requests
import os

from DB.atlas import *

def get_next_id(ids):
    for i in ids:
        yield i['id']

if __name__ == '__main__':

    s = requests.session()
    s.keep_alive = False

    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(name)s:%(levelname)s: %(message)s"
    )

    atlas = mongoAtlas()
    movie_ids = atlas.get_ids()

    while movie_ids != None:

        for movie_id in get_next_id(movie_ids):
            url = 'https://www.amazon.com/dp/' + movie_id
            content_dict = get_web_content(url)
            if content_dict != None:
                with open('./pagedata/{}.json'.format(movie_id), 'w') as f:
                    content_json = json.dump(content_dict, f)

                logging.info(movie_id + ' finished ! size:' + str(os.path.getsize('./pagedata/{}.json'.format(movie_id))))

                atlas.update_id(movie_id)
                logging.info('update mongo Atlas !')

        movie_ids = atlas.get_ids()