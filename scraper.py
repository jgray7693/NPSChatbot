import requests
from bs4 import BeautifulSoup
import json

def scrape_faq(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    faq_data = []
    current_question = None
    current_answers = []
    # print(soup.prettify())
    faq_container = soup.find("div", class_="Component ArticleTextGroup TextWrapped clearfix")
    for tag in faq_container.find_all(["h3", "p", "ul"], recursive=False):  
        if tag.name == "h3":  
            # Save the previous question and answers before starting a new one
            if current_question:
                faq_data.append({"question": current_question, "answer": " ".join(current_answers)})
            
            # Start a new question
            current_question = tag.text.strip()
            current_answers = []  # Reset answers list

        elif tag.name == "p" and current_question:
            # Collect all paragraphs under the latest <h3>
            current_answers.append(tag.text.strip())
        elif tag.name == "ul" and current_question:
            # Collect all list items under the latest <h3>
            current_answers.append("\n".join([li.text.strip() for li in tag.find_all("li")]))

    # Add the last FAQ entry
    if current_question:
        faq_data.append({"question": current_question, "answer": " ".join(current_answers)})

    
    

    # for q, a in zip(questions, answers):
        # print(f"Q: {q.text.strip()}")
        # print(f"A: {a.text.strip()}\n")

    return faq_data

if __name__ == "__main__":
    url = "https://www.nps.gov/yose/faqs.htm"
    faqs = scrape_faq(url)
    # for faq in faqs:
    #     print(f"Q: {faq['question']}")
    #     print(f"A: {faq['answer']}\n")

    with open("faqs.json", "w", encoding="utf-8") as file:
        json.dump(faqs, file, ensure_ascii=False, indent=2)