from configparser import ConfigParser


class App(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
            cls._instance.config = ConfigParser()
            cls._instance.config.read('./config/config.ini', 'UTF-8')

        return cls._instance
