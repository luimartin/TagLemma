import requests
from bs4 import BeautifulSoup

def scrape_all_tagalog_nouns(stop_word="yata", output_file="tagalog_adverbs.txt"):
    base_url = "https://en.wiktionary.org"
    start_path = "/wiki/Category:Tagalog_adverbs"
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
                        nouns.append(word)  # Save only the word (no link)
                        total += 1
                        print(f"[{total}] {word}: {link}")  # Still print link for progress
                        if word.lower() == stop_word.lower():
                            found_stop_word = True
                            break
            if found_stop_word:
                break

        # Find the next page link
        next_link = soup.find('a', text='next page')
        if next_link and next_link.get('href'):
            start_path = next_link['href']
        else:
            start_path = None

    # Save to .txt file
    with open(output_file, 'w', encoding='utf-8') as f:
        for word in nouns:
            f.write(word + '\n')

    print(f"\n✅ Done! Saved {len(nouns)} words (no links) to '{output_file}'.")

# Run the scraper
if __name__ == "__main__":
    scrape_all_tagalog_nouns()
