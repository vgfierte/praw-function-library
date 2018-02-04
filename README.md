This is a Python script that handles subject-specific PMs to carry out a host of subreddit management and statistic operations*. The main uses for this script are for subreddits requiring a bot to manage flairs (usually those with 350+ flairs, the limit for flair templates in subreddits) or curious moderators who desire more detailed inforamtion about their subreddit.

* Based on /u/Gavin19's Reddit Flair Bot --> http://github.com/gavin19/reddit-flair-bot

System Requirements: Python (2.7 supported, 3.3-3.6 may work but have not been specifically tested) and PRAW (Python Reddit API Wrapper --> https://praw.readthedocs.io/en/latest/getting_started/installation.html)

Online Requirements: You must set up a Reddit Script App to authorize the bot to read PMs, mark them as read, and apply flairs to users. These can be created easily on an account's Preferences-->App page. The account in question must be invited as a Moderator with minimum Flair permissions to be able to serve a particular subreddit. All account and scrip details (client id, secret, username and password etc etc) must be entered into the conf.ini file.

Subreddit Setup: Create a post (wiki page, website, etc) that contains links, images, and a great deal of organization for users to find the flair they desire. Somewhere you will need to create a link to create a message with a preset PM pointed at your bot account, like so:
    [Select Flair](http://www.reddit.com/message/compose/?to=bot_account&subject=flair&message=flairclassnamehere%20%0DReplace%20this%20text%20with%20your%20desired%20flair%20text.)
    As mentioned before, the bot account must be invited as a Moderator with flair permissions in order to change the user's flair.

Configuration: The configuration file (conf.ini) has five sections.
[app]
The app_id and app_secret values will be found after you create your Reddit Script on the bot account's preference page (you can revisit this page to see these values if you forget or misplace them). The user_agent identifies the bot when it connects to Reddit, and should be adequately descriptive (ex: Flair Bot for /r/yoursub) and unique.

[credentials]
The username and password fields here should be populated with the account username and password. For this reason, do not share your conf.ini file with anyone who you do not want to have access to your account, as it will be in plaintext in this document. As always, it is strongly recommended to use strong passwords that are unique relative to all other passwords for all other accounts and services you utilize.

[update]
As an optimization, some data is cached in small csv files in the same directory as your program, reducing the necessary API calls to run and improving responsiveness. The every_days field specifies a number of days to wait before refreshing this cache. E.g.: Setting this value to 1 will cause the bot to update its cache daily, 0 will cause the bot to update its cache every time it receives a request.

[subreddit]
The name field here will be set to the subreddit you wish for the bot to monitor. If the bot is to serve multiple subreddits, you can set this to your primary sub and modify the bot's source code as detailed later to have it serve the other subreddits.

[subject]
The subject that will magically activate the bot and rouse it to do its job upon receiving a PM with matching subject. Each function has its own subject field. Whatever you set this value to is what users will need to PM the bot with to receive that particular service.

Running: Simply execute python BotDriver.py from a terminal/command prompt for a one-time check, or schedule it to run periodically with a task scheduler such as cron.

Advanced: The file layout as presented allows for simple bot editing and a small variety of statistical functions. Calling different functions from BotDriver.py will change the behavior of the bot, or you may create your own driver function and utilize the developed functions by including "from Reddit import redditpraw" in your Python code. Below is a list of the available functions as well as a short description of their purpose.

mod_permissions(user) : Returns True or False depending on whether the specified username is a moderator or not of the currently targeted subreddit. Utilizes a cache called mods.csv for efficiency.

get_flairlist() : Returns a Python list object with all flair classes. Utilizes a cache called flairs.csv for efficiency.

update_flairs_by_pm(None) : Each call to this function pushes the bot to search for and handle flair requests (specified by conf.ini's [subject] 'getflair' field). Returns the number of updates handled.

update_flair_curious_users_by_pm() : Each call to this function pushes the bot to search for and handle flair statistic requests (specified by conf.ini's [subject] 'getflairstats' field). Returns the number of updates handled.

show_flair_diagnostics() : Calls the following functions and prints their returned values: define_overall_flair_statistics(), getusercount(), flair_text_detail()

define_overall_flair_statistics(None) : Returns a string that lists all available flairs for the subreddit and counts how many users are currently using each flair. Diagnostic information ordered by ascending user count.

flair_usage_detail(target) : Returns a string that lists all users who currently have the flair specified by the target classname. If no target is specified, prompts for keyboard input of a flair class.

flair_text_detail() : Returns a float describing the average character count of user's flair texts (does not count users without flair text)

getusercount() : Returns an integer describing the number of users who have a flair on the subreddit.

flair_users_detail() : Returns a float describing the average character count of the usernames of users with flair

set_target_subreddit(target) : Changes the target subreddit of the PRAW Reddit instance to the specified target. If no target is specified, prompts for keyboard input of a subreddit. NOTE: you must change the target to a moderated subreddit in order to use any flair-related functions. Functions that do not require moderator permissions will work as intended with any subreddit

fetch_post(target) : Returns the shortlink identifier for the target post name in the top 100 Hot Posts. If no target is specified, prompts for keyboard input of a post name with the same criteria as before.

user_comments_on_post(target) : Counts the number of comments each user has made on the specified post. If no target is specified, uses fetch_post() to acquire a target.

Support: PM /u/VGFierte on Reddit
