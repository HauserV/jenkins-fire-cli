from .config import Config
from fire import Fire


config = Config()
config._init()


if __name__ == '__main__':
    Fire(dict(
        config=config,
    ))