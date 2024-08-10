import logging.config

def setup_logging():
    # Configured without module name `%(name)s`
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
