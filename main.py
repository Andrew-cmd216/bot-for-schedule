import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Define the scope
scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# Add credentials
creds = Credentials.from_service_account_file('Credential/Credentials.json', scopes=scope)

# Authenticate and create the client
client = gspread.authorize(creds)

# Open the spreadsheet
sheet = client.open('Your Sheet Name').sheet1