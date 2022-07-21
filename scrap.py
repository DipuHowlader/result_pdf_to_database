import psycopg2
from PyPDF2 import PdfFileReader
from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
import datetime
import re


def extract_from_pdf(source):
    results = []
    info_for_passed_sudent = []
    info_for_reffed_sudent = []
    id = 0
    with open(source, 'rb') as file:
        pdf = PdfFileReader(file)
        for no_of_page in range(pdf.getNumPages()):
            # 134513 { 65852(T), 66454(T) }
            page = pdf.pages[no_of_page].extract_text()
            pattern_for_passed_student = r'[0-9][0-9][0-9][0-9][0-9][0-9][^\S\n\t]\([0-9][.][0-9][0-9]\)'
            pattern_for_refered_student = r'([0-9][0-9][0-9][0-9][0-9][0-9][^\S\n\t](?s){.*?})'
            info_for_reffed_sudent.extend(
                re.findall(pattern_for_refered_student, page))
            info_for_passed_sudent.extend(
                re.findall(pattern_for_passed_student, page))

    for item in info_for_passed_sudent:
        roll = item.split(' ')[0].strip()
        mark = item.split(' ')[1].replace('(', '').replace(')', '')

        result = {
            "id": id,
            "roll": roll,
            "passed": True,
            "result": mark,
        }

        # result = {roll: mark}
        results.append(result)
        id += 1

    for item in info_for_reffed_sudent:
        roll = item.split('{')[0].strip()
        reffered_subjects = item.split('{')[1].replace('}', '').replace(
            ' ', '').replace('\n', '').replace('(T,P)', '').replace('(T)', '').replace('(P)', '').split(',')

        result = {
            "id": id,
            "roll": roll,
            "passed": False,
            "failed_subjects": reffered_subjects
        }
        results.append(result)
        id += 1
    return results


def extract_data_from_web(url):
    books_list = []
    html_content = requests.get(url).text
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

            data = {
                "id": id,
                "code": book_code,
                "name": book_name,
                "depermant": deparment,
                "semester": semester,
            }

            dep_text = item.find_previous(name='p').text

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

    return books_list
