import pandas as pd

class Singleton:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance.load_data()
        return cls._instance

    def __getitem__(self, key):
        return self.df[key]

    def load_data(self):
        self.df = pd.read_json("static/songs.json")
        print(self.df.head(5))