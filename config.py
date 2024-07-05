from dotenv import load_dotenv


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Config(metaclass=SingletonMeta):
    def __init__(self):
        """Initialize the config class."""
        load_dotenv()

        self.gpt_4_turbo = 'gpt-4-1106-preview'
        self.gpt_4_vision = 'gpt-4'
        self.gpt_40 = 'gpt-4o-2024-05-13'
        self.gpt_4_32k = 'gpt-4-32k'


        
