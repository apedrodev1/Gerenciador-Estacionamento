"""
Database Context Manager.

This module provides the DatabaseManager class for handling
safe and automatic SQLite connection management (commit, rollback, close)
using a 'with' statement.
"""

import sqlite3


class DatabaseManager:
    """
    A context manager for handling SQLite database connections.

    Ensures that connections are opened, foreign keys are enabled,
    transactions are committed or rolled back, and connections
    are closed automatically.
    """

    def __init__(self, db_path: str):
        """
        Initializes the manager with the path to the database.

        Args:
            db_path (str): The file path to the SQLite database.
        """
        self.db_path = db_path
        self.conn = None

    def __enter__(self) -> sqlite3.Connection:
        """
        Opens the database connection and enables foreign keys.

        Returns:
            sqlite3.Connection: The active database connection.
        """
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.execute("PRAGMA foreign_keys = ON;")
            return self.conn
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Closes the connection, committing or rolling back changes.
        """
        if self.conn:
            try:
                if exc_type:  # If an exception occurred
                    print(f"Rolling back changes due to error: {exc_val}")
                    self.conn.rollback()
                else:  # If no exception
                    self.conn.commit()
            except sqlite3.Error as e:
                print(f"Error during __exit__: {e}")
            finally:
                self.conn.close()