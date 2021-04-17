import openpyxl  # импортируем модуль дря работы с Экселем

# Load book excel
wb = openpyxl.load_workbook('ШУ ТЗ1.xlsx')

# get name sheet and load it
sheet_name = wb.sheetnames[-1]
sheet = wb[sheet_name]
printers={}
# pass for diapason in book and print
for i in sheet['A2':'N74']:
    if i[9]:
        printers[i[9].value] = {
            'Местоположение': f'{i[1].value}  {i[4].value}  {i[5].value}',
            'IP': i[11].value,
            'Инвентарный номер':i[7].value,
            'РМ':i[13].value,
            'Модель':i[10].value
            }

if __name__=='main':
    for i in printers:
        print(printers[i])


help_bot = "Этот бот используется для выдачи инфромации по принтерам ланты. \
Для получения информации используйте  номер ланты сервис "