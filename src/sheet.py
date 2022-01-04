import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive',
]
json_file_name = '/Users/wookey/wookey-dev/bjsr-1-425650a81038.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
gc = gspread.authorize(credentials)
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/18dW8IekVuoaW_POTb3b6ug0iEnUKCaBktpgavomcLgQ/edit#gid=0'

# get doc
doc = gc.open_by_url(spreadsheet_url)

# 시트 선택하기
worksheet = doc.worksheet('bjsr-store')


def write_cells(cell_head, cell_values):
    column = ""
    if cell_head == "name":
        column = "A"
    elif cell_head == "tel":
        column = "B"
    elif cell_head == "address":
        column = "C"

    start_row = 2
    cell_list = worksheet.range(column + str(start_row) + ":" + column)

    for i, val in enumerate(cell_values):
        cell_list[i].value = val

    worksheet.update_cells(cell_list)
