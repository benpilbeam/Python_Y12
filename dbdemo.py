import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file) #The database will be created if it does not exist
        return conn
    except Error as e:
        print(e)
 
    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def create_project(conn, project):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO projects(name,begin_date,end_date)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    return cur.lastrowid

def create_task(conn, task):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """
 
    sql = ''' INSERT INTO tasks(name,priority,status_id,project_id,begin_date,end_date)
              VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    return cur.lastrowid


def select_all_tasks(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks")
 
    rows = cur.fetchall()
 
    for row in rows:
        print(row)


def select_task_by_priority(conn, priority):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks WHERE priority=?", (priority,))
 
    rows = cur.fetchall()
 
    for row in rows:
        print(row)

def delete_a_task(conn, id):
    """
    Delete a task by id
    :param conn: the Connection object
    :param id:
    :return:
    """

    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id=?",(id,))
    conn.commit()

def update_a_task(conn, id, name):
    """
    Update a task by id
    :param conn: the Connection object
    :param id:
    :return:
    """
    
    cur = conn.cursor()
    cur.execute("UPDATE tasks SET name = ? WHERE id=?",(name,id))
        
def main():
    database = r"dbtest3.db"
 
    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS projects (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        begin_date text,
                                        end_date text
                                    ); """
 
    sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    priority integer,
                                    status_id integer NOT NULL,
                                    project_id integer NOT NULL,
                                    begin_date text NOT NULL,
                                    end_date text NOT NULL,
                                    FOREIGN KEY (project_id) REFERENCES projects (id)
                                );"""
 
    # create a database connection
    conn = create_connection(database)
 
    # create tables
    if conn is not None:
        
        choice = 99
        
        while choice != 0:
            print ("1 = Create new tables/db")
            print ("2 = Insert data")
            print ("3 = Select data")
            print ("4 = Delete task")
            print ("5 = Update task")
            choice = int(input ("Which Option?"))
            print ("Choice", choice)

            if choice == 1:
                # create projects table
                create_table(conn, sql_create_projects_table)
 
                # create tasks table
                create_table(conn, sql_create_tasks_table)
                
            elif choice == 2:
                with conn:
                    # create a new project
                    project = ('Cool App with SQLite & Python', '2015-01-01', '2015-01-30');
                    project_id = create_project(conn, project)
 
                    # tasks
                    task_1 = ('Analyze the requirements of the app', 2, 1, project_id, '2015-01-01', '2015-01-02')
                    task_2 = ('Confirm with user about the top requirements', 3, 1, project_id, '2015-01-03', '2015-01-05')
 
                    # create tasks
                    create_task(conn, task_1)
                    create_task(conn, task_2)
                
            elif choice == 3:
                with conn:
                    print("1. Query task by priority:")
                    select_task_by_priority(conn, 1)
 
                    print("2. Query all tasks")
                    select_all_tasks(conn)

            elif choice == 5:
                taskId = int(input("Which id?"))
                newName = str(input("What is the new name?"))
                update_a_task(conn, taskId, newName)

            elif choice == 4:  
                with conn:
                    taskId = int(input("Which id?"))
                    delete_a_task(conn, taskId)
                                 
            elif choice == 0:
                print ("Bye")

                #Close the database connection when finished
                if conn:
                    conn.close()
                
            else:
                print("Invalid option")
    else:
        print("Error! cannot create the database connection.")



main()
