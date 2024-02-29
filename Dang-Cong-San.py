import requests
from bs4 import BeautifulSoup
import json

URL = 'https://dangcongsan.vn/tu-tuong-van-hoa/';
response = requests.get('https://dangcongsan.vn/tu-tuong-van-hoa/p/1')
html_content = response.content
soup = BeautifulSoup(html_content, 'html.parser')

def get_soup(url):
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup

def next_page(soup):
    div_next_url = soup.find('div',{'class': 'ex_page'})
    next_urls = div_next_url.find_all('a', {'class':'boxdv1'})
    for next_url in next_urls:
        if 'active' not in next_url.get('class',[]):
            new_url = (next_url['href'])
            return new_url
        else:
            None    

def extract(link_bai):
    try:
        response = requests.get(link_bai)
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')
        div_post_content = soup.find('div', class_='post-content')
        p_contents = div_post_content.find_all('p', {'style' : 'text-align: justify;'})
        content_list=[]
        for p_content in p_contents:
            content = p_content.text.strip()
            content_list.append(content)
        extracted_content = " ".join(content_list)
        return extracted_content
    except Exception as e:
        print(f"Error: {e}")
        return None

def article_extract(soup):
    articles =[]
    if soup == get_soup('https://dangcongsan.vn/tu-tuong-van-hoa/p/1') or soup == get_soup('https://dangcongsan.vn/tu-tuong-van-hoa'):
        All_as = soup.find_all('a', {'class':'item-title'})
        for All_a in All_as:
            s_article_title = All_a['title']
            s_article_url = All_a['href']
            s_article_content = extract(s_article_url)
            s_article_data = {
                'Title': s_article_title,
                'Content': s_article_content,
                'URL': s_article_url
            }
            articles.append(s_article_data)    
    All_divs = soup.body.find_all('div', class_='col-md-4 col-sm-12 col0 box-thumbnail')
    for All_div in All_divs:
        link = All_div.find_next('a')
        if link:
            article_title = link['title']
            article_url = link['href']
            article_content = extract(link['href'])
            article_data = {
                'Title': article_title,
                'Content': article_content,
                'URL': article_url
            }
            articles.append(article_data)
    return articles

def save_data(articles):
    json_file_path = 'DCSVN.json'
    try:
        with open(json_file_path, 'a', encoding='utf-8') as json_file:
            for article in articles:
                json.dump(article, json_file, ensure_ascii = False, indent = 2)
                json_file.write('\n') 
        print(f"Data successfully saved to {json_file_path}")
    except Exception as e:
        print(f"Error saving data to {json_file_path}: {e}")

save_data(article_extract(soup))
while True:
    next_page_url = URL + next_page(soup)
    if next_page_url:
        save_data(article_extract(get_soup(next_page_url)))
        soup = get_soup(next_page_url)
    else:
        break