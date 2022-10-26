# Use this programme to scrape details from hackernews.com to find only posts that have over 100 points
# This will leverage beautiful soup to scrape the website.

import requests  # Allows us to get files from website
from bs4 import BeautifulSoup  # Allows us to parse data from files
import re


def create_custom_hn(links, scores):
    new_links = [
        {'id': count,
         'title': link.get_text(),
         'link': link.find('a').get('href'),
         'points': int(scores[count])}
        for count, link in enumerate(links)
        if int(scores[count]) >= 100]

    return sorted(new_links, key=lambda x: x['points'], reverse=True)


def get_points(lines):
    scores = [(re.search(r"(\d+) points", str(line)).group(1)
               if re.search(r"(\d+) points", str(line))
               else '0') for line in lines]

    # for line in subtext:
    #     check = re.search(r"(\d+) points", str(line))
    #     if check:
    #         scores.append(check.group(1))
    #     else:
    #         scores.append(0)

    return scores


def output_news(link_list):
    for link in link_list:
        print(f"{link['title']}: {link['link']}")


def query_website(num_pages):
    res = ''
    for i in range(1, num_pages):
        res += requests.get(f'https://news.ycombinator.com/news?p={i}').text

    return res


if __name__ == '__main__':
    res = query_website(4)
    ref_doc = BeautifulSoup(res, 'html.parser')

    links = ref_doc.select('.titleline')
    subtext = ref_doc.select('.subtext')
    scores = get_points(subtext)

    link_list = create_custom_hn(links, scores)
    output_news(link_list)
