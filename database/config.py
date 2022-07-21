from configparser import ConfigParser


class Config:
    def __init__(self, file, section) -> None:
        self.file = file
        self.section = section

    def get_data(self):
        parser = ConfigParser()
        parser.read(self.file)
        db = {}

        if parser.has_section(self.section):
            params = parser.items(self.section)
            for param in params:
                db[param[0]] = param[1]

        return db
