import logging.config

def setup_logging():
    # Configured without module name `%(name)s`
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
