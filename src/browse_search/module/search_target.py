from browse_search.common.selenium import get_clickable_target, get_target_clickable_element, check_exist_element, wait_staleness_presence

def search_keyword(word):
    presence_check_el = "div.su-card-container a.image-treatment"
    # 入力
    input_el = get_clickable_target("id", "gh-ac")
    
    if input_el == None:
        return False
    input_el[0].clear()
    input_el[0].send_keys(word)

    # 古い検索結果の先頭を覚える
    old_first_el = check_exist_element("css", presence_check_el)

    # 検索押下
    search_btn_el = get_target_clickable_element("id", "gh-search-btn")
    if search_btn_el:
        search_btn_el[0].click()

    if old_first_el:
        wait_staleness_presence(old_first_el[0])
    check_exist_element("css", presence_check_el)
    
    return True