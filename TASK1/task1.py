import requests
import re
from bs4 import BeautifulSoup

def check_response(r):
    if r.status_code == 200:
        print("Web request success !")
        return 0
    else:
        print("Web request fail !")
        return 1

def get_all_href_on_page(soup):
    href_list = []
    
    for a_tag in soup.find_all('a', href=True):
        href_list.append(a_tag['href'])

    return href_list

def get_top100_filenumbers_on_page(soup):
    file_numbers = []
    top100_section = soup.find('h2', string="Top 100 EBooks yesterday")
    if top100_section:
        parent = top100_section.find_next_sibling()
        if parent and parent.name == 'ol':  
            links = parent.find_all('a', href=True)
            for link in links[:100]:
                match = re.search(r'\((\d+)\)$', link.text.strip())  
                if match:
                    file_numbers.append(match.group(1))  
    return file_numbers

def get_top100_ebooks_Yesterday(soup):
    book_titles = []
    top100_section = soup.find('h2', string="Top 100 EBooks yesterday")
    if top100_section:
        parent = top100_section.find_next_sibling()
        links = parent.find_all('a') if parent else []
        for link in links[:100]:
            title_author = link.text.strip()
            clean_title = re.sub(r"\s*\(\d+\)$", "", title_author) 
            book_titles.append(clean_title)
    return book_titles

url = "https://www.gutenberg.org/browse/scores/top"
print(f"กำลังร้องขอข้อมูลจาก {url}")

try:
    response = requests.get(url)
    if check_response(response) == 1:
        print("ไม่สามารถดึงข้อมูลได้ กรุณาตรวจสอบการเชื่อมต่ออินเทอร์เน็ต")
        exit()

    soup = BeautifulSoup(response.text, 'html.parser')

    all_links = get_all_href_on_page(soup)
    print(f"พบลิงก์ทั้งหมด {len(all_links)} ลิงก์\n")

    print("ตัวอย่างลิงก์ 30 รายการแรก:")
    for i, link in enumerate(all_links[:30], start=1):
        print(f"{link}")
    print("\n")

    file_numbers = get_top100_filenumbers_on_page(soup)
    print("\nหมายเลขไฟล์ eBooks 100 อันดับแรก:")
    print(file_numbers)  

    text_data = soup.get_text(separator=" ").strip()
    print("\nข้อความจากหน้าเว็บ (2000 ตัวอักษรแรก):")
    print(text_data[:2000])
    print("...")  

    book_list = get_top100_ebooks_Yesterday(soup)
    print("\nรายชื่อหนังสือ Top 100 จาก Project Gutenberg:")
    for book in book_list:
        print(f" {book}")

except Exception as e:
    print(f"เกิดข้อผิดพลาด: {e}")
