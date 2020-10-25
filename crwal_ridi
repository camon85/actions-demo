import requests
from bs4 import BeautifulSoup
from github import Github
import os
from datetime import datetime
from pytz import timezone


def create_issue(repository_name, title, body):
    access_token = os.environ['GITHUB_ACCESS_TOKEN']
    g = Github(access_token)
    repo = g.get_user().get_repo(repository_name)
    repo.create_issue(title, body=body)


if __name__ == '__main__':
    url = 'https://ridibooks.com/category/new-releases/2200?order=recent'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    books = []
    for book_tag in soup.find_all(attrs={"data-book_id_for_tracking": True}):
        book_id = book_tag['data-book_id_for_tracking']
        book_detail_url = f'https://ridibooks.com/books/{book_id}'
        book_image_url = f'https://img.ridicdn.net/cover/{book_id}/large'
        books.append({'book_id': book_id, 'book_detail_url': book_detail_url, 'book_image_url': book_image_url})

    title_tags = soup.select('.title_text.js_highlight_helper')

    for index, title_tag in enumerate(title_tags):
        book_name = title_tag.get_text().strip()
        books[index]['book_name'] = book_name

    body_str_list = []
    for index, book in enumerate(books):
        book_name = book['book_name']
        book_detail_url = book['book_detail_url']
        book_image_url = book['book_image_url']
        first_line = f'{index + 1}. [{book_name}]({book_detail_url})'
        second_line = f'![{book_name}]({book_image_url})'
        body_str_list.append(first_line)
        body_str_list.append(second_line)

    now = datetime.now(timezone('Asia/Seoul'))
    format_now = now.strftime("%Y-%m-%d %H:%M")
    issue_title = f'리디북스 컴퓨터/IT 신간 - {format_now}'
    issue_body = '\n'.join(body_str_list)

    create_issue('actions-demo', issue_title, issue_body)
