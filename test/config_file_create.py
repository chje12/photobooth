from configparser import ConfigParser
config = ConfigParser()
config['settings'] = {
    'debug': 'true',
    'secret_key': 'abc123',
    'log_path': '/my_app/log'
}

config['db'] = {
    'db_name': 'myapp_dev',
    'db_host': 'localhost',
    'db_port': '8889'
}

config['files'] = {
    'use_cdn': 'false',
    'images_path': '/my_app/images'
}
with open('./config.ini', 'w') as f:
      config.write(f)