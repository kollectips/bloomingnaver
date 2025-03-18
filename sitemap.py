import requests
import xml.etree.ElementTree as ET
from datetime import datetime

# 네이버 블로그 RSS 피드 URL
BLOG_ID = "bloomingdreamer"  # 네이버 블로그 ID 입력
RSS_URL = f"https://rss.blog.naver.com/{BLOG_ID}.xml"

# 사이트맵 파일 이름
SITEMAP_FILE = "sitemap.xml"

# RSS 피드 가져오기
response = requests.get(RSS_URL)
if response.status_code != 200:
    print("❌ RSS 피드를 불러오지 못했습니다. URL을 확인하세요.")
    exit()

# XML 파싱
root = ET.fromstring(response.content)
items = root.findall(".//item")

# 사이트맵 XML 생성
sitemap = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

if not items:
    print("❌ RSS에서 게시글을 찾지 못했습니다.")
    exit()

for item in items:
    post_url = item.find("link").text
    pub_date = item.find("pubDate").text  # 네이버 RSS의 pubDate 값 가져오기

    # pubDate를 datetime 객체로 변환
    dt = datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %z")

    # UTC 오프셋을 +09:00 형식으로 변환
    timezone_offset = dt.strftime("%z")  # +0900 형태
    timezone_offset = f"{timezone_offset[:3]}:{timezone_offset[3:]}"  # +09:00 형태로 변환

    # 최종 ISO 8601 형식 (YYYY-MM-DDTHH:MM:SS+09:00)
    formatted_date = dt.strftime("%Y-%m-%dT%H:%M:%S") + timezone_offset

    # Sitemap에 추가
    url_element = ET.SubElement(sitemap, "url")
    ET.SubElement(url_element, "loc").text = post_url
    ET.SubElement(url_element, "lastmod").text = formatted_date  # +09:00 형식 적용됨
    ET.SubElement(url_element, "changefreq").text = "daily"
    ET.SubElement(url_element, "priority").text = "0.8"

# XML 파일 저장
tree = ET.ElementTree(sitemap)
tree.write(SITEMAP_FILE, encoding="utf-8", xml_declaration=True)

print(f"✅ 사이트맵이 '{SITEMAP_FILE}' 파일로 생성되었습니다! (lastmod 시간 +09:00 형식 적용)")
