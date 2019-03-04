import sys
import random
import os
import requests
import json


class Bot(object):
    def __init__(self, config, domain="http://127.0.0.1:8000"):
        self.registration_url = domain + "/account/create/"
        self.auth_url = domain + "/account/token/"
        self.post_url = domain + "/post/"
        self.post_like_url = domain + "/post/like/"

        try:
            self.number_of_users = config.get("number_of_users", 1)
            self.max_posts_per_user = config.get("max_posts_per_user", 1)
            self.max_likes_per_user = config.get("max_likes_per_user", 1)
        except(AttributeError, ):
            raise Exception("Incorrect config file")

        self.user_objects = self._create_user_objects()

    def _create_user_objects(self):
        users = [{"email": f"test{x}@email.com",
                  "password": "qwerty12345"} for x in range(self.number_of_users)]
        return users

    def _get_post(self):
        data = requests.get("https://baconipsum.com/api/?type=all-meat&paras=1&start-with-lorem=1").json()[0]
        return {
            "title": " ".join(data.split(" ")[:4]),
            "text": data
        }

    def sign_up_users(self):
        for user in self.user_objects:
            res = requests.post(self.registration_url, json=user)
            print(f"Registration status_code: {res.status_code}")
            res = requests.post(self.auth_url, json=user)
            print(f"Authentication status_code: {res.status_code}")
            user["token"] = res.json()["access"] if res.status_code == 200 else False

    def send_posts(self):
        for user in self.user_objects:
            if not user["token"]:
                print(f"User {user['email']} not authenticated")
                continue
            else:
                for i in range(random.randint(0, self.max_posts_per_user)):
                    res = requests.post(self.post_url,
                                        json=self._get_post(),
                                        headers={"Authorization": f"Bearer {user['token']}"})
                    print(f"Post creation status_code: {res.status_code}")

    def set_likes(self):
        post_id_list = [x["id"] for x in requests.get(self.post_url).json()]
        for user in self.user_objects:
            if not user["token"]:
                print(f"User {user['email']} not authenticated")
                continue
            else:
                for i in range(random.randint(0, self.max_likes_per_user)):
                    res = requests.post(self.post_like_url,
                                        json={"post": random.choice(post_id_list)},
                                        headers={"Authorization": f"Bearer {user['token']}"})
                    print(f"Post like status_code: {res.status_code}")

    def run(self):
        self.sign_up_users()
        self.send_posts()
        self.set_likes()


if __name__ == "__main__":
    try:
        with open(sys.argv[1]) as json_file:
            json_str = json_file.read()
            config = json.loads(json_str)
            domain = sys.argv[2]
            bot = Bot(config, domain)
            bot.run()
    except(IndexError, ):
        raise Exception("Config file and domain must be defined")
