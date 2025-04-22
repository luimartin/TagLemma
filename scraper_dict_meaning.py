import requests
from bs4 import BeautifulSoup
import csv
import time

def scrape_all_tagalog_nouns(stop_word="yata", output_file="tagalog_nouns_meaning.csv"):
    base_url = "https://en.wiktionary.org"
    start_path = "/wiki/Category:Tagalog_nouns"
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    nouns = []
    seen = set()
    found_stop_word = False
    total = 0

    while start_path and not found_stop_word:
        response = requests.get(base_url + start_path, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch: {base_url + start_path}")
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        main_div = soup.select_one('div#mw-pages > div > div')
        if not main_div:
            print("Main content not found.")
            break

        for ul in main_div.find_all('ul'):
            for li in ul.find_all('li'):
                a_tag = li.find('a')
                if a_tag and a_tag.get('href') and a_tag.get('title'):
                    word = a_tag.text.strip()
                    link = base_url + a_tag['href']
                    if word.lower() not in seen:
                        seen.add(word.lower())
                        meaning = get_noun_meaning(link, headers)
                        if not meaning:
                            meaning = "No meaning provided"
                        nouns.append((word, meaning))
                        total += 1
                        print(f"[{total}] {word}: {meaning}")
                        if word.lower() == stop_word.lower():
                            found_stop_word = True
                            break
                        time.sleep(1)  # Be polite to the server
            if found_stop_word:
                break

        # Find the next page link
        next_link = soup.find('a', string='next page')
        if next_link and next_link.get('href'):
            start_path = next_link['href']
        else:
            start_path = None

    # Save to CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Word', 'Meaning'])
        writer.writerows(nouns)

    print(f"\n✅ Done! Saved {len(nouns)} words with meanings to '{output_file}'.")

def get_noun_meaning(link, headers):
    try:
        response = requests.get(link, headers=headers)
        if response.status_code != 200:
            return "No meaning provided"
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find Tagalog language section
        tagalog_heading = soup.find('span', id='Tagalog')
        if not tagalog_heading:
            return "No meaning provided"

        tagalog_div = tagalog_heading.find_parent('h2')
        next_sibling = tagalog_div.find_next_sibling()

        while next_sibling:
            if next_sibling.name == 'h3' and next_sibling.find('span', id='Noun'):
                noun_section = next_sibling
                break
            next_sibling = next_sibling.find_next_sibling()
        else:
            return "No meaning provided"

        # Get content until the next heading
        sib = noun_section.find_next_sibling()
        while sib and sib.name not in ['h2', 'h3']:
            if sib.name == 'p':
                italic = sib.find('i')
                if italic:
                    return italic.text.strip()
            sib = sib.find_next_sibling()

        return "No meaning provided"
    except Exception:
        return "No meaning provided"

# Run the scraper
if __name__ == "__main__":
    scrape_all_tagalog_nouns()
