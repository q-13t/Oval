import logging as log
import configparser as cp

config = cp.ConfigParser()
config.read("config.ini")
LOG_LEVEL = config.getint("SERVER", "LOG_LEVEL")

log.basicConfig(level=log.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

log.info(LOG_LEVEL)
