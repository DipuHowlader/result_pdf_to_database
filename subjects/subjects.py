from bs4 import BeautifulSoup
import os
import requests
import re
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.database import Database

class Subjects:
    def __init__(self, url):
        self.url = url

    def extract_data_from_web(self):
        # every single book list as a dict will be updated in in book Variable
        books_list = []
        # connect to the webpage where to get all the book list
        html_content = requests.get(self.url).text
        soup = BeautifulSoup(html_content, "lxml")
        books = soup.find_all("li")
        semester = '1'
        deparment = "Electrical"

        id = 0
        for item in books:
            pattern = r'[0-9][0-9][0-9][0-9][0-9]'
            if not re.search(pattern, item.text) == None:
                semester = item.find_previous(name='h2').text[0]
                book_code = re.search(pattern, item.text).group(0)
                book_name = item.text.replace(book_code, '').replace(
                    '(', '').replace(')', '').strip()
                # print(re.search(pattern, item.text).group())

                # acceptable database format
                data = {
                    "id": id,
                    "code": book_code,
                    "name": book_name,
                    "depermant": deparment,
                    "semester": semester,
                }

                dep_text = item.find_previous(name='p').text


                # get the deparment value
                if "2016" in dep_text:
                    if "Civil" in dep_text:
                        deparment = "Civil"
                    elif "Computer" in dep_text:
                        deparment = "Computer"
                    elif "marine" in dep_text:
                        deparment = "Marine"
                    elif "RAC" in dep_text:
                        deparment = "RAC"
                    elif "POWER" in dep_text:
                        deparment = "POWER"
                    elif "Electronics" in dep_text:
                        deparment = "Electronics"
                    elif "Electrical" in dep_text:
                        deparment = "Electrical"
                    elif "Mechanical" in dep_text:
                        deparment = "Mechanical"

                    books_list.append(data)
                    id += 1

                if book_code == "68546":
                    print(data)
                

        return books_list


    def push_sub_to_database(self, Database):
        self.path = os.path.join('database', 'database.ini')
        database = Database('../database/database.ini')
        database.enter(self.extract_data_from_web())



if __name__ == "__main__":
    url = os.environ.get('URL')
    SubjectsInstance = Subjects(url)
    SubjectsInstance.extract_data_from_web()
    # SubjectsInstance.push_sub_to_database(Database)