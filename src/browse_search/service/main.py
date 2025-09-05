# エクセル用
from openpyxl import load_workbook
# common
from browse_search.common.selenium import check_exist_element
from browse_search.common.driver import driver
# module
from browse_search.module.get_item_data import get_item_link, get_item_data
from browse_search.module.input_data import input_data

def get_all_data():
    PATH =  input('input path: ')
    wb = load_workbook(PATH)
    ws_search_word = wb["検索ワード"]

    link_list = get_item_link(ws_search_word)
    if link_list is None:
        print("link_listが0件のため処理を終了します")
        return
    data_list = get_item_data(link_list)
    input_data(wb, data_list)

    wb.save(PATH)

def exe():
    TARGET_URL = "https://www.ebay.com/"
    driver.get(TARGET_URL)
    el = check_exist_element("id", "gh-ac-wrap")
    if el != None:
        get_all_data()
