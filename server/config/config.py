import os

import config


def get_custom_config():
    """Read custom settings from file and update config variables in the config module."""
    config_path = os.environ.get('HOCKEYSTATS_CONFIG')
    if config_path is not None:
        try:
            with open(config_path, mode='rb') as config_file:
                exec(compile(config_file.read(), config_path, 'exec'), config.__dict__)
        except Exception:
            pass
    return config
