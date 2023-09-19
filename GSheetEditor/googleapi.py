from __future__ import print_function
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import requests


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1K7pAu91P8CLyjRk4rD1WuOg8gljC3IKml09SIxtCzww'
RANGE_NAME = 'A1:C11'


def reader():
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    try:
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=RANGE_NAME).execute()
        values = result.get('values', [])
        return values

    except HttpError as err:
        raise HttpError(err)


def editor(range, value):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    try:
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        values = [
            [
                value
            ],
        ]
        body = {
            'values': values
        }
        result = sheet.values().update(
            spreadsheetId=SPREADSHEET_ID, range=range,
            valueInputOption="USER_ENTERED", body=body).execute()
        return result
    except HttpError as error:
        return error


def send_email(row):
    url = 'https://hooks.zapier.com/hooks/catch/6872019/oahrt5g/'
    data = {
        'idOp': int(row[0]),
        'tasa': float(row[1].replace(',', '.')),
        'email': row[2]
    }

    response = requests.post(url, data=data)
    return response
