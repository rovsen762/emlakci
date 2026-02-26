# import time
# from playwright.sync_api import sync_playwright


# def extract_item_details():
#     url = "https://bina.az/kiraye"

#     start_time = time.perf_counter()   # 🔥 başlanğıc vaxt

#     with sync_playwright() as p:
#         browser = p.chromium.launch(
#             headless=True,
#             slow_mo=100
#         )

#         page = browser.new_page()
#         page.goto(url, timeout=60000)

#         page.wait_for_selector("#search-page-regular-items")

#         links_locator = page.locator(
#             "#search-page-regular-items div[data-cy='item-card'] a[data-cy='item-card-link']"
#         )

#         links = []

#         for i in range(links_locator.count()):
#             href = links_locator.nth(i).get_attribute("href")
#             if href:
#                 links.append(f"https://bina.az{href}")

#         if links:
#             first_link = links[0]
#             print(f"İlk link açılır: {first_link}")
#             page.goto(first_link, timeout=60000)

#             title = page.text_content("h1.product-title")
#             if title:
#                 print("Başlıq:", title.strip())

#             properties = {}
#             items = page.locator("div.product-properties__column div.product-properties__i")

#             for i in range(items.count()):
#                 key = items.nth(i).locator("label.product-properties__i-name").text_content()
#                 value = items.nth(i).locator("span.product-properties__i-value").text_content()
#                 if key and value:
#                     properties[key.strip()] = value.strip()

#             print("\nProduct Properties:")
#             for k, v in properties.items():
#                 print(f"{k}: {v}")

#             location_locator = page.locator("div.product-shop__location a")

#             if location_locator.count() > 0:
#                 location = location_locator.first.text_content()
#                 location = location.strip() if location else None
#             else:
#                 location = None

#             print("\nLocation:", location)

#         browser.close()

#     end_time = time.perf_counter()  # 🔥 bitmə vaxtı
#     total_time = end_time - start_time

#     print(f"\nScript icra müddəti: {total_time:.2f} saniyə")


# if __name__ == "__main__":
#     extract_item_details()




#GRAPHQL API ilə məlumat çəkmək üçün nümunə kod

# import requests
# import json
# import time

# BASE_URL = "https://bina.az/graphql"

# HEADERS = {
#     "Content-Type": "application/json",
#     "User-Agent": "Mozilla/5.0",
#     "Accept": "application/json",
#     "X-Requested-With": "XMLHttpRequest",
#     "Referer": "https://bina.az/"
# }


# def fetch_item_name(path):
#     payload = {
#         "operationName": "ItemDetails",
#         "variables": {"path": path}
#     }

#     response = requests.post(BASE_URL, headers=HEADERS, json=payload)

#     if response.status_code != 200:
#         return None

#     try:
#         data = response.json()
#         return data.get("data", {}).get("item", {}).get("name")
#     except:
#         return None


# def fetch_bina_items(limit=24, offset=0):

#     payload = {
#         "operationName": "FeaturedItemsRow",
#         "variables": {"limit": limit, "offset": offset},
#         "extensions": {
#             "persistedQuery": {
#                 "version": 1,
#                 "sha256Hash": "4cd50103dbbf5b4c64339526de55e490b3cfa3d56cad20149efa11934369a477"
#             }
#         }
#     }

#     response = requests.post(BASE_URL, headers=HEADERS, json=payload)

#     if response.status_code != 200:
#         print("Request error:", response.status_code)
#         return []

#     data = response.json()
#     items = data.get("data", {}).get("items", [])

#     result = []

#     for item in items:

#         path = item.get("path")

#         # Əgər name boşdursa ayrıca query atırıq
#         name = fetch_item_name(path)

#         item_data = {
#             "id": item.get("id"),
#             "name": name,
#             "link": f"https://bina.az{path}",
#             "price": item.get("price", {}).get("total"),
#             "currency": item.get("price", {}).get("currency"),
#             "rooms": item.get("rooms"),
#             "area": item.get("area", {}).get("value"),
#             "area_units": item.get("area", {}).get("units"),
#             "city": item.get("city", {}).get("name"),
#             "location": item.get("location", {}).get("fullName"),
#             "company": item.get("company", {}).get("name"),
#             "photos_count": item.get("photosCount"),
#             "photos": [photo.get("f460x345") for photo in item.get("photos", [])]
#         }

#         result.append(item_data)

#         time.sleep(0.3)  # server block etməsin deyə

#     return result


# if __name__ == "__main__":
#     items = fetch_bina_items(limit=24, offset=0)

#     print(f"Toplam item: {len(items)}\n")

#     for i, item in enumerate(items, 1):
#         print(f"Item {i}:")
#         print(json.dumps(item, indent=2, ensure_ascii=False))
#         print("-" * 50)



# from bs4 import BeautifulSoup
# import requests


# url = "https://bina.az/items/5881944"
# def get_data(url):
    
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
#     }   
#     response = requests.get(url, headers=headers)
#     soup = BeautifulSoup(response.text, 'html.parser')

#     div_title = soup.find('div', class_='panel clearfix')
#     if div_title:
#         title = div_title.find('h1', class_='title')
#         print("Title:", title.text.strip() if title else "Yoxdur")


#     meta_name_description = soup.find('meta', attrs={'name': 'description'})
#     print("Meta Name Description:", meta_name_description['content'] if meta_name_description else "Yoxdur")
    
    # print(soup.prettify())
    
# url = "https://emlak.az/elanlar/?ann_type=1&tip[]=1"
    
# base_url = "https://emlak.az"
# def get_all_links(url):
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, 'html.parser')

#     links = []
    
    
    
#     ticked_list_class = soup.find('div', class_='ticket-list')
#     if ticked_list_class:
#         inner_divs = ticked_list_class.find_all('div', class_='ticket clearfix pinned')
#         if inner_divs:
#             for inner_div in inner_divs:
#                 h6_class = inner_div.find('h6', class_='title')
#                 if h6_class:
#                     a_tag = h6_class.find('a')
#                     if a_tag and 'href' in a_tag.attrs:
#                         link = a_tag['href']
#                         link = base_url + link
#                         links.append(link)
#                         print(link)
#         else:
#             print("Inner div with class 'ticket clearfix pinned' not found.")

if __name__ == "__main__":
    get_data(url)



