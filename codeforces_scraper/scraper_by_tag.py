import requests
from bs4 import BeautifulSoup
import json

def fetch_codeforces_problems(filter_tag=None):
    base_url = "https://codeforces.com/problemset"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    }

    problems = []
    page = 1

    while True:
        # Add pagination and tag filter to the URL
        params = {"tags": filter_tag} if filter_tag else {}
        params["page"] = page

        response = requests.get(base_url, headers=headers, params=params)

        if response.status_code != 200:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            break

        soup = BeautifulSoup(response.content, 'html.parser')

        # Parse the problemset table
        problem_table = soup.find('table', class_='problems')
        if not problem_table:
            print(f"No problems found on page {page}. Exiting.")
            break

        new_problems = 0

        for row in problem_table.find_all('tr')[1:]:  # Skip the header row
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

            new_problems += 1

        if new_problems == 0:
            # No more problems on the next page
            break

        print(f"Fetched {new_problems} problems from page {page}.")
        page += 1

    return problems

if __name__ == "__main__":
    tag_to_filter = input("Enter a tag to filter problems (leave empty to fetch all): ").strip()
    problems = fetch_codeforces_problems(tag_to_filter if tag_to_filter else None)

    if problems:
        output_file = f"codeforces_problems_{tag_to_filter if tag_to_filter else 'all'}.json"
        with open(output_file, 'w', encoding='utf-8') as json_file:
            json.dump(problems, json_file, ensure_ascii=False, indent=4)

        print(f"Fetched {len(problems)} problems and saved to '{output_file}'.")
    else:
        print("No problems fetched.")
