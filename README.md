# result_pdf_to_database
python project to scrap data from pdf and web and push to database
Skip to content
Search or jump to…
Pull requests
Issues
Marketplace
Explore

Public
Code
Issues
1
Pull requests
Actions
Security
Insights
result_pdf_to_database/README.md
@DipuHowlader 
DipuHowlder Updated Files
 History
 1 contributor


BTEB RESULT MANAGEMENT SYSTEM

---------
:FOLDERS:
_________

/source : Contains the pdf file that is to be inserted in the postgres tables
         
         Files: 6th_result_2016.pdf -> Contains all the data about the student in the format 
                                     (students Roll, Reffered subject Code, passed student's gpa , colleage name )

/subjects : Contains all the files that prepares data of subject code and name for database 

        Files: subjects.py -> This file contains the a functions that scrap data about diploma books from
                              a external website and prepares it to be inserted in postgres table
                              
                              
/database : Contains all the files that connect the project to database and insert subjects code,
            student's roll, their gpa and reffered subjects to databse

        Files: database.ini -> though This repo doesn't have this file, It will be needed to contain the database
                               information such as database name, host, password and user.
              config.py -> This file will take the data from database.ini and configure it for database.py
               database.py -> This file does the real job it take data from subject and source file and push
               them into database
                              

-------------------
:ROOT FOLDER FILES:
___________________

scrap.py -> This is the main file that connects all the other modules and is used to run the project

requirements.txt -> It contains the required packages for this project to work that can be installed via the command
                    `pip3 install -r requirements.txt`


-------------------
:ENVIRONMENT SETUP:
___________________

1. Clone the Repository to your machine.
2. Create a Virtual Environment using virtualenv or pipenv.
3. `pip3 install -r Requirements.txt` to install the required packages automatically.
4. Make sure the Postgres Service is running and insert database's info to the database.ini file.
5. `python3 database/database.py` to see if the program is running correctly and is able to connect to postgres Server. (Feel free to ask for help if you face any error)

### NOTE: Step 2 is optional but highly recommended to avoid conflicting packages.
Footer
© 2022 GitHub, Inc.
Footer navigation
Terms
Privacy
Security
Status
Docs
Contact GitHub
Pricing
API
Training
Blog
About