# ログ
from logging import getLogger, handlers, Formatter, DEBUG

def set_logger():
    root_logger = getLogger()
    root_logger.setLevel(DEBUG)

    # ファイル出力
    rotating_handler = handlers.RotatingFileHandler(
        r'./app.log',
        maxBytes=100 * 1024,  # ログローテーションするなら maxBytes を有効にする
        backupCount=3,
        encoding="utf-8"
    )
    format = Formatter('%(asctime)s : %(levelname)s : %(filename)s - %(message)s')
    rotating_handler.setFormatter(format)
    root_logger.addHandler(rotating_handler)
