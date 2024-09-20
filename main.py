from requests import get
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string

from models import Forum, Topic, Comment

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')


def fetch_forums():
    response = get('https://www.clubedohardware.com.br/forums/')

    soup = BeautifulSoup(response.text, 'html.parser')

    hardware = soup.select('#ipsLayout_mainArea > section > ol > li:nth-child(2) > ol')[0]

    titles = [h4.find('a') for h4 in hardware.find_all('h4')]

    forums = [Forum(title.text, title.get('href')) for title in titles]

    return forums


def fetch_topics(forum: Forum, pages = 1):
    all_topics = []

    for page in range(1, pages + 1):
        response = get(f'{forum.url}page/{page}')

        soup = BeautifulSoup(response.text, 'html.parser')

        topics = soup.find_all('li', class_='ipsDataItem ipsDataItem_responsivePhoto')

        titles = [topic.find('span', class_='ipsType_break ipsContained').find('a') for topic in topics]

        usernames = [
            topic.find('div', class_='ipsDataItem_meta ipsType_reset ipsType_light ipsType_blendLinks').find('a')
            for topic in topics
        ]

        answers = [topic.find('li', attrs={'data-stattype': 'forums_comments'}).find('span') for topic in topics]

        views = [topic.find('li', attrs={'data-stattype': 'num_views'}).find('span') for topic in topics]

        for title, username, answers, views in zip(titles, usernames, answers, views):
            all_topics.append(Topic(
                forum,
                title.text.strip(),
                answers.text,
                views.text,
                username.text,
                title.get('href')
            ))

    return all_topics

def clean_content(content):
    tokens = word_tokenize(content)

    tokens = [word.lower() for word in tokens]

    tokens = [word for word in tokens if word not in string.punctuation]

    stop_words = set(stopwords.words('portuguese'))

    tokens = [word for word in tokens if word not in stop_words]

    return ' '.join(tokens)

def fetch_comments(topic: Topic):
    response = get(topic.url)

    soup = BeautifulSoup(response.text, 'html.parser')

    articles = soup.find_all('article')

    usernames = [
        article.find(
            'h3',
            class_='ipsType_sectionHead cAuthorPane_author ipsType_blendLinks ipsType_break'
        ).find('a') for article in articles
    ]

    paragraphs = [article.find_all('p') for article in articles]

    all_comments = []

    for username, paragraph in zip(usernames, paragraphs):
        content = []

        for p in paragraph:
            content.append(p.text)

        all_comments.append(Comment(
            topic.forum,
            topic,
            username.text,
            content,
            clean_content('\n'.join(content)),
        ))

    return all_comments


def main():
    for topic in fetch_topics(fetch_forums()[0]):
        for comment in fetch_comments(topic):
            print(comment.forum.name)
            print(comment.topic.title)
            print(comment.topic.answers)
            print(comment.topic.views)
            print(comment.topic.username)
            print(comment.topic.url)
            print(comment.username)
            print(comment.raw_content)
            print(comment.clean_content)
            print()


if __name__ == '__main__':
    main()
