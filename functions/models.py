import psycopg2
import os
from datetime import datetime

class Schema:
    def __init__(self):
        self.conn = self.get_connection()
        self.create_to_do_table()

    def get_connection(self):
        return psycopg2.connect(
            host=os.getenv("DB_HOST", "db"),
            database=os.getenv("DB_NAME", "todoapp"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "password"),
            port=os.getenv("DB_PORT", "5432")
        )

    def __del__(self):
        if hasattr(self, 'conn') and self.conn:
            self.conn.commit()
            self.conn.close()

    def create_to_do_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS "Todo" (
            "id" SERIAL PRIMARY KEY,
            "Title" TEXT,
            "Description" TEXT,
            "_is_deleted" BOOLEAN DEFAULT FALSE,
            "CreatedOn" DATE DEFAULT CURRENT_DATE,
            "DueDate" DATE
        );
        """
        cur = self.conn.cursor()
        cur.execute(query)
        cur.close()

# ---------------- ToDoModel -----------------

class ToDoModel:
    def __init__(self):
        self.conn = self.get_connection()

    def get_connection(self):
        return psycopg2.connect(
            host=os.getenv("DB_HOST", "db"),
            database=os.getenv("DB_NAME", "todoapp"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "password"),
            port=os.getenv("DB_PORT", "5432")
        )

    def __del__(self):
        if hasattr(self, 'conn') and self.conn:
            self.conn.commit()
            self.conn.close()

    def list_items(self, where_clause=""):
        query = '''SELECT * FROM "Todo" WHERE _is_deleted != TRUE''' + where_clause
        cur = self.conn.cursor()
        cur.execute(query)
        columns = [desc[0] for desc in cur.description]
        result_set = cur.fetchall()
        cur.close()
        return [dict(zip(columns, row)) for row in result_set]

    def sql_edit_insert(self, var):
        title, description, due_date = var

        if due_date and due_date.strip():
            try:
                datetime.strptime(due_date, '%Y-%m-%d')
            except ValueError:
                due_date = None
        else:
            due_date = None

        query = '''INSERT INTO "Todo"("Title", "Description", "DueDate") VALUES (%s, %s, %s)'''
        cur = self.conn.cursor()
        cur.execute(query, (title, description, due_date))
        self.conn.commit()
        cur.close()

    def sql_delete(self, ID):
        query = '''UPDATE "Todo" SET _is_deleted = TRUE WHERE id = %s'''
        cur = self.conn.cursor()
        cur.execute(query, (ID,))
        self.conn.commit()
        cur.close()

    def sql_edit(self, var):
        title, description, due_date, old_id = var

        if due_date and due_date.strip():
            try:
                datetime.strptime(due_date, '%Y-%m-%d')
            except ValueError:
                due_date = None
        else:
            due_date = None

        query = '''UPDATE "Todo" 
                   SET "Title" = %s, "Description" = %s, "DueDate" = %s 
                   WHERE id = %s'''
        cur = self.conn.cursor()
        cur.execute(query, (title, description, due_date, old_id))
        self.conn.commit()
        cur.close()
