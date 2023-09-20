from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import requests


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1UlsvCxYmEUKC8aSl5WCd2zphNEUKYmUkxrZMR9Ujd1E'
RANGE = 'A:D'
CREDS = Credentials.from_authorized_user_file('token2.json', SCOPES)


def clean_spreadsheet():
    """
    Borra los contenidos de la GSheet.

    Parameters:
    - None.

    Returns:
    - response object del llamado a la googleapi para googlesheets.
    """

    try:
        service = build('sheets', 'v4', credentials=CREDS)
        sheet = service.spreadsheets()
        result = sheet.values().clear(spreadsheetId=SPREADSHEET_ID,
                                      range=RANGE).execute()
        return result

    except HttpError as err:
        return err


def write_header():
    """
    Escribe el Header correspondiente para la GSheet

    Parameters:
    - None.

    Returns:
    - response object del llamado a la googleapi para googlesheets.
    """

    try:
        service = build('sheets', 'v4', credentials=CREDS)
        sheet = service.spreadsheets()
        body = {
          "valueInputOption": "USER_ENTERED",
          "includeValuesInResponse": False,
          "responseDateTimeRenderOption": "FORMATTED_STRING",
          "responseValueRenderOption": "FORMATTED_VALUE",
          "data": [
            {
              "range": "A1:D1",
              "values": [
                [
                  "Titular",
                  "Categoría",
                  "Autor",
                  "Tiempo de lectura"
                ]
              ]
            }
          ]
        }
        result = sheet.values().batchUpdate(
            spreadsheetId=SPREADSHEET_ID, body=body).execute()
        return result
    except HttpError as error:
        return error


def populate_gsheet(contents):
    """
    Escribe el contenido en la GSheet.

    Parameters:
    - contents (list): lista de dictionarios con el contenido a escribir en la GSheet.

    Returns:
    - response object del llamado a la googleapi para googlesheets.
    """

    try:
        clean_spreadsheet()
        write_header()
        service = build('sheets', 'v4', credentials=CREDS)
        sheet = service.spreadsheets()
        range = "A2:D" + str(1+len(contents))
        values = []

        for content in contents:
            values.append([content['title'],
                           content['category'],
                           content['author'],
                           content['time']])

        body = {
            "valueInputOption": "USER_ENTERED",
            "includeValuesInResponse": False,
            "responseDateTimeRenderOption": "FORMATTED_STRING",
            "responseValueRenderOption": "FORMATTED_VALUE",
            "data": [
                {
                    "range": range,
                    "values": values
                }
            ]
        }
        result = sheet.values().batchUpdate(spreadsheetId=SPREADSHEET_ID, body=body).execute()
        return result
    except HttpError as error:
        return error


def webhook_response(webhook):
    """
    Ejecuta el POST al webhook.

    Parameters:
    - webhook (string): url del webhook.

    Returns:
    - response object del POST al webhook.
    """
    data = {
        'link': 'https://docs.google.com/spreadsheets/d/1UlsvCxYmEUKC8aSl5WCd2zphNEUKYmUkxrZMR9Ujd1E',
        'email': 'taskerxepelin@gmail.com'
    }

    response = requests.post(webhook, data=data)
    return response
