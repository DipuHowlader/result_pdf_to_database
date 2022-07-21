import traceback
import psycopg2
from .config import Config


class Database:
    def __init__(self, file):
        """ Connect to the PostgreSQL database server """
        self.Config = Config
        self.file = file
        print(self.Config)

    def connect(self):
        # read connection parameters
        self.config = Config(self.file, "postgresql")
        self.params = self.config.get_data()

        # connect to the PostgreSQL server
        try:
            print("Connecting to the PostgreSQL database...")
            self.conn = psycopg2.connect(**self.params)
            # create a cursor
            self.cur = self.conn.cursor()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        except:
            traceback.print_exc()

    def enter(self, subjects):
        self.connect()
        if subjects:
            for subject in subjects:
                self.query = f"INSERT INTO app_subjectsmodel (id, code, name, semester, depermant) VALUES ({subject['id']}, {subject['code']}, '{subject['name']}', {subject['semester']}, '{subject['depermant']}')"
                print(self.query)
                print("Updated " + str(subject.values()))
                getattr(self, "cur").execute(self.query)
                getattr(self, "conn").commit()

        self.__exit__()

    def enter_result(self, results):
        self.connect()

        if results:
            for result in results:
                

                if "result" in result:
                    pass
                    # self.query = f"INSERT INTO app_result_of_6th VALUES ({result['id']}, 't', '{result['result']}', null, '{result['student_id']}')"
                else:
                    if result['roll']:
                        self.student_query = f"INSERT INTO app_student VALUES ('{result['id']}', '{result['roll']}');"
                        getattr(self, "cur").execute(self.student_query)
                        getattr(self, "conn").commit()
                        print("Updated " + str(result['roll']))

                    self.query = f"INSERT INTO app_result_of_6th VALUES ({result['id']}, 'f', null ,'{result['failed_subjects']}', '{result['student_id']}')"
                    print(self.query)
                    print("Updated " + str(result.values()))
                    getattr(self, "cur").execute(self.query)

                getattr(self, "conn").commit()

        self.__exit__()

    def __exit__(self):
        for c in ("cur", "conn"):
            try:
                obj = getattr(self, c)
                obj.close()
            except:
                pass


if __name__ == "__main__":
    database = Database("database.ini")
    database.enter([])
