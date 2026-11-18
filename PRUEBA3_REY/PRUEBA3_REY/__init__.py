import pymysql
from django.db.backends.base.base import BaseDatabaseWrapper

pymysql.version_info = (2, 2, 1, "final", 0)
pymysql.install_as_MySQLdb()

BaseDatabaseWrapper.check_database_version_supported = lambda self: None



