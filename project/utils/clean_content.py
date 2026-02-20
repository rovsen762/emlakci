from bs4 import BeautifulSoup,Tag
import re


def clean_soup_tags(soup: BeautifulSoup, container: Tag) -> None:
    
    for tag in container.find_all(['script', 'iframe', 'video']):
        tag.decompose()

    for a_tag in container.find_all('a'):
        if a_tag and a_tag.has_attr('href'):
            new_a_tag = soup.new_tag('a', href=a_tag['href'])
            new_a_tag.string = a_tag.get_text(strip=True)
            a_tag.replace_with(new_a_tag)
        else:
            a_tag.decompose()
            
            
def extract_gallery_images(news_content):
   
    gallery_images = []
    images = news_content.find_all('img')

    for image in images: 
        src = None
        if image and image.has_attr('data-src'):
            src = image['data-src'].strip()
        elif image and image.has_attr('src'):
            src = image['src'].strip()

        if src:
            gallery_images.append(src)

    for img in images:
        img.decompose()

    return gallery_images


            
def clean_html_withregex(content: str) -> str:
    if not content:
        return None

    content = re.sub(r'<div>\s*</div>', '', content)

    content = re.sub(r'<div>\s*(<div>\s*</div>\s*)+\s*</div>', '', content)

    content = re.sub(r'<div>\s*<svg[^>]*?>[\s\S]*?</svg>\s*</div>', '', content)

    content = re.sub(r'(<div>\s*){2,}(</div>\s*){2,}', '', content)

    content = re.sub(r'\n\s*\n+', '\n', content)

    content = re.sub(r'<\s*br\s*/?>', ' ', content, flags=re.IGNORECASE)

    content = re.sub(r'<\s*/?\s*o:p\s*>', '', content, flags=re.IGNORECASE)

    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)

    content = re.sub(r'^\s*\n', '', content, flags=re.MULTILINE)

    return content
            
            

def clean_unwantedtags_com(content_element):
    soup = BeautifulSoup(content_element, 'html.parser')
    
    
    #div ve p taglari bosdursa silir
    for tag in soup.find_all(["p", "div","style","span","button","blockquote","li","section","b","figure","figcaption","h2","h1","h3","h4","h5","h6","ol","td","table","ul","use","style","aside","article","i","strong"]):
        if not tag.text.strip() and not tag.find():  
            tag.decompose()
            
    #DIV VE P class adlari ve diger attributlari silir
    for tag in soup.find_all(["div", "p","style","span","button","blockquote","li","section","b","figure","figcaption","h2","h1","h3","h4","h5","h6","ol","td","table","ul","use","style","aside","article","i","strong"]):
        tag.attrs = {}  
    
    return str(soup)
        



