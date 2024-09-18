from requests import get
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')


def fetch_forums():
    response = get('https://www.clubedohardware.com.br/forums/')

    soup = BeautifulSoup(response.text, 'html.parser')

    hardware = soup.select('#ipsLayout_mainArea > section > ol > li:nth-child(2) > ol')[0]

    forums = [h4.find('a') for h4 in hardware.find_all('h4')]

    links = [forum.get('href') for forum in forums]

    return links


def fetch_topics(forum: str, pages: int = 1):
    all_topics = []

    for page in range(1, pages + 1):
        response = get(f'{forum}page/{page}')

        soup = BeautifulSoup(response.text, 'html.parser')

        topics = soup.find_all('li', class_='ipsDataItem ipsDataItem_responsivePhoto')

        titles = [topic.find('h4', class_='ipsDataItem_title ipsContained_container') for topic in topics]

        links = [title.find('a').get('href') for title in titles]

        for link in links:
            all_topics.append(link)

    return all_topics


def fetch_comments(topic: str):
    response = get(topic)

    soup = BeautifulSoup(response.text, 'html.parser')

    articles = soup.find_all('article')

    paragraphs = [article.find_all('p') for article in articles]

    content = []

    for paragraph in paragraphs:
        for p in paragraph:
            content.append(p.text)

    return '\n'.join(content)


def clean_comment(comment):
    tokens = word_tokenize(comment)

    tokens = [word.lower() for word in tokens]

    tokens = [word for word in tokens if word not in string.punctuation]

    stop_words = set(stopwords.words('portuguese'))

    tokens = [word for word in tokens if word not in stop_words]

    return ' '.join(tokens)


def main():
    comments = []

    for forum in fetch_forums():
        for topic in fetch_topics(forum):
            comments.append(clean_comment(fetch_comments(topic)))

    comments = ' '.join(comments)

    print(comments)
    print(len(comments))


if __name__ == '__main__':
    main()
