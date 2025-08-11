from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

path = input('input path: ')
wb = load_workbook(path)
ws = wb["比較"]

targetCol = 1
comparisonCol = 2

# 最終行取得
def getLastRow():
    for rowNum in range(ws.max_row, 1, -1):
        row = ws[rowNum]
        if any(cell.value is not None for cell in row):
            return rowNum
    return 1

# 同じ値のセルをリストで取得
def getSameValueRow(value, startRow, lastRow, targetCol):
    find_row_list = []
    for row in ws.iter_rows(startRow, lastRow, targetCol, targetCol):
        for cell in row:
            if cell.value == value:
                    find_row_list.append(cell.row)
    return len(find_row_list)

# 挿入行数を取得
def getinsertRowNum(val, targetRow, lastRow, comparisonCol):
    target_row_num = getSameValueRow(val, targetRow, lastRow, comparisonCol)
    if target_row_num == 0:
        col_letter = get_column_letter(comparisonCol)
        insertRow = 1
    else:
        col_letter = get_column_letter(targetCol)
        insertRow = target_row_num
    return insertRow, col_letter


# target列とcomparison列の比較
def compareData():
    lastRow = getLastRow()
    i = 1 
    # whileループを使用してlastRowの変更を反映
    while i <= lastRow:
        val_t = ws.cell(i, targetCol).value
        val_c = ws.cell(i, comparisonCol).value
        val_t = int(val_t if val_t is not None else 0)
        val_c = int(val_c if val_c is not None else 0)

        # 値が異なる場合
        if val_t != val_c:
            # どちらも値がある場合
            if val_t != 0 and val_c != 0:
                # targetがcomparison より小さい場合
                if val_t < val_c:
                    insertRow, col_letter = getinsertRowNum(val_t, i, lastRow, comparisonCol) 
                # comparisonがtarget より小さい場合
                else:
                     insertRow, col_letter = getinsertRowNum(val_c, i, lastRow, targetCol) 
                # 行ずらし
                ws.move_range(f"{col_letter}{i}:{col_letter}{lastRow}", rows=insertRow, cols=0) 
                lastRow = lastRow + insertRow 
        i += 1

compareData()
wb.save(path)
