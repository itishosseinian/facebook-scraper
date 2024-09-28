from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import json, re

urls = [
    "https://www.facebook.com/adidas/",
    "https://www.facebook.com/Cristiano",
    "https://www.facebook.com/nasaearth"
]

all_data = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()

    for url in urls:
        page = context.new_page()
        print(f"Going to page: {url}")
        page.goto(url)
        time.sleep(3)  

        soup = BeautifulSoup(page.content(), 'html.parser')

        cover_image = soup.find('img', {'data-imgperflogname': 'profileCoverPhoto'})['src'] 
        logo_image = soup.select_one('g image')['xlink:href'] 

        num_like_tag = soup.find('a', string=re.compile(r' likes$'))
        num_like = num_like_tag.get_text() if num_like_tag else "none"

        num_follower_tag = soup.find('a', string=re.compile(r' followers$'))
        num_follower = num_follower_tag.get_text() if num_follower_tag else "none"

        num_following_tag  = soup.find('a', string=re.compile(r' following$'))
        num_following = num_following_tag.get_text() if num_following_tag else "none"

        photo = soup.find_all('div', class_='x1yztbdb')[1]
        photos = [img['src'] for img in photo.select('img')]
        
        detail = soup.find('meta', {'name': 'description'})['content'] if soup.find('meta', {'name': 'description'}) else "none"

        data = {
            'url': url,
            'cover_image': cover_image,
            'logo_image': logo_image,
            'num_like': num_like,
            'num_follower': num_follower,
            'num_following': num_following,
            'detail': detail,
            'post_photos': photos
        }

        all_data.append(data)

        print(f"Finished scraping {url}")
        page.close()

    browser.close()

with open('out_all_urls.json', 'w', encoding='utf-8') as f:
    json.dump(all_data, f, ensure_ascii=False, indent=4)

print("Scraping completed for all URLs.")
