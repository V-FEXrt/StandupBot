import os
import time
from slackclient import SlackClient
from SlackUser import SlackUser

class UserState:
	Default, WaitingFirstResponse, NoReport, ReadyForQuestions, DailyComplete = range(5)

# starterbot's ID as an environment variable
BOT_ID = os.environ.get('BOT_ID')

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

def sendMessageToChannel(message, channel): # D1M78PHPH
    #return slack_client.api_call("chat.postMessage", channel=channel, text=message, as_user=True)
    print "Message: '" + message + "' sent to '" +  channel + "'"

def openDirectMessage(userID):
    resp = slack_client.api_call("im.open", user=userID)
    return resp['channel']['id']

def getSlackUsers():
    json = slack_client.api_call("users.list")

    map = {}

    for user in json['members']:
        name = user['name']
        id = user['id']

        if name == "ashley.coleman": # remove for release
            channel = openDirectMessage(id)
        else:
        	channel = ''

        state = UserState.Default
        map[id] = SlackUser(name, id, channel, state)

    return map

def askForUpdate(name, channel):
    sendMessageToChannel('Hey @' + name + '! It\'s a great time to start the day. Ready for stand up? (just say *no* if you don\'t want to report today)', channel)

def sendMessageToUser(user):
	if user.state == UserState.Default:
		askForUpdate(user.name, user.channel)
		user.state = UserState.WaitingFirstResponse
	elif user.state == UserState.NoReport:
		user.state = UserState.DailyComplete
		sendMessageToChannel('Okay no problem. I\'ll try again tomorrow!', user.channel)
	elif user.state == UserState.ReadyForQuestions:
		user.state = UserState.DailyComplete
		sendMessageToChannel('Question 1', user.channel)

def recieveMessageFromUser(user, message):
	if user.state == UserState.WaitingFirstResponse:
		if message == 'no':
			user.state = UserState.NoReport
			sendMessageToUser(user)
		elif message == 'yes':
			user.state = UserState.ReadyForQuestions
			sendMessageToUser(user)

def parseSlackMessage(slack_rtm_output, IDToUser):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and 'user' in output:
                recieveMessageFromUser(IDToUser[output['user']], output['text'])

    return

if __name__ == "__main__":
    if not slack_client.rtm_connect():
        print("Connection failed. Invalid Slack token or bot ID?")    
        exit()

    IDToUser = getSlackUsers()
    
    for id, user in IDToUser.iteritems():
    	if user.name == "ashley.coleman": # Remove for release
            sendMessageToUser(user)

    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    print("Bot connected and running!")
    while True:
        parseSlackMessage(slack_client.rtm_read(), IDToUser)
        time.sleep(READ_WEBSOCKET_DELAY)

        