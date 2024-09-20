class Forum:
    def __init__(self, name, url):
        self.name = name
        self.url = url

class Topic:
    def __init__(self, forum, title, answers, views, username, url):
        self.forum = forum
        self.title = title
        self.answers = answers
        self.views = views
        self.username = username
        self.url = url

class Comment:
    def __init__(self, forum, topic, username, raw_content, clean_content):
        self.forum = forum
        self.topic = topic
        self.username = username
        self.raw_content = raw_content
        self.clean_content = clean_content
