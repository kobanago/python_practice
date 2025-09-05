# ログ
from logging import getLogger
# common 
from browse_search.common.log import set_logger
# service
from browse_search.service.main import exe
# driver
from browse_search.common.driver import driver

set_logger()
logger = getLogger(__name__)
try:
    exe()
except Exception as e:
    logger.exception("エラー発生", exc_info=e)
finally:
    driver.quit()