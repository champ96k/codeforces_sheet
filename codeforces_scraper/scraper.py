import requests
from bs4 import BeautifulSoup
import json

def fetch_codeforces_problems():
    base_url = "https://codeforces.com/problemset"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    }
    response = requests.get(base_url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    # Parsing the problemset table
    problem_table = soup.find('table', class_='problems')
    if not problem_table:
        print("Problem table not found.")
        return

    problems = []

    for row in problem_table.find_all('tr')[1:]:  # Skipping the header row
        columns = row.find_all('td')
        if len(columns) < 3:
            continue

        # Extract problem data
        problem_link = columns[0].find('a')
        if not problem_link:
            continue

        title = problem_link.text.strip()
        link = "https://codeforces.com" + problem_link['href']

        # Extract tags
        tags = [tag.text.strip() for tag in columns[1].find_all('a')]

        # Extract difficulty
        difficulty_span = columns[3].find('span', class_='ProblemRating')
        difficulty = difficulty_span.text.strip() if difficulty_span else "Unknown"

        problems.append({
            "title": title,
            "link": link,
            "tags": tags,
            "difficulty": difficulty
        })

    return problems

if __name__ == "__main__":
    problems = fetch_codeforces_problems()
    if problems:
        # Exporting to JSON format
        with open('codeforces_problems.json', 'w', encoding='utf-8') as json_file:
            json.dump(problems, json_file, ensure_ascii=False, indent=4)

        print(f"Fetched {len(problems)} problems and saved to 'codeforces_problems.json'.")
    else:
        print("No problems fetched.")
