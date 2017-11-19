class Query:
    """
    This class is a helper for generating simple SQL SELECT queries. It does not have full SQL support.
    """
    def __init__(self, table_name):
        self._table_name = table_name
        self.query = ''

    def select(self, columns=None):
        """'columns' is a list of column names"""
        if columns is None:
            self.query = 'SELECT * FROM {}'.format(self._table_name)
        else:
            self.query = 'SELECT {} FROM {}'.format(', '.join(columns), self._table_name)
        return self

    def where(self, conditions):
        """'conditions' is a string with all WHERE conditions(w/o WHERE keyword) in correct SQL format"""
        self.query += ' WHERE ' + conditions
        return self

    def filter_by(self, columns):
        """'columns' is a list of column names. All columns are used in equal comparison with AND operator"""
        where = ' WHERE {} = %s' + ' AND {} = %s'*(len(columns) - 1)
        self.query += where.format(*columns)
        return self

    def order_by(self, columns):
        """'columns' is a string of column names in correct SQL format"""
        self.query += ' ORDER BY ' + columns
        return self

    def limit(self, row_number):
        self.query += ' LIMIT {}'.format(row_number)
        return self
