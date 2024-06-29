from django.conf import settings
import openpyxl

COLUMNS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def write_xl(filename: str, content: dict):
    """
    Write timetable to xlsx file.

    Parameters
    ----------
    filename : str
    content : dict e.g. {cell: {column: columnValue, row: rowValue}}
    """
    # Create a new unique xlsx file.
    filepath = str(settings.OUT_DIR / filename) + '.xlsx'
    openpyxl.Workbook().save(filepath)

    try:
        # Open workbook and get access to worksheet.
        workbook = openpyxl.load_workbook(filepath)
        worksheet = workbook.active
        
        # Write data to excel.
        for key, value in content.items():
            cell = COLUMNS[value['timeslot'].id - 1] + str(value['room'].id)
            worksheet[cell] = key.course.code + '-' + str(key.number)

        workbook.save(filepath)
    except Exception as e:
        print('Failed:', e) # Might be caused by file not found or file is running in another window.