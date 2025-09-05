# エクセル最終行取得
def get_last_row(ws):
    for row in range(ws.max_row, 1, -1):
        if any(cell.value is not None for cell in ws[row]):
            return row
    return 1

# エクセル最終列取得
def get_last_col(ws):
    for col in range(ws.max_column, 1, -1):
        for cells in ws.iter_cols(min_col=col, max_col=col):
            if any(cell.value is not None for cell in cells):
                return col
    return 1
