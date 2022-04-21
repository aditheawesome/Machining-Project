# This file contains necessary functions to execute SQL queries that are projected from injection attacks
# Each function takes in a SQLite Connection object, the table, and any columns or conditions
# import sqlite3
# connection = sqlite3.connect("database.db", check_same_thread=False)

# Connection, Object, Object, Tuple
def insert(conn, table, columns, col_info):
    # SQLCursor
    c = conn.cursor();
    # Tuple
    col_info = tuple_maker(col_info);
    # String
    query = "insert into {tbl} {col} values ".format(tbl=table, col=columns);
    query = qmark_concatenator(query, col_info);
    with conn:
        c.execute(query, col_info);


# Connection, String, Tuple, Tuple
def delete(conn, table, conditions, cond_info):
    # SQLCursor
    c = conn.cursor();
    # Tuple
    cond_info = tuple_maker(cond_info);
    # String
    query = "delete from {tbl} where ".format(tbl=table);
    query = condition_concatenator(query, tuple_maker(conditions));
    with conn:
        c.execute(query, cond_info);

# Connection, Object, Object, Tuple, Tuple
def select(conn, table, column, conditions, cond_info):
    # SQLCursor
    c = conn.cursor();
    # Tuple
    cond_info = tuple_maker(cond_info);
    # String
    query = "select {col} from {tbl} where ".format(col=column, tbl=table);
    query = condition_concatenator(query, tuple_maker(conditions));
    with conn:
        return c.execute(query, cond_info);

# Connection, Object, Tuple, Tuple
def select_all(conn, table, conditions, cond_info):
    # SQLCursor
    c = conn.cursor();
    # Tuple
    cond_info = tuple_maker(cond_info);
    # String
    query = "select * from {tbl} where ".format(tbl=table);
    query = condition_concatenator(query, tuple_maker(conditions));
    with conn:
        return c.execute(query, cond_info);


# this can only update one column at a time
# if you need to update multiple columns, call it multiple times for now
# Connection, Object, Object, Tuple, Tuple, Tuple;
def update(conn, table, column, new_col_info, conditions, cond_info):
    c = conn.cursor();
    query = "update {tbl} set {col} = ? where ".format(tbl=table, col=column);
    query = condition_concatenator(query, tuple_maker(conditions));
    args = (new_col_info, cond_info);
    with conn:
        c.execute(query, args);


def qmark_concatenator(query, parameters):
    query += "("
    for x in range(len(parameters)):
        query += "?, "
    query = query[:-2] + ")"
    return query


def condition_concatenator(query, columns):
    for column in columns:
        query += "{col} = ? and ".format(col=column);
    query = query[:-5];
    return query;

# Tuple || List
def tuple_maker(parameters): #Tuple
    if type(parameters) in [list, tuple]:
        return tuple(parameters);
    else:
        return tuple([parameters]);

#print(select(connection, "builder", "email_address", 2, 2).fetchall())