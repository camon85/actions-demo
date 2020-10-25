import requests
from bs4 import BeautifulSoup
import re
from github import Github
import os
from datetime import datetime
from pytz import timezone


def get_html(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')


def parse(html):
    tags = html.select('.goodsImgW')
    book_list = []
    for i, v in enumerate(tags):
        name = v.select('img')[0].attrs['alt']
        img_src = v.select('img')[0].attrs['src']
        book_list.append({'book_name': name, 'book_img_src': img_src})
    return book_list


def create_issue(repository_name, title, body):
    access_token = os.environ['GITHUB_ACCESS_TOKEN']
    g = Github(access_token)
    repo = g.get_user().get_repo(repository_name)
    repo.create_issue(title, body=body)


if __name__ == '__main__':
    books = parse(get_html('http://www.yes24.com/24/Category/NewProductList/001001003?sumGb=01'))

    body_str_list = []
    for index, book in enumerate(books):
        regex = re.compile(r'https?://image.yes24.com/goods/(\d+)')
        match = regex.search(book['book_img_src'])
        img_url = match.group()
        goods_no = match.group(1)
        detail_url = f'http://www.yes24.com/Product/Goods/{goods_no}'
        large_image_url = f'{img_url}/L'
        book_name = book['book_name']
        first_line = f'{index + 1}. [{book_name}]({detail_url})'
        second_line = f'![{book_name}]({large_image_url})'
        body_str_list.append(first_line)
        body_str_list.append(second_line)

    now = datetime.now(timezone('Asia/Seoul'))
    format_now = now.strftime("%Y-%m-%d %H:%M")
    issue_title = f'YES24 IT 모바일 신간 - {format_now}'
    issue_body = '\n'.join(body_str_list)

    create_issue('actions-demo', issue_title, issue_body)
