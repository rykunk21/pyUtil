import sqlite3

class Database:
  """
  Database provides a convenient interface for interacting with a SQLite database.
  """
  import sqlite3

  def __init__(self, db_file):
    """
    Constructor for the Database class.

    Arguments:
    db_file -- the path to the SQLite database file.
    """
    self.conn = sqlite3.connect(db_file)
    self.cursor = self.conn.cursor()

  def execute(self, query, params=()):
    """
    Execute a SQL query that does not return any data (e.g. INSERT, UPDATE, DELETE).

    Arguments:
    query -- the SQL query to execute.
    params -- a tuple of parameters for the query.
    """
    self.cursor.execute(query, params)
    self.conn.commit()

  def fetchone(self, query, params=()):
    """
    Execute a SQL query that returns a single row of data (e.g. SELECT) and return the first row of the result.

    Arguments:
    query -- the SQL query to execute.
    params -- a tuple of parameters for the query.

    Returns:
    The first row of the result of the query.
    """
    self.cursor.execute(query, params)
    return self.cursor.fetchone()

  def fetchall(self, query, params=()):
    """
    Execute a SQL query that returns multiple rows of data (e.g. SELECT) and return all the rows of the result.

    Arguments:
    query -- the SQL query to execute.
    params -- a tuple of parameters for the query.
    """
    