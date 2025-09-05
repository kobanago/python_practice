from selenium.webdriver.common.by import By
# 非同期処理用
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
# driver
from browse_search.common.driver import driver

# 検索型を返還
def get_search_by_element(type):
    match type:
        case "xpath":
           search_by = By.XPATH
        case "tag":
            search_by = By.TAG_NAME
        case "class":
            search_by = By.CLASS_NAME
        case "css":
            search_by = By.CSS_SELECTOR
        case "id":
            search_by = By.ID
        case _:
            raise ValueError(f"不正な検索タイプです: {type}")
    return search_by

def wait_check_presence(type, el):
    return WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((get_search_by_element(type), el))
        )

def wait_staleness_presence(el):
    WebDriverWait(driver, 10).until(EC.staleness_of(el))

# 検索した要素の存在チェック
def check_exist_element(type, el):
    try:            
        elements = wait_check_presence(type, el)
        return elements
    except TimeoutException:
        return None
    except Exception as e:
        print(f"要素取得中にエラー: {e}")
        return None
    
    # 要素が押下可能かを取得する
def get_clickable_target(type, name):
    try:
        el = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((get_search_by_element(type), name))
        )
        cls = el.get_attribute("class") or ""
        if el.is_enabled() != True:
            return None
        if "disable" in cls or "disabled" in cls:
            return None
        if el.get_attribute("aria-disabled") == "true":
            return None
        return [el]
    except Exception:
        return None

# 要素がクリック可能な状態であるか確認する
def get_target_clickable_element(type, name):
    try:
        element = check_exist_element(type, name)
        if element == None:
            return None
        return get_clickable_target(type, name)
    except TimeoutException:
        print(f"要素が見つかりませんでした: {name}")
        return None
