import sys,tweepy,re,os.path

#Populate your twitter API details below
cKey = ''
cSecret = ''
atKey = ''
atSecret = ''

auth = tweepy.OAuthHandler(cKey, cSecret)
auth.set_access_token(atKey,atSecret)

def chefalise(phrase):
	subs = ((r'a([nu])', r'u\1'),
		(r'A([nu])', r'U\1'),
		(r'a\B', r'e'),
		(r'A\B', r'E'),
		(r'en\b', r'ee'),
		(r'\Bew', r'oo'),
		(r'\Be\b', r'e-a'),
		(r'\be', r'i'),
		(r'\bE', r'I'),
		(r'\Bf', r'ff'),
		(r'\Bir', r'ur'),
		(r'(\w*?)i(\w*?)$', r'\1ee\2'),
		(r'\bow', r'oo'),
		(r'\bo', r'oo'),
		(r'\bO', r'Oo'),
		(r'the', r'zee'),
		(r'The', r'Zee'),
		(r'th\b', r't'),
		(r'\Btion', r'shun'),
		(r'\Bu', r'oo'),
		(r'\BU', r'Oo'),
		(r'v', r'f'),
		(r'V', r'F'),
		(r'w', r'w'),
		(r'W', r'W'),
		(r'([a-z])[.]', r'\1.  Bork Bork Bork!'))

	urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', phrase)

	# Twitter Handles
	twitterHandles = re.findall('\B@([^\W]+)', phrase)

	# Twitter Hashtags
	hashtags = re.findall(r"#(\w+)", phrase)

 	if not isinstance(urls, (list, tuple)):
		urls = [urls]
	
	if not isinstance(twitterHandles, (list, tuple)):
		twitterHandles = [twitterHandles]

	if not isinstance(hashtags, (list, tuple)):
		hashtags = [hashtags]

	x = 0;
	y = 0;
	thx = 0;
	thy = 0;
	htx = 0;
	hty = 0;

	for url in urls:
		phrase = phrase.replace(url,'#!??!'+str(x)+"#####");
		x=x+1

	for handle in twitterHandles:
		phrase = phrase.replace(handle,'##??!'+str(thx)+"#####");
		thx=thx+1

	for hashtag in hashtags:
		phrase = phrase.replace(hashtag,'##?#!'+str(htx)+"#####");
		htx=htx+1


	for fromPattern, toPattern in subs:
		phrase = re.sub(fromPattern, toPattern, phrase)
	
	while y < x:
		phrase = phrase.replace("#!??!"+str(y)+"#####",urls[y])
		y=y+1

	while thy < thx:
		phrase = phrase.replace("##??!"+str(thy)+"#####",twitterHandles[thy])
		thy=thy+1
	
	while hty < htx:
		phrase = phrase.replace("##?#!"+str(hty)+"#####",hashtags[hty])
		hty=hty+1

	return phrase



api = tweepy.API(auth)
id = 0

for status in api.user_timeline(screen_name = 'realDonaldTrump', count = 1, include_rts = False,tweet_mode='extended'):
	if os.path.isfile(".swedish") :
		id=open(".swedish").read(1)
	if id != str(status.id):
		if status.in_reply_to_status_id is None:
			api.update_status(chefalise(status._json['full_text']))
			#print chefalise(status._json['full_text'])
		else:
			api.update_status(chefalise(status._json['full_text']),status.in_reply_to_status_id)
			#print "REPLY: "+chefalise(status._json['full_text'])
	
		f = open(".swedish", 'w')
		f.write(str(status.id))
		f.close()