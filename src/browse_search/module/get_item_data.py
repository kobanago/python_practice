from selenium.common.exceptions import TimeoutException
# common
from browse_search.common.selenium import check_exist_element, get_target_clickable_element, wait_staleness_presence, wait_check_presence
from browse_search.common.excel import get_last_row
# module
from browse_search.module.search_target import search_keyword
# driver
from browse_search.common.driver import driver

def check_next_page(target_el):
    # ページ数確認
    try:
        pagenation_el = "nav.pagination .pagination__next"
        next_page_el = get_target_clickable_element("css", pagenation_el)

        if not next_page_el:
            print("次ページなし → 終了")
            return False
        old_first = check_exist_element("css", target_el)
        next_page_el[0].click()

        if old_first:
            wait_staleness_presence(old_first[0])

        if wait_check_presence("css", target_el) == None:
            return False
        return True
    except Exception as e:
        print("次ページ取得失敗:", e)
        return False

def get_item_link(ws):
    last_row = get_last_row(ws)
    link_list = {}
    target_el = "div.su-card-container a.image-treatment"

    for row in range(2, last_row + 1, 1):
        # 検索ワードを検索
        search_word = ws.cell(row, 1).value
        if search_keyword(search_word) == False:
            print("検索処理に失敗しました")

        while True:
            link_element = check_exist_element("css", target_el)
            if link_element == None:
                break
            for el in link_element:
                try:
                    href = el.get_attribute("href")
                    link_list.setdefault(search_word, []).append(href)
                except Exception as e:
                    print("href_get_attribute失敗:", e)
                    return link_list

            if not check_next_page(target_el):
                break
            if check_exist_element("css", target_el) == None:
                break
    return link_list

    
def get_element_text_value(title_el, price_el, deleveryday_el):
    title = check_exist_element("class", title_el)
    title = "取得失敗" if title is None else title[0].text.strip()

    price = check_exist_element("css", price_el)
    price = "取得失敗" if price is None else price[0].text.strip()

    deleveryday = check_exist_element("xpath", deleveryday_el)
    deleveryday = "取得失敗" if deleveryday is None else deleveryday[0].text.strip()
    return [title, price, deleveryday]

def safe_get(url):
    try:
        driver.get(url)
        return True
    except TimeoutException:
        print(f"Timeoutエラー: {url}")
        return False
    except Exception as e:
        print(f"その他エラー: {url} - {e}")
        return False

def get_item_data(link_dict:dict):
    link_keys = link_dict.keys()
    data_list = {}
    title_el = "x-item-title__mainTitle"
    price_el = "div.x-price-primary > span"
    deleveryday_el = (
        "//div[@data-testid='ux-labels-values' and contains(@class,'ux-labels-values--deliverto')]"
    )

    for key in link_keys:
        for url in link_dict[key]:
            if not safe_get(url):
                data_list.setdefault(key, []).append({
                    "title": "取得失敗",
                    "price": "取得失敗",
                    "delivery": "取得失敗",
                    "link": url
                })
                continue
            [title, price, deleveryday] = get_element_text_value(title_el, price_el, deleveryday_el)
            data_list.setdefault(key, []).append({
                "title": title,
                "price": price,
                "delivery": deleveryday,
                "link": url
            })
    return data_list
