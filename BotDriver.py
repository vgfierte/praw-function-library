from Reddit import redditpraw
import time

if __name__ == '__main__':
	seconds_to_sleep = 2
	iterations = 0
	# Runs for 1 minute, change sleep interval, iteration count, or use cron to run the bot longer
	while(iterations < 15):
		# Check PMs for flair updates
		count = redditpraw.update_flairs_by_pm()
		iterations += 1
		if count != 0:
			print count, "flair updates handled."
		time.sleep(seconds_to_sleep)
		# Check PMs for flair statistic requests
		count = redditpraw.update_flair_curious_users_by_pm()
		if count != 0:
			print count, "statistic requests handled."
		time.sleep(seconds_to_sleep)
