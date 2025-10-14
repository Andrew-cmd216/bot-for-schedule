import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from pathlib import Path


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

data = sheet.get_values()
df = pd.DataFrame(data)
print(df)