import logging


logging.basicConfig(
    filename ='logger/logs.log',
    level=logging.INFO,
    format = '%(asctime)s - %(levelname)s - %(message)s - %(funcName)s'
)

