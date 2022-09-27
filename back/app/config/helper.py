import configparser

def read_config():
    config = configparser.ConfigParser()
    config.read('app/config/configurations.ini')
    return config