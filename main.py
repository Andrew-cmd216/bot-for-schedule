import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from pathlib import Path

def make_req() -> pd.DataFrame:
    '''Function called for accessing specific data from the table'''
    sheet = client.open('кадабра1').get_worksheet(2)
    data = sheet.get_values()
    df = pd.DataFrame(data)
    return df

class DayOfTheWeek:
    """Class that stores the info of the day of the week"""
    def __init__(self,
                 subset: pd.DataFrame):
        self.subset = subset
    def get_data(self, group_id: int) -> pd.DataFrame:
        if group_id == 1:
            table = self.subset.iloc[:, 2:4].join(self.subset.iloc[:, 14:17])
        else:
            table = self.subset.iloc[:, 2:4].join(self.subset.iloc[:, 18:21])
        table = table.replace({"К": "ул. Костина 2Б",
                               'Л': 'ул. Львовская 1В',
                               'БП': 'ул. Большая Печёрская 25/12',
                               'Р': 'ул. Родионова 136',
                               "С": "Сормовское шоссе 30"})
        return table


class Schedule:
    '''Class responsible for parsing the table and organising the data in groups'''

    df: pd.DataFrame
    monday: DayOfTheWeek
    tuesday: DayOfTheWeek
    wednesday: DayOfTheWeek
    thursday: DayOfTheWeek
    friday: DayOfTheWeek
    saturday: DayOfTheWeek

    def __init__(self):
        self.__df = None
        self._monday = None
        self._tuesday = None
        self._wednesday = None
        self._thursday = None
        self._friday = None
        self._saturday = None

    def fill_the_table(self) -> None:
        '''Function to fill self.__df'''
        self.__df = make_req()
    def _make_monday(self):
        monday = DayOfTheWeek(self.__df.iloc[13:20])
        self._monday = monday

    def _make_tuesday(self):
        tuesday = DayOfTheWeek(self.__df.iloc[22:29])
        self._tuesday = tuesday

    def _make_wednesday(self):
        wednesday = DayOfTheWeek(self.__df.iloc[31:38])
        self._wednesday = wednesday

    def _make_thursday(self):
        thursday = DayOfTheWeek(self.__df.iloc[40:43])
        self._thursday = thursday

    def _make_friday(self):
        friday = DayOfTheWeek(self.__df.iloc[45:52])
        self._friday = friday

    def _make_saturday(self):
        saturday = DayOfTheWeek(self.__df.iloc[54:61])
        self._saturday = saturday

    def organise(self):

        self.fill_the_table()
        self._make_monday()
        self._make_tuesday()
        self._make_wednesday()
        self._make_thursday()
        self._make_friday()
        self._make_saturday()

    def get_monday(self, group_id: int):
        return str(self._monday.get_data(group_id))
    def get_tuesday(self, group_id: int):
        return str(self._tuesday.get_data(group_id))
    def get_wednesday(self, group_id: int):
        return str(self._wednesday.get_data(group_id))
    def get_thursday(self, group_id: int):
        return str(self._thursday.get_data(group_id))
    def get_friday(self, group_id: int):
        return str(self._friday.get_data(group_id))
    def get_saturday(self, group_id: int):
        return str(self._saturday.get_data(group_id))



PROJECT_PATH = Path(__file__).parent
CREDENTIALS_PATH = PROJECT_PATH / 'Credential' / 'Credentials.json'

# Define the scope
scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]


# Add credentials
creds = Credentials.from_service_account_file(str(CREDENTIALS_PATH), scopes=scope)


# Authenticate and create the client
client = gspread.authorize(creds)


# Open the spreadsheet
schedule = Schedule()
schedule.organise()