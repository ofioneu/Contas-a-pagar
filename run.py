import sys
from app import create_app
from config import app_config, app_active

config = app_config[app_active]
config.APP = create_app(app_active)

print(config.APP)

if __name__ == '__main__':
    config.APP.run(host='0.0.0.0', port=config.PORT_HOST)
    reload(sys)