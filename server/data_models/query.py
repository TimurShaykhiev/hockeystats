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
        """
        'columns' is a list of column names. Column name must have '-' at the beginning if descending order is needed.
        """
        self.query += ' ORDER BY '
        for col in columns:
            if col[0] == '-':
                self.query += col[1:] + ' DESC, '
            else:
                self.query += col + ', '
        self.query = self.query[:-2]
        return self

    def limit(self, row_number):
        self.query += ' LIMIT {}'.format(row_number)
        return self

    @staticmethod
    def get_col_list(columns, table_alias=None):
        if columns is None:
            return '*'
        if table_alias is None:
            return ', '.join(columns)
        return ', '.join(['{}.{}'.format(table_alias, c) for c in columns])
