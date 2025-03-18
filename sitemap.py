import requests
import xml.etree.ElementTree as ET
from datetime import datetime

# 네이버 블로그 정보
BLOG_ID = "bloomingdreamer"
BASE_URL = f"https://blog.naver.com/{BLOG_ID}/"  # 블로그 메인 URL
RSS_URL = f"https://rss.blog.naver.com/{BLOG_ID}.xml"  # RSS 피드 URL

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

# 🔹 1️⃣ 블로그 메인 페이지 추가
main_url_element = ET.SubElement(sitemap, "url")
ET.SubElement(main_url_element, "loc").text = BASE_URL  # 블로그 메인 URL
ET.SubElement(main_url_element, "lastmod").text = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+09:00")  # 현재 날짜 & 시간
ET.SubElement(main_url_element, "changefreq").text = "daily"
ET.SubElement(main_url_element, "priority").text = "1.0"

# 🔹 2️⃣ 블로그 글 목록 추가
if not items:
    print("❌ RSS에서 게시글을 찾지 못했습니다.")
    exit()


# XML 파일 저장
tree = ET.ElementTree(sitemap)
tree.write(SITEMAP_FILE, encoding="utf-8", xml_declaration=True)

print(f"✅ 사이트맵이 '{SITEMAP_FILE}' 파일로 생성되었습니다! (메인 페이지 + 개별 글 포함)")
