from PyPDF2 import PdfFileReader
import os
import sys
import re
import uuid

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from database.database import Database

class Result:
    def __init__(self, source):
        self.source = source

    def extract_from_pdf(self):
        results = []
        info_for_passed_sudent = []
        info_for_reffed_sudent = []
        id = 0
        with open(self.source, 'rb') as file:
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
                "result": mark,
                'student_id': id
            }

            results.append(result)
            id += 1

        char_to_replace =['}','-','\n','(T)','(','T','P',')','F','expelled_sub','withheld_sub','reffered_sub',';', ' ']
        for item in info_for_reffed_sudent:
            roll = item.split('{')[0].strip()
            reffered_subjects = item.split('{')[1]
            for char in char_to_replace:
                reffered_subjects = reffered_subjects.replace(char, '')
            
            fixed = []
            for i in tuple(map(str, reffered_subjects.replace('[','').replace(']','').split(','))):
                if len(str(i)) > 5:
                    fixed.append(i[:len(i)//2])
                    fixed.append(i[len(i)//2:])
                else:
                    fixed.append(i)

            
            result = {
                "id": id,
                "roll": roll,
                "failed_subjects": [int(x) for x in fixed.split(',') if x!= ''],
                'student_id': id
            }

            
            results.append(result)
            id += 1
        return results

    def push_sub_to_database(self, Database):
        database = Database('../database/database.ini')
        database.enter_result(self.extract_from_pdf())


if __name__ == "__main__":
    source = '../source/6th_result_2016.pdf'
    ResultInstance = Result(source)
    ResultInstance.extract_from_pdf()
