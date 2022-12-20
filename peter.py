import random
import tweepy
import os
import requests
from PIL import Image

from settings import tweepy_config
from settings import logger



def get_priorities_at_random():
    priorities = [
        {
            "priority": "priority1",
            "text": "To secure Nigeria, end banditry and insurgency, and unite our dear nation, to manage our diversity such that no one is left behind.",
            "image": "https://pbs.twimg.com/media/FkctbLBWQAkL5jG?format=jpg&name=medium"
        },

        {
            "priority": "priority2",
            "text": "Shift emphasis from consumption to production by running a production-centered economy that is driven by an agrarian revolution and export-oriented industrialization.",
            "image": "https://pbs.twimg.com/media/FkctbK9XEAA7WVr?format=jpg&name=medium"
        },

        {
            "priority": "priority3",
            "text": "Restructure the polity through effective legal and institutional reforms to entrench the rule of law, aggressively fight corruption, reduce cost of governance, and establish an honest and efficient civil service.",
            "image": "https://pbs.twimg.com/media/FkctbK6XwAADDiu?format=jpg&name=medium"
        },

        {
            "priority": "priority4",
            "text": "Leapfrog Nigeria into the 4th Industrial Revolution (4IR), through the application of scientific and technological innovations to create a digital economy.",
            "image": "https://pbs.twimg.com/media/FkctgQUXoAEeVpy?format=jpg&name=medium"
        },

        {
            "priority": "priority5",
            "text": "Build expansive and world-class infrastructure for efficient power supply, rail, road and air transportation, and pipeline network, through integrated public-private partnerships, and entrepreneurial public sector governance.",
            "image": "https://pbs.twimg.com/media/FkctgQoXoAcnwlZ?format=jpg&name=medium"
        },

        {
            "priority": "priority6",
            "text": "Enhance the human capital of Nigerian youths for productivity and global competitiveness through investment in world-class scholarship and research, quality healthcare, and entrepreneurship education.",
            "image": "https://pbs.twimg.com/media/FkctgTAXEAEchTU?format=jpg&name=medium"
        },

        {
            "priority": "priority7",
            "text": "Conduct an afro-centric diplomacy that protects the rights of Nigerian citizens abroad and advances the economic interests of Nigerians and Nigerian businesses in a changing world.",
            "image": "https://pbs.twimg.com/media/FkctgTlXEAIIyMe?format=jpg&name=medium"
        }
    ]

    random_post = random.sample(priorities, 1)[0]

    return random_post


class PeterObi:
    def __init__(self):
        self.auth = tweepy.OAuthHandler(tweepy_config.get("CONSUMER_KEY"), tweepy_config.get("CONSUMER_SECRET"))
        self.auth.set_access_token(tweepy_config.get("ACCESS_TOKEN"), tweepy_config.get("ACCESS_TOKEN_SECRET"))
        self.tweepy_api = tweepy.API(self.auth, wait_on_rate_limit=True)

        self.prefix = "ObiDatti:"
        self.suffix = "\nIT’S POSSIBLE\nLP\n#automated_task"

    def get_random_priority(self):
        try:
            random_post = get_priorities_at_random()
            TWEET_STATUS = random_post.get("text")
            PRIORITY = random_post.get("priority")
            FILE_URL = random_post.get("image")
            FILE_PATH = f"/pictures/{PRIORITY}.jpg"
        except Exception as reason:
            logger.exception(f"Error getting random priority: {reason}")

        return FILE_URL, FILE_PATH, TWEET_STATUS, PRIORITY

    def download_image(self, FILE_URL, FILE_PATH):
        try:
            im = Image.open(requests.get(FILE_URL, stream=True).raw)
            im.save(os.getcwd() + FILE_PATH)
        except Exception as reason:
            logger.exception(f"Error downloading images: {reason}")

    def make_a_post(self, TWEET_STATUS, FILE_PATH):
        try:
            filename = os.getcwd() + FILE_PATH
            upload_result = self.tweepy_api.media_upload(filename)
            self.tweepy_api.update_status(
                status=TWEET_STATUS,
                media_ids=[upload_result.media_id_string],
                auto_populate_reply_metadata=True)
        except Exception as reason:
            logger.exception(f"Error send a post to twitter: {reason}")

    def make_post_with_multiple_images(self, filenames, TWEET_STATUS):
        try:
            media_ids = []
            for name in filenames:
                filename = os.getcwd() + f"/pictures/{name}"
                res = self.tweepy_api.media_upload(filename)
                media_ids.append(res.media_id)

            TWEET_STATUS = f"{self.prefix} '{TWEET_STATUS}'{self.suffix}"
            self.tweepy_api.update_status(
                status=TWEET_STATUS,
                media_ids=media_ids,
                auto_populate_reply_metadata=True)
        except Exception as reason:
            logger.exception(f"Error sending multiple post to twitter: {reason}")


if __name__ == "__main__":
    po = PeterObi()
    FILE_URL, FILE_PATH, TWEET_STATUS, PRIORITY = po.get_random_priority()
    po.download_image(FILE_URL, FILE_PATH)
    filenames = ["cover.jpg", f"{PRIORITY}.jpg"]
    po.make_post_with_multiple_images(filenames, TWEET_STATUS)
