import logging.config

class WinnerFilter(logging.Filter):
    def __init__(self, param=None):
        self.param = param

    def filter(self, record):
        """
        Filtering logs for record. If it's info about new Warfare with no winner, this record should be
        ignored. We are looking on log string and slice it to find table name and winner. If there is
        no winner, result will be 'None', so winner slice will be 'e' (in other case it will be 1 or 2).
        """
        table_name = record.msg[3:11]
        winner = record.msg[-1]
        not_for_record = table_name == "Warfares" and (winner != "1" and winner != "2")
        if not_for_record:
            is_allowed = False
        else:
            is_allowed = True
        return is_allowed

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,

    'filters': {
            'filter_for_winner': {
                '()': WinnerFilter,
                'param': 'noshow',
            },
        },

    'formatters': {
            'default_formatter': {
                'format': "%(asctime)s => %(filename)s => %(levelname)s => %(message)s"
            },
        },

    'handlers': {
        'insert_file_handler': {
            'class': 'logging.FileHandler',
            'formatter': 'default_formatter',
            'filename': 'logs_for_inserting.txt',
            'level': 'INFO',
            'filters': ['filter_for_winner']
                },
        'delete_file_handler': {
            'class': 'logging.FileHandler',
            'formatter': 'default_formatter',
            'filename': 'logs_for_deleting.txt',
            'level': 'WARNING'
        },
        'integrity_error_file_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'default_formatter',
            'level': 'ERROR'
        }
    },

    'loggers': {
        'logger_INFO': {
            'handlers': ['insert_file_handler', 'delete_file_handler'],
            'level': 'INFO',
            'propagate': False
        },
        'logger_ERROR': {
            'handlers': ['integrity_error_file_handler'],
            'level': 'ERROR',
            'propagate': True
        }
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
my_logger_info = logging.getLogger("logger_INFO")
my_logger_error = logging.getLogger("logger_ERROR")
# logging.config.dictConfig(LOGGING_CONFIG)
# logger = logging.getLogger('my_logger')
# logger.debug('debug log')