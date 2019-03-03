Automated bot usage:

python3 bot.py "path_to_config_file.json" "domain"

Social Network

Basic models:
- User
- Post (always made by a user)

Basic features:
- user signup
- user login
- post creation
- post like
- post unlike

For User and Post objects, candidate is free to define attributes as they see fit.
Requirements:
- Token authentication (JWT is prefered)
- use Django with any other Django batteries, databases etc.

Optional:
- use clearbit.com/enrichment for getting additional data for the user on signup
- use emailhunter.co for verifying email existence on signup

Automated bot
Object of this bot demonstrate functionalities of the system according to defined rules.
This bot should read rules from a config file (in any format chosen by the candidate), but
should have following fields (all integers, candidate can rename as they see fit):
- number_of_users
- max_posts_per_user
- max_likes_per_user
Bot should read the configuration and create this activity:
- signup users (number provided in config)
- each user creates random number of posts with any content (up to
max_posts_per_user)
- After creating the signup and posting activity, posts should be liked randomly, posts
can be liked multiple times
