import requests
import xml.etree.ElementTree as ET
from datetime import datetime

# 네이버 블로그 RSS 피드 URL
BLOG_ID = "bloomingdreamer"
RSS_URL = f"https://rss.blog.naver.com/{BLOG_ID}.xml"

# 사이트맵 파일 이름
SITEMAP_FILE = "sitemap.xml"

# RSS 피드에서 글 목록 가져오기
response = requests.get(RSS_URL)
root = ET.fromstring(response.content)

# 네임스페이스 설정
ns = {"ns": "http://purl.org/rss/1.0/"}

# 사이트맵 XML 기본 구조
sitemap = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

# RSS에서 블로그 글 가져오기
for item in root.findall(".//ns:item", ns):
    post_url = item.find("ns:link", ns).text
    post_date = item.find("ns:date", ns).text[:10]  # YYYY-MM-DD 형식

    url_element = ET.SubElement(sitemap, "url")
    ET.SubElement(url_element, "loc").text = post_url
    ET.SubElement(url_element, "lastmod").text = post_date
    ET.SubElement(url_element, "changefreq").text = "daily"
    ET.SubElement(url_element, "priority").text = "0.8"

# XML 파일로 저장
tree = ET.ElementTree(sitemap)
tree.write(SITEMAP_FILE, encoding="utf-8", xml_declaration=True)

print(f"✅ 사이트맵이 '{SITEMAP_FILE}' 파일로 생성되었습니다!")