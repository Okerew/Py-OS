import requests
from bs4 import BeautifulSoup
from termcolor import colored

def fetch_webpage(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching webpage: {e}")
        return None

def apply_css_styles(tag):
    if tag.name == "a":
        return colored(tag.get_text(), 'blue')
    return tag.get_text()

def display_webpage(content):
    if content is not None:
        soup = BeautifulSoup(content, 'html.parser')
        for tag in soup.find_all(['p', 'a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            styled_text = apply_css_styles(tag)
            print(styled_text)
            print()

def main():
    print("PyOS Web Browser")
    while True:
        user_input = input("Enter a URL (or ':q' to quit): ")
        if user_input.lower() == ":q":
            break
        else:
            content = fetch_webpage(user_input)
            display_webpage(content)

if __name__ == "__main__":
    main()
