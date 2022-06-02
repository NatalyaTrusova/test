from loguru import logger
from notifiers.logging import NotificationHandler

params = {
    'token': '5223272425:AAHlQAcLl4EcydP0imyCQUjfxdu_uDJv0Mg',
    'chat_id': '-1001599028566'
}
tg_handler = NotificationHandler("telegram", defaults=params)

telegram_logger = logger
# добавляем в logger правило, что все логи уровня info и выше отсылаются в телегу
telegram_logger.add(tg_handler, level="ERROR")