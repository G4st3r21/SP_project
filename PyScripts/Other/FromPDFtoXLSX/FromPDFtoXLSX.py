"""
This code converts pdf files from PDFfiles directory to xlsx files and puts it into XLSXfiles directory.
Note that it only converts tables and puts all of them into one sheet separating with one empty row.
"""
from openpyxl import Workbook
import camelot
import time
import os

from PyScripts.Parsers.RegionalProjects.base_functions_RP import get_file_names

current_directory = os.path.dirname(os.path.abspath(__file__))

pdf_files_directory = os.path.join(current_directory, 'PDFfiles')
xlsx_files_directory = os.path.join(current_directory, 'XLSXfiles')

files = get_file_names(pdf_files_directory)

for f in files:
    start_time = time.time()
    pdf_path = pdf_files_directory + "/" + f
    tables = camelot.read_pdf(pdf_path, pages="all")
    wb = Workbook()
    sheet = wb.active
    for i, table in enumerate(tables):
        if i > 0:
            sheet.append([])

        for row in table.df.itertuples(index=False, name=None):
            sheet.append(row)
    xlsx_path = xlsx_files_directory + "/" + f.replace(".pdf", ".xlsx")
    wb.save(xlsx_path)

    end_time = time.time()
    execution_time = end_time - start_time
    print("file ", f, " is converted")
    print("Execution time: {:.2f} секунд".format(execution_time))
