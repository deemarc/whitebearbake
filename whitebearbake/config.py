from whitebearbake import defaults
import os
# Instantiate config object with defaults
defualt_cfg = {key: getattr(defaults, key) for key in dir(defaults) if key.isupper()}

config = {}
for key,value in defualt_cfg.items():
    config[key] = os.environ.get(key) or value