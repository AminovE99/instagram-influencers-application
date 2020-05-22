import numpy as np
import time
import requests

from instagram_influencers_application.celery_controller import app
from webscrape_app.webscrape_util.scrape_util import add_new_line, load_last_line, setup_mongo_client


def insert_edge(response, collection):
    """Insert records into Mongo database.

    Args:
        response (request response object): Response from request.get('url')
        collection (pymongo.Collection): Collection object for record insertion.
    """
    edges = response.json()['data']['hashtag']['edge_hashtag_to_media']['edges']
    for edge in edges:
        collection.insert_one(edge)

def get_page_info(response):
    """Find and save page_info from response json.

    Args:
        response (request response object): Response from request.get('url')

    Returns:
        page_info (dict): Dictionary from response json.
            Keys: 'has_next_page' (bool) and 'end_cursor' (unicode)
    """
    page_info = response.json()['data']['hashtag']['edge_hashtag_to_media']['page_info']
    return page_info


@app.task
def instascrape(page_info_filepath, num_requests, collection_name):
    """
    Scrape instagram hashtag search

    Args:
        page_info_filepath (str): Filepath to text file with page_info dicts
        num_requests (int): Number of pages to be scraped

    Action: saves influencer node information to pymongo database

    Output: None
    """

    client, collection = setup_mongo_client('instascrape2', collection_name)
    page_info = ""
    response = requests.get("https://www.instagram.com/graphql/query/?query_id=17875800862117404&variables={{%22tag_name%22:%22tennis%22,%22first%22:{}}}"
                            .format('12'))

    if response.status_code == 200:
        print(response)
        insert_edge(response, collection)
        page_info = get_page_info(response)
        add_new_line(page_info, page_info_filepath)

    page_info = load_last_line(page_info_filepath)
    base_url_search = "https://www.instagram.com/graphql/query/?query_id=17875800862117404&variables={{%22tag_name%22:%22tennis%22,%22first%22:{},%22after%22:%22{}%22}}"

    for i in range(num_requests):
        print(page_info['end_cursor'])

        if page_info['has_next_page']:
            response = requests.get(base_url_search.format('11', str(page_info['end_cursor'])))

            if response.status_code == 200:
                insert_edge(response, collection)
                page_info = get_page_info(response)
                add_new_line(page_info, page_info_filepath)

            else:
                print("Status Code = " + str(response.status_code))
                return None

        time.sleep(np.random.uniform(15, 45))
        print("Finished scraping {} pages of {}".format(i + 1, num_requests))

    client.close()

    print("\n Finished scraping {} pages of 12 influencers each".format(num_requests))
    return None
#
# ex = "https://www.instagram.com/graphql/query/?query_id=17875800862117404&variables={{%22tag_name%22:%22womenwhoclimb%22,%22first%22:{},%22after%22:%22{}%22}}".format('12', " ")
# print(ex)
# response = requests.get(ex)
# print(response.url)

# instascrape("../date/influenc_d.json", 10)