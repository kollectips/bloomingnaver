import requests
import xml.etree.ElementTree as ET
from datetime import datetime

# 🔹 네이버 블로그 RSS 피드 URL
BLOG_ID = "bloomingdreamer"  # 네이버 블로그 ID 입력
RSS_URL = f"https://rss.blog.naver.com/{BLOG_ID}.xml"

# 🔹 사이트맵 파일 이름
SITEMAP_FILE = "sitemap.xml"

# 🔹 RSS 피드 가져오기
response = requests.get(RSS_URL)
if response.status_code != 200:
    print("❌ RSS 피드를 불러오지 못했습니다. URL을 확인하세요.")
    exit()

# 🔹 XML 파싱
root = ET.fromstring(response.content)

# 🔹 네임스페이스 설정 (네이버 RSS는 네임스페이스가 다를 수 있음)
namespaces = {"ns": "http://purl.org/rss/1.0/"}

# 🔹 사이트맵 XML 기본 구조 생성
sitemap = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

# 🔹 RSS에서 블로그 글 URL 가져오기
items = root.findall(".//item")  # 네이버 RSS는 네임스페이스 없이 `item` 태그를 사용함
if not items:
    print("❌ RSS에서 게시글을 찾지 못했습니다.")
    exit()

for item in items:
    post_url = item.find("link").text  # 블로그 글 URL
    pub_date = item.find("pubDate").text  # 게시글 작성 날짜
    formatted_date = datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %z").strftime("%Y-%m-%d")

    url_element = ET.SubElement(sitemap, "url")
    ET.SubElement(url_element, "loc").text = post_url
    ET.SubElement(url_element, "lastmod").text = formatted_date
    ET.SubElement(url_element, "changefreq").text = "daily"
    ET.SubElement(url_element, "priority").text = "0.8"

# 🔹 XML 파일 저장
tree = ET.ElementTree(sitemap)
tree.write(SITEMAP_FILE, encoding="utf-8", xml_declaration=True)

print(f"✅ 사이트맵이 '{SITEMAP_FILE}' 파일로 생성되었습니다!")
