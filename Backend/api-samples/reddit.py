from flask import Flask, request, redirect
import praw
import os
import json
import prawcore
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
USER_AGENT = os.getenv('REDDIT_USER_AGENT')
REDIRECT_URI = 'http://localhost:8888/callback'

app = Flask(__name__)

reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     redirect_uri=REDIRECT_URI,
                     user_agent=USER_AGENT)

@app.route('/')
def home():
    scope = ['mysubreddits', 'read']
    auth_url = reddit.auth.url(scopes=scope, state='...', duration='permanent')
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    try:
        reddit.auth.authorize(code)

        subscribed_subreddits = []
        for subreddit in reddit.user.subreddits(limit=None):
            subreddit_info = {
                'name': subreddit.display_name,
                'description': subreddit.public_description,
                'subscribers': subreddit.subscribers,
                'top_posts': [{'title': post.title, 'url': post.url} for post in subreddit.top(limit=10)]
            }
            subscribed_subreddits.append(subreddit_info)

        user_data = {
            'subscribed_subreddits': subscribed_subreddits
        }

        with open('reddit_user_data.json', 'w', encoding='utf-8') as f:
            json.dump(user_data, f, ensure_ascii=False, indent=4)

    except prawcore.exceptions.InsufficientScope as e:
        return f"Insufficient scope: {str(e)}"

    return 'Data has been saved to reddit_user_data.json'

if __name__ == '__main__':
    app.run(port=8888)
