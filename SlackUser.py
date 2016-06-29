class SlackUser:
    """Class to represent SlackUser"""

    def __init__(self, name, id, channel, state):
        self.name = name
        self.id = id
        self.channel = channel
        self.state = state