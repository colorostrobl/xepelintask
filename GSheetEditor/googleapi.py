from __future__ import print_function
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


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
    print('Changing cell ' + range +' to value: ' + value)
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
        print(f"{result.get('updatedCells')} cells updated.")
        return result
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error
