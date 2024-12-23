import requests
from bs4 import BeautifulSoup
import json

def fetch_problems_for_tag(tag, limit=50):
    base_url = "https://codeforces.com/problemset"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    }

    problems = []
    page = 1

    while len(problems) < limit:
        params = {"tags": tag, "page": page}
        response = requests.get(base_url, headers=headers, params=params)

        if response.status_code != 200:
            print(f"Failed to fetch data for tag '{tag}'. Status code: {response.status_code}")
            break

        soup = BeautifulSoup(response.content, 'html.parser')

        # Parse the problemset table
        problem_table = soup.find('table', class_='problems')
        if not problem_table:
            print(f"No problems found for tag '{tag}' on page {page}. Exiting.")
            break

        for row in problem_table.find_all('tr')[1:]:  # Skip the header row
            if len(problems) >= limit:
                break

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

        print(f"Fetched {len(problems)} problems for tag '{tag}' so far.")
        page += 1

    return problems[:limit]

def fetch_all_sections(tags, limit=50):
    all_problems = {}
    for tag in tags:
        print(f"Fetching problems for tag: {tag}")
        all_problems[tag] = fetch_problems_for_tag(tag, limit=limit)
        print(f"Completed fetching problems for tag: {tag}\n")
    return all_problems

if __name__ == "__main__":
    # List of tags to fetch problems for
    tags = ["binary search", "dp", "greedy", "math", "graphs"]

    problems_by_section = fetch_all_sections(tags, limit=50)

    # Save the results to a JSON file
    with open('codeforces_problems_by_section.json', 'w', encoding='utf-8') as json_file:
        json.dump(problems_by_section, json_file, ensure_ascii=False, indent=4)

    print("Fetched problems for all sections and saved to 'codeforces_problems_by_section.json'.")
