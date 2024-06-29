from django.conf import settings
import openpyxl

class Xl:
    __COLUMNS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def __init__(self, filename: str):
        self.filename = filename
        self.filepath = str(settings.OUT_DIR / filename) + '.xlsx'

    def setup(self, rows, columns):
        pass    
    
    def write(self, content: dict):
        """
        Write timetable to xlsx file.

        Parameters
        ----------
        filename : str
        content : dict e.g. {cell: {column: columnValue, row: rowValue}}
        """
        # Create a new unique xlsx file.
        openpyxl.Workbook().save(self.filepath)

        try:
            # Open workbook and get access to worksheet.
            workbook = openpyxl.load_workbook(self.filepath)
            worksheet = workbook.active
            
            # Write data to excel.
            for key, value in content.items():
                cell = self.__COLUMNS[value['timeslot'].id - 1] + str(value['room'].id)
                worksheet[cell] = key.course.code + '-' + str(key.number)

            workbook.save(self.filepath)
        except Exception as e:
            print('Failed:', e) # Might be caused by file not found or file is running in another window.