import psycopg2
import os


class Schema:
    def __init__(self):
        self.conn = self.get_connection()
        self.create_to_do_table()
        # Why are we calling user table before to_do table
        # what happens if we swap them?

    def get_connection(self):
        return psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            database=os.getenv('DB_NAME', 'todoapp'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', 'password'),
            port=os.getenv('DB_PORT', '5432')
        )

    def __del__(self):
        # body of destructor
        if hasattr(self, 'conn'):
            self.conn.commit()
            self.conn.close()

    def create_to_do_table(self):

        query = """
        CREATE TABLE IF NOT EXISTS "Todo" (
          "id" SERIAL PRIMARY KEY,
          "Title" TEXT,
          "Description" TEXT,
          "_is_deleted" boolean DEFAULT FALSE,
          "CreatedOn" Date DEFAULT CURRENT_DATE,
          "DueDate" Date
        );

        """

        cur = self.conn.cursor()
        cur.execute(query)
        cur.close()
#Schema Ends


class ToDoModel:
    def __init__(self):
        self.conn = self.get_connection()

    def get_connection(self):
        return psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            database=os.getenv('DB_NAME', 'todoapp'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', 'password'),
            port=os.getenv('DB_PORT', '5432')
        )

    def __del__(self):
        # body of destructor
        if hasattr(self, 'conn'):
            self.conn.commit()
            self.conn.close()

    def list_items(self, where_clause=""):
        query='''select * from "Todo" where _is_deleted != true'''+where_clause
        #print (query)
        cur = self.conn.cursor()
        cur.execute(query)
        columns = [desc[0] for desc in cur.description]
        result_set = cur.fetchall()
        # Convert to list of dictionaries for compatibility with template
        return [dict(zip(columns, row)) for row in result_set]

    def sql_edit_insert(self,var):
        #print(var)
        # Validate and format the date
        title, description, due_date = var
        if due_date and due_date.strip():
            try:
                # Try to parse the date to validate it
                from datetime import datetime
                datetime.strptime(due_date, '%Y-%m-%d')
            except ValueError:
                # If invalid date format, set to None
                due_date = None
        else:
            due_date = None
            
        query='''insert into "Todo"("Title","Description","DueDate") values (%s,%s,%s)'''
        cur = self.conn.cursor()
        cur.execute(query,(title, description, due_date))
        self.conn.commit()
        
    def sql_delete(self,ID):
        print("Inside sql_delete",ID)
        print("Type",type(ID))
        query='''UPDATE "Todo" SET _is_deleted=1 where id=%s'''
        print("Query",query)
        cur = self.conn.cursor()
        cur.execute(query,ID)
        self.conn.commit()  

    def sql_edit(self,var):
        # Validate and format the date
        title, description, due_date, old_id = var
        if due_date and due_date.strip():
            try:
                # Try to parse the date to validate it
                from datetime import datetime
                datetime.strptime(due_date, '%Y-%m-%d')
            except ValueError:
                # If invalid date format, set to None
                due_date = None
        else:
            due_date = None
            
        query='''UPDATE "Todo" SET "Title"=%s,"Description"=%s,"DueDate"=%s where id=%s'''
        cur = self.conn.cursor()
        cur.execute(query,(title, description, due_date, old_id))
        self.conn.commit()      
    

#end TodoModel
