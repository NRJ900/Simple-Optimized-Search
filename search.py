import requests
from bs4 import BeautifulSoup

# Accept user input
while True:
    question = input("What is your question? ")

    # Send the question to Google search
    url = f"https://www.google.com/search?q={question}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3 Brave/58.0.3029.110'}
    response = requests.get(url, headers=headers)

    # Process the retrieved data
    soup = BeautifulSoup(response.text, "html.parser")
    answer_tags = soup.find_all('div', class_='Z0LcW')

    if len(answer_tags) > 0:
        answer = answer_tags[0].get_text()
        print(answer)
    else:
        print("Sorry, I couldn't find an answer to that question.")
