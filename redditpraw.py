import praw
import re
import sys
import os
import csv
try:
	from configparser import ConfigParser
except ImportError:
	from ConfigParser import ConfigParser
'''
Grab necessary information to run as script from conf.ini file
Global scope/run first for setup/ease-of-access
'''
conf = ConfigParser()
if len(sys.argv) == 2:
	path = sys.argv[1]
else:
	path = sys.path[0]
os.chdir(path)
if os.path.exists('conf.ini'):
	conf.read('conf.ini')
else:
	raise IOError('Config file, conf.ini, was not found.')
a_id = conf.get('app', 'app_id')
a_scrt = conf.get('app', 'app_secret')
ua = conf.get('app', 'user_agent')
usr = conf.get('credentials', 'username')
psswd = conf.get('credentials', 'password')
subrddt = conf.get('subreddit', 'name')
update_interval = int(conf.get('update', 'every_days'))

# Initialize reddit and subreddit instances
reddit = praw.Reddit(client_id=a_id, client_secret=a_scrt,username=usr, password=psswd, user_agent=ua)
subreddit = reddit.subreddit(subrddt)

# Uses target subreddit and date str(date +"%j %y") to write a newline-delimited csv of moderator names
def updateModsCSV(date):
	with open('mods.csv', 'w') as modfile:
		modfile.write(date+'\n')
		modfile.write(subreddit.display_name+'\n')
		for moderator in subreddit.moderator():
			modfile.write(moderator.name+'\n')

# Boolean function that determines if str(user) is a moderator of the current subreddit
def mod_permissions(user):
	currentDate = os.popen("date +\"%j %y\"").read().strip('\n')
	# Check file for list of moderators, call update methods as needed
	try:
		modfile = open('mods.csv', 'r')
		lastDate = next(modfile)
		tracking = next(modfile).strip('\n')
		modfile.close()
		day_difference = int(currentDate[0:3]) - int(lastDate[0:3])
		day_difference += 365 * (int(currentDate[4:6]) - int(lastDate[4:6]))
		# Update cache when update interval expires
		if day_difference >= update_interval:
			updateModsCSV(currentDate)
		# Update cache when subreddit context does not match cached material
		elif tracking != str(subreddit.display_name):
			updateModsCSV(currentDate)
	except IOError:
		# Use update to create file and handle corruptions
		updateModsCSV(currentDate)

	# Get list of mods
	modlist = []
	with open('mods.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter='\n', quotechar='|')
		# Skip date and subreddit rows (meta-data only)
		next(reader)
		next(reader)
		for row in reader:
			# CSV reader adds [''] around names, so this gets rid of that
			modlist.append(str(row)[2:len(row)-3].lower())
	# Evaluates to True for mods, else False
	return user.lower() in modlist

# Uses target subreddit and date str(date +"%j %y") to write a newline-delimited csv of flair template names
def updateFlairCSV(date):
	with open('flairs.csv', 'w') as flairlist:
		flairlist.write(date+'\n')
		flairlist.write(subreddit.display_name+'\n')
		for template in subreddit.flair.templates:
			word = str(template)
			pos_start = int(word.find("-")+1)
			pos_end = word.find("',")
			flairtemplatename = word[pos_start:pos_end].lower()
			flairlist.write(flairtemplatename+'\n')

# Returns list [] of valid flair template names for current subreddit
def get_flairlist():
	currentDate = os.popen("date +\"%j %y\"").read().strip('\n')
	# Check file for list of flair templates, call update methods as needed
	try:
		flairs = open('flairs.csv', 'r')
		lastDate = next(flairs)
		tracking = next(flairs).strip('\n')
		flairs.close()
		day_difference = int(currentDate[0:3]) - int(lastDate[0:3])
		day_difference += 365 * (int(currentDate[4:6]) - int(lastDate[4:6]))
		# Update cache when update interval expires
		if day_difference >= update_interval:
			updateFlairCSV(currentDate)
		# Update cache when subreddit context does not match cached material
		elif tracking != str(subreddit.display_name):
			updateFlairCSV(currentDate)
	except IOError:
		# Use update to create file and handle corruptions
		updateFlairCSV(currentDate)

	# Create list of flairs to return
	flairlist = []
	with open('flairs.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter='\n', quotechar='|')
		# Skip date and subreddit rows (meta-data only)
		next(reader)
		next(reader)
		for row in reader:
			# CSV adds [''] around names, get rid of it
			flairlist.append(str(row)[2:len(row)-3].lower())
	return flairlist

# PM-handling function for 'getflairstats' command
# Currently configured as MODERATOR_ONLY
# Returns int(# Services Issued) (this is <= int(# PMs replied to))
def update_flair_curious_users_by_pm():
	valid = r'[A-Za-z0-9_-]+' # Defines a real username
	subject = conf.get('subject', 'getflairstats')	
	updatecount = 0
	# Searching PMs for target subject
	for msg in reddit.inbox.unread():
		author = str(msg.author)
		valid_user = re.match(valid, author)
		if msg.subject.lower() == subject and valid_user:
			# Prevent handling this message again!
			msg.mark_read()
			# This particular service rejects non-Moderators
			if mod_permissions(author):
				updatecount += 1
				replymessage = show_flair_diagnostics()	
			else:
				replymessage = "Your request was denied: You must be a moderator of r/"+subreddit.display_name+" to access this feature."
			msg.reply(replymessage)
	return updatecount

# Returns str(Full flair diagnostics)
def show_flair_diagnostics():
	returnstring = define_overall_flair_statistics()+'\n\n'
	returnstring += str(getusercount())+" users with flairs\n\n"
	returnstring += "Average flair-text length: "+str(flair_text_detail())
	return returnstring

# PM-handling function for 'getflair' command
# Returns int(# Services Issued) (this is <= int(# PMs replied to))
def update_flairs_by_pm():
	valid = r'[A-Za-z0-9_-]+' # Defines a real username
	subject = conf.get('subject', 'getflair')
	# Define available flairs on the subreddit (only assign flairs that exist)
	flairlist = get_flairlist()
	updatecount = 0
	# Searching PMs for target subject
	for msg in reddit.inbox.unread():
		author = str(msg.author)
		valid_user = re.match(valid, author)
		if msg.subject.lower() == subject and valid_user:
			# Prevent handling this message again!
			msg.mark_read()
			body = str(msg.body)
			pos_end = body.find(" ")
			# Recommend NOT using super long flair texts, enforce over 60 due to Reddit's limit
			if len(body) - pos_end > 60:
				replymessage = 'Your flair request was denied. The flair text contains too many characters. Retry with a shorter flair text (maximum length is 60 characters)'
			else:
				# First word is the flair class name, all else is flair text
				content = body.split(' ',1)
				class_name = content[0].rstrip().lower()
				# Check for valid flair
				if class_name not in flairlist:
					replymessage = 'Your flair request was denied because the requested flair class '+class_name+' does not exist on our subreddit. See the wiki page (r/'+subreddit.display_name+'/wiki/index/getflair) for available flairs'
				else:
					if len(content) > 1:
						flair_text = content[1].lstrip()[:64]
					else:
						flair_text = ''
					subreddit.flair.set(author, flair_text, class_name)
					updatecount += 1
					replymessage = 'Your flair change has been accepted. Your flair will now appear with the '+class_name+' image and the following flair text: '+flair_text
			msg.reply(replymessage)
	return updatecount

# str(target) = name of subreddit to select
# Changes target subreddit to specified name (accepts keyboard entry if none provided)
def set_target_subreddit(target=None):
	global subreddit
	if target == None:
		target = raw_input('Set target subreddit: ')
	subreddit = reddit.subreddit(target)

# Returns str(high-level statistics about flairs)
def define_overall_flair_statistics():
	returnstring = 'Flair Statistics for /r/'+subreddit.display_name
	returnstring += '\n\nTitle: '+subreddit.title
	returnstring += '\n\nAvailable Flairs for users of /r/'+subreddit.display_name+': '

	# Initialize Dictionary
	dictionary = {}
	flairtemplates = get_flairlist()
	for template in flairtemplates:
		# Add to dictionary, set occurrence count to 0
		dictionary[template]=0
		returnstring += template+', '

	# Get Usage Statistics
	returnstring += '\n\nUser Flair Statistics: '
	flairlist = subreddit.flair(limit=None)
	for flair in flairlist:
		# Strip flair name from JSON
		word = str(flair)
		pos_start = int(word.find(" u'") + 3)
		pos_end = word.find("',")
		userflairname = word[pos_start:pos_end]
		# Update Dictionary Count
		dictionary[userflairname.lower()] += 1
	# Write Statistics
	for key, value in sorted(dictionary.iteritems(), key=lambda (k,v): (v,k)):
		returnstring += key+': '+str(value)+', '
	return returnstring

# str(search) defines a flair class to learn more about (accepts keyboard input if none specified)
# Returns str(names using flair)
def flair_usage_detail(search=None):
	# More detail about a specific flair
	if not search:
		search = raw_input('\n\nLearn more about a flair? ')
		if not search:
			return
	# Parse JSON of users
	flairlist = subreddit.flair(limit=None)
	searchlist = []
	returnstring = ""
	for flair in flairlist:
		# Check flair name
		word = str(flair)
		pos_start = int(word.find(" u'") + 3)
       		pos_end = word.find("',")
       		userflairname = word[pos_start:pos_end]
		# Add associated username to list
		if userflairname.lower() == search.lower():
		       	pos_start = int(word.find("='") + 2)
		       	end = "')"
		       	pos_end = word.find(end)
		       	usersname = word[pos_start:pos_end]
			searchlist.append(usersname)
	if len(searchlist) > 0:
		returnstring += "Found users: "
		for key in searchlist:
			returnstring += key+", "
	else:
		returnstring += "No users found with that flair class"
	return returnstring+"\n"

# Returns float(average length of flair texts)
def flair_text_detail():
	flairlist = subreddit.flair(limit=None)
	total_length = 0
	total_count = 0
	for flair in flairlist:
		word = str(flair)
		pos_start = int(word.find("u'flair_text': u'")+17)
		pos_end = word.find("'}")
		flairtext = word[pos_start:pos_end]
		if len(flairtext):
			total_length += len(flairtext)
			total_count += 1
	return float(total_length)/total_count

# Returns float(average length of usernames of persons with flair)
def flair_users_detail():
	flairlist = subreddit.flair(limit=None)
	total_length = 0
	total_count = 0
	for flair in flairlist:
		word = str(flair)
		pos_start = int(word.find("name='")+6)
		pos_end = word.find("'), u'flair_text'")
		username = word[pos_start:pos_end]
		total_length += len(username)
		total_count += 1
	return float(total_length)/total_count

# str(name) specifies post name (partial titles accepted, accepts keyboard input if none)
# Returns str(shortlink URL specifier) (None if unable to locate)
def fetch_post(name=None):
	if not name:
		name = raw_input('Name the hot post (exactly, must be in top 100): ')
	posturl = ''
	name = name.lower()
	#Search target subreddit's hot 100 for post
	for submission in subreddit.hot(limit=100):
		if name == submission.title[0:len(name)].lower():
			start = int(str(submission.shortlink).find(".it/")+4)
			return submission.shortlink[start:len(submission.shortlink)]
	# Maybe re-search if name not found
	for submission in subreddit.hot(limit=100):
		if submission.title.find(name) != -1:
			start = int(str(submission.shortlink).find(".it/")+4)
			return submission.shortlink[start:len(submission.shortlink)]

# Returns int(number of users with flairs)
def getusercount():
	flairlist = subreddit.flair(limit=None)
	count = 0
	for flair in flairlist:
		word = str(flair)
        	pos_start = int(word.find(" u'") + 3)
		pos_end = word.find("',")
		userflairname = word[pos_start:pos_end]
		count += 1
	return count

# Helper-function, updates comment-tracking dictionary
def add_comment_count(dictionary, comment):
	end = len(str(comment.author))
	start = int(str(comment.author).find("'")+1)
	word = str(comment.author)[start:end]
	if word in dictionary:
		dictionary[word] += 1
	else:
		dictionary[word] = 1

# Recursive function that processes all comments on CommentForest object
def process_comments(dictionary, objects):
	for object in objects:
		if type(object).__name__ == "Comment":
			# Get replies to this comment
			process_comments(dictionary, object.replies)
			add_comment_count(dictionary, object)
		elif type(object).__name__ == "MoreComments":
			# Get more comments
			process_comments(dictionary, object.comments())

# str(post) is shortlink URL to target post for analysis
# Determine the number of comments Redditors have on a target post
def user_comments_on_post(post=None):
	if not post:
		post = fetch_post()
	submission = reddit.submission(post)
	commentdictionary = {}
	process_comments(commentdictionary, submission.comments)
	for key, value in sorted(commentdictionary.iteritems(), key=lambda (k,v): (v,k)):
		print 'User: ',key, 'has', value, 'comments on the post'

	print 'Dictionary found', len(commentdictionary), 'commenters'
	count = 0
	for item in commentdictionary.iteritems():
		count += item[1]
	print 'Dictionary found', count, 'total comments'

if __name__ == '__main__':
	print define_overall_flair_statistics(),"\n"
	print getusercount(), 'users using flairs'
	print "Average flair user's username length: ", flair_users_detail()
        print "Averate flair text length: ", flair_text_detail()
	print flair_usage_detail()
