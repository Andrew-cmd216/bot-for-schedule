import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from pathlib import Path


class Schedule:
    def get_monday(self):
        return 'понедельник'
    def get_tuesday(self):
        return 'вторник'
    def get_wednesday(self):
        return 'среда'
    def get_thursday(self):
        return 'четверг'
    def get_friday(self):
        return 'пятница'
    def get_saturday(self):
        return 'суббота'



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
sheet = client.open('кадабра1').sheet1