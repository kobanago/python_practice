# データ書き込み
def input_data(wb, data_dict:dict):
    data_keys = data_dict.keys()
    for data_key in data_keys:
        ws = wb.create_sheet(data_key)
        target_list = data_dict[data_key]
        list_len = len(target_list)
        list_keys = list(target_list[0].keys())
        keys_len = len(list_keys)

        # ヘッダー設定 
        ws.cell(1, 1).value = "商品名"
        ws.cell(1, 2).value = "値段(ドル)"
        ws.cell(1, 3).value = "配達日"

        for cnt in range(0, list_len):
            for key_cnt in range(0, keys_len):
                key_name = list_keys[key_cnt]  # 例: "title"
                ws.cell(cnt + 3, key_cnt + 1).value = target_list[cnt][key_name]
