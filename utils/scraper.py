import time
import requests
from bs4 import BeautifulSoup
from docx import Document

class DocumentationScraper:
    def __init__(self, url: str):
        self.url = url
        self.doc = Document()
        self.visited_urls = set()
       
    def get_links(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True) if self.valid_link(a['href'])]
        return links

    def valid_link(self, link):
        return link.startswith('/view/fusion360/ENU/')  # Modify to match the pattern of valid links

    def get_text(self, url):
        if url in self.visited_urls:
            return ""
        else:
            self.visited_urls.add(url)
            full_url = f"https://help.autodesk.com{url}"  # Construct the full URL if it's a relative URL
            response = requests.get(full_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            text = '\n'.join([p.get_text() for p in soup.find_all('p')])
            return text

    def save_to_docx(self, filename):
        self.doc.save(filename)

    def scrape(self):
        links = self.get_links()
        for link in links:
            text = self.get_text(link)
            if text:
                self.doc.add_paragraph(text)
            time.sleep(1)  # Sleep to respect the website's rate limit

def main():
    f360_user_manual_link = "https://help.autodesk.com/view/fusion360/ENU/?guid=GUID-7B5A90C8-E94C-48DA-B16B-430729B734DC"
    scraper = DocumentationScraper(f360_user_manual_link)
    scraper.scrape()
    scraper.save_to_docx("f360_user_manual.txt")

if __name__ == "__main__":
    main()