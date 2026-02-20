# import requests
# from bs4 import BeautifulSoup
# import re

# from dateutil import parser
# import pytz

# from utils.clean_content import clean_armenianweekly_com


# def scrape_meta_title(soup):
#     tag = soup.find("meta", {"property": "og:title"})
#     return tag["content"] if tag and "content" in tag.attrs else None


# def scrape_meta_description(soup):
#     tag = soup.find("meta", {"property": "og:description"})
#     return tag["content"] if tag and "content" in tag.attrs else None


# def scrape_meta_url(soup):
#     tag = soup.find("meta", {"property": "og:image"})
#     return tag["content"] if tag and "content" in tag.attrs else None


# def scrape_meta_news_shared_date_1(soup):
#     tag = soup.find("meta", {"property": "og:article:published_time"})
#     if tag and "content" in tag.attrs:
#         try:
#             dt_utc = parser.parse(tag["content"])
#             baku_tz = pytz.timezone("Asia/Baku")
#             return dt_utc.astimezone(baku_tz)
#         except Exception:
#             return None
#     return None



# def scrape_meta_news_shared_date(soup):
#     meta_attrs = [
#         {"property": "article:published_time"},
#         {"name": "article:published_time"},
#         {"property": "og:updated_time"},
#         {"name": "dcterms.created"},
#     ]
    
#     for attrs in meta_attrs:
#         tag = soup.find("meta", attrs=attrs)
#         if tag and tag.has_attr("content"):
#             return tag["content"]
    
#     return None

