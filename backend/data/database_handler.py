import sqlite3
import os

class DatabaseConnection:


    """
        This Class fetches content from the bellary SQLite DB
    """

    def __init__(self):
        path = os.path.abspath('backend/data/bellary.db');
        self.conn = sqlite3.connect(path);

    def select_table_detail(self,sql):

        # Select the contents of the sqlite table

        cursor = self.conn.cursor();
        cursor_data = cursor.execute(sql);
        data = cursor.fetchall();
        self.conn.close;
        return data

    def insert_table_detail(self,sql,args):
        # Insert into sqlite table

        cursor = self.conn.cursor();

        try:
            cursor_data = cursor.execute(sql,args);
            self.conn.commit();
            self.conn.close;
            message = "Fertilizer Add completed successfully"
        except sqlite3.IntegrityError:
            message = "Fertilizer to be added already exists"

        return message
