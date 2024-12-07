import logging


def custom_logger(name):
    # Create a custom logger
    logger = logging.getLogger(name)

    # Set the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    logger.setLevel(logging.DEBUG)

    # Create handlers (console and file)
    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler('app.log')

    # Set levels for each handler
    console_handler.setLevel(logging.DEBUG)
    file_handler.setLevel(logging.INFO)

    # Define log format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Attach formatter to handlers
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Attach handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)


    return logger
