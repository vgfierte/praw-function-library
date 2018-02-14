The library contained in redditpraw.py contains simple functions which allow for simple bot creation, editing and a small variety of statistical functions. Calling different functions from `BotDriver.py` will change the behavior of the bot, or you may create your own driver and utilize the developed functions by importing `redditpraw.py` to your driver. Below is a list of the available functions as well as a short description of their purpose.

`[boolean] mod_permissions([str]user)` : Returns boolean value answering the question "Is `user` a moderator of the currently targeted subreddit?" Utilizes a cache called `mods.csv` for efficiency purposes.

`[list] get_flairlist(None)` : Returns a Python list object with all flair classes. Utilizes a cache called `flairs.csv` for efficiency.

`[None] update_flairs_by_pm(None)` : Each call to this function pushes the bot to search for and handle flair requests (specified by `conf.ini`'s `[subject] getflair` field). Returns the number of updates granted (does not count denied requests).

`[None] update_flair_curious_users_by_pm(None)` : Each call to this function pushes the bot to search for and handle flair statistic requests (specified by `conf.ini`'s `[subject] getflairstats` field). Returns the number of updates granted (does not count denied requests).

`[str] show_flair_diagnostics(None)` : Calls the following functions and concatenates/forwards their returned values: `define_overall_flair_statistics()`, `getusercount()`, `flair_text_detail()`

`[str] define_overall_flair_statistics(None)` : Returns a string that lists all available flairs for the subreddit and counts how many users are currently using each flair. Diagnostic information ordered by ascending user count.

`[str] flair_usage_detail([str]target)` : Returns a string that lists all users who currently have the flair specified by the `target` classname. If no `target` is specified, prompts for keyboard input of a flair class.

`[float] flair_text_detail(None)` : Returns a float describing the average character count of users' flair texts (does not count users without flair text).

`[int] getusercount(None)` : Returns an integer describing the number of users who have a flair on the subreddit.

`[float] flair_users_detail(None)` : Returns a float describing the average character count of the usernames of users with flair

`[None] set_target_subreddit([str]target)` : Changes the target subreddit of the PRAW Reddit instance to the specified `target`. If no `target` is specified, prompts for keyboard input of a subreddit. You MUST change the target to a moderated subreddit in order to use any flair-related functions. Functions that do not require moderator permissions will work as intended with any subreddit.

`[str] fetch_post([str]target)` : Returns the shortlink identifier for the target post name in the top 100 Hot Posts. If no target is specified, prompts for keyboard input of a post name with the same criteria as before.

`[None] user_comments_on_post(target)` : Counts and displays the number of comments each user has made on the specified post. If no `target` is specified, uses `fetch_post()` to acquire a target.
