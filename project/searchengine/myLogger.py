import logging

# Classe per i colori
class bcolors:
    GREEN = '\033[32m'  # Green
    RESET = '\033[0m'  # Reset color
    DEBUG = '\033[34m'  # Blue
    INFO = '\033[37m'  # White
    WARNING = '\033[33m'  # Yellow
    ERROR = '\033[31m'  # Red
    CRITICAL = '\033[91m'  # Bright Red

# Formatter personalizzato per aggiungere i colori
class CustomFormatter(logging.Formatter):
    def __init__(self):
        super().__init__()
        self.FORMATS = {
            logging.DEBUG: bcolors.DEBUG + "%(asctime)s - %(levelname)s - %(message)s" + bcolors.RESET,
            logging.INFO: bcolors.INFO + "%(asctime)s - %(levelname)s - %(message)s" + bcolors.RESET,
            logging.WARNING: bcolors.WARNING + "%(asctime)s - %(levelname)s - %(message)s" + bcolors.RESET,
            logging.ERROR: bcolors.ERROR + "%(asctime)s - %(levelname)s - %(message)s" + bcolors.RESET,
            logging.CRITICAL: bcolors.CRITICAL + "%(asctime)s - %(levelname)s - %(message)s" + bcolors.RESET,
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno, self.FORMATS[logging.INFO])
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

# Configurazione del logger
logger = logging.getLogger("colored_logger")
logger.setLevel(logging.DEBUG)  # Imposta il livello minimo di log

# Aggiungi un handler
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
handler.setFormatter(CustomFormatter())

logger.addHandler(handler)

if __name__ == '__main__':
    
    # Test dei messaggi di log
    logger.debug("This is a DEBUG message")
    logger.info("This is an INFO message")
    logger.warning("This is a WARNING message")
    logger.error("This is an ERROR message")
    logger.critical("This is a CRITICAL message")
