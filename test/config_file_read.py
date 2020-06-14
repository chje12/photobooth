from configparser import ConfigParser

parser = ConfigParser()
parser.read('config.ini')
print(parser.sections())  # ['settings', 'db', 'files']
print(parser.get('settings', 'secret_key'))  # abc123
print(parser.options('settings'))  # ['debug', 'secret_key', 'log_path']
print('db' in parser)  # True
print(parser.get('db', 'db_port'), type(parser.get('db', 'db_port')))  # 8889 <class 'str'>
print(int(parser.get('db', 'db_port')))  # 8889 (as int)
print(parser.getint('db', 'db_default_port', fallback=3306))  # 3306
print(parser.getboolean('settings', 'debug', fallback=False))  # True