This is a Python script that handles subject-specific PMs to carry out a host of subreddit management and statistic operations*. The main uses for this script are for subreddits requiring a bot to manage flairs (usually those with 350+ flairs, the limit for flair templates in subreddits) or curious moderators who desire more detailed information about their subreddit.

* Based on /u/Gavin19's Reddit Flair Bot --> http://github.com/gavin19/reddit-flair-bot

System Requirements: Python (2.7 supported, Python 3 may work but have not been specifically tested) and PRAW (Python Reddit API Wrapper --> https://praw.readthedocs.io/en/latest/getting_started/installation.html)

Online Requirements: You must set up a Reddit Script App to authorize the bot to read PMs, mark them as read, and apply flairs to users. These can be created easily on an account's Preferences-->App page. The account in question must be invited as a Moderator with minimum Flair permissions to be able to serve a particular subreddit. All account and script details (client id, secret, username and password etc etc) must be entered into the conf.ini file.

Subreddit Setup: Create a post (wiki page, website, etc) that contains links, images, and a great deal of organization for users to find the flair they desire. Somewhere you will need to create a link to create a message with a preset PM pointed at your bot account, like so:
    [Select Flair](http://www.reddit.com/message/compose/?to=bot_account&subject=flair&message=flairclassnamehere%20%0DReplace%20this%20text%20with%20your%20desired%20flair%20text.)
    As mentioned before, the bot account must be invited as a Moderator with flair permissions in order to change the user's flair.

Configuration: The configuration file (conf.ini) has five sections.
[app]
The app_id and app_secret values will be found after you create your Reddit Script on the bot account's preference page (you can revisit this page to see these values if you forget or misplace them). The user_agent identifies the bot when it connects to Reddit, and should be adequately descriptive (ex: Flair Bot for /r/yoursub) and unique.

[credentials]
The username and password fields here should be populated with the account username and password. For this reason, do not share your conf.ini file with anyone who you do not want to have access to your account, as it will be in plaintext in this document. As always, it is strongly recommended to use strong passwords that are unique relative to all other passwords for all other accounts and services you utilize.

[update]
As an optimization, some data is cached in small .csv files in the same directory as your program, reducing the necessary API calls to run and improving responsiveness. The every_days field specifies a number of days to wait before refreshing this cache. E.g.: Setting this value to 1 will cause the bot to update its cache daily, 0 will cause the bot to update its cache every time it receives a request.

[subreddit]
The name field here will be set to the subreddit you wish for the bot to monitor. If the bot is to serve multiple subreddits, you can set this to your primary sub and modify the bot's source code as detailed later to have it serve the other subreddits.

[subject]
The subject that will magically activate the bot and rouse it to do its job upon receiving a PM with matching subject. Each function has its own subject field. Whatever you set this value to is what users will need to PM the bot with to receive that particular service.

Running: Simply execute python BotDriver.py from a terminal/command prompt for a one-time check, or schedule it to run periodically with a task scheduler such as cron.

Support: PM /u/VGFierte on Reddit
