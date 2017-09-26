# coding=utf-8
import MySQLdb


class Connection(object):
    def __init__(self):
        self.conn = self.connect()

    def connect(self):
        conn = MySQLdb.connect(host='127.0.0.1', port=33060, user='homestead',
                               passwd='secret', db='caikes',
                               charset='utf8')
        return conn


class DB(object):
    def __init__(self, conn):
        self.primary = None

        self.table = None

        self.connect = conn

        self.cursor = self.connect.cursor()

        self.__wheres = []

    def find(self, id, column=['*']):
        """
        单个查询
        :param id:
        :param column:
        :return:
        """
        sql = "SELECT %s from %s where %s = %d" % (','.join(column), self.table, self.primary, int(id))
        print sql
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def where(self, column, operator, value, boolean='and'):
        """
        mysql where语句
        :rtype: object
        """
        self.__wheres.append({'column': column, 'operator': operator, 'value': value, 'boolean': boolean})
        return self

    def between(self, column, value=[]):
        """
        mysql between语句
        :rtype: object
        """
        self.__wheres.append({{'column': column, 'value': value, 'method': 'BETWEEN'}})
        return self

    def get(self, column=['*']):
        """
        多条查询
        :rtype: object
        """
        sql = self.schema(column)
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def first(self, column=['*']):
        """
        单条查询
        :rtype: object
        """
        sql = self.schema(column)
        sql += 'LIMIT 1 OFFSET  0'
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def insert(self, column, value=None):
        sql = "INSERT INTO `%s`(%s) VALUES(%s)" % (self.table, '`,`'.join(column), ','.join(["%s" for x in value if x]))
        self.cursor.execute(sql, value)
        # self.connect.commit()

    def schema(self, column):
        """
        查询语法解析
        :rtype: object
        """
        i = 0
        sql = "SELECT %s FROM `%s` " % ('`,`'.join(column), self.table)
        for x in self.__wheres:
            if i == 0:
                sql += "WHERE `%s` %s '%s' " % (x['column'], x['operator'], x['value'])
            else:
                sql += "%s `%s` %s '%s' " % (x['boolean'], x['column'], x['operator'], str(x['value']))
            i = +1
        return sql

    def __del__(self):
        self.connect.close()


class Model(dict):
    def __init__(self, **kwargs):

        self.table = None

        self.primary = "id"

        self.db = DB(Connection().connect())

        super(Model, self).__init__(**kwargs)

    def save(self):
        fill = []
        value = []
        for field in self:
            if field not in {'table', 'primary', 'db'}:
                fill.append(field)
                value.append(self.get(field))
        self.db.table = self.table
        self.db.insert(fill, value)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value
