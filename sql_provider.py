import re
from psycopg2 import sql
import pandas as pd
import numpy as np

from jptranslations_provider import is_japanese

# CSV data types to PostgreSQL data types
# TYPE_MAP = {
#     "int32": "INTEGER",
#     "int64": "BIGINT",
#     "uint16": "SMALLINT",
#     "byte": "SMALLINT",  # PostgreSQL does not have a byte type, so using SMALLINT here instead..
#     "str": "VARCHAR",
#     "float32": "REAL",
#     "float64": "DOUBLE PRECISION",
#     "bool": "BOOLEAN",
#     "datetime": "TIMESTAMP"
# }


def sanitize_column_name(col_name):
    if col_name and col_name[0].isalnum():
        col_name = '_' + col_name
    col_name = re.sub(r'^\d', r'_\g<0>', col_name)
    col_name = re.sub(r'\W', '_', col_name)
    return col_name


# def map_data_type(csv_type):
#     return TYPE_MAP.get(csv_type, "VARCHAR")  # Default to VARCHAR for unknown types


def map_data_type(csv_type):
    """Maps the data types from CSV to PostgreSQL"""
    # if isinstance(csv_type, int):
    #     return 'INTEGER'
    # elif isinstance(csv_type, float):
    #     return 'FLOAT'
    # elif isinstance(csv_type, str):
    #     return 'TEXT'
    # else:
    #     return 'TEXT'
    return 'TEXT'


def create_table_from_df(df, table_name, conn):
    cursor = conn.cursor()
    print(f"Creating table: {table_name}")
    data_types = df.iloc[2].tolist()
    sanitized_columns = [sanitize_column_name(col) for col in df.columns]
    print(f"Sanitized columns: {sanitized_columns}")

    column_definitions = []
    for i, column in enumerate(sanitized_columns):
        column_type = map_data_type(data_types[i])
        column_definitions.append(f"{column} {column_type}")
    print(f"Column definitions: {column_definitions}")

    drop_table_query = sql.SQL(f"DROP TABLE IF EXISTS {table_name} CASCADE;")
    columns_sql = ', '.join(column_definitions)
    create_table_query = sql.SQL(f"""
        CREATE TABLE {table_name} (
            {columns_sql}
        )
    """)
    print(f"Executing DROP TABLE: {drop_table_query.as_string(conn)}")
    cursor.execute(drop_table_query)
    print(f"Executing CREATE TABLE: {create_table_query.as_string(conn)}")
    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    print(f"Table {table_name} created successfully.")


def insert_data_from_df(df, table_name, conn):
    cursor = conn.cursor()
    sanitized_columns = [sanitize_column_name(col) for col in df.columns]
    print(f"Sanitized columns for insert: {sanitized_columns}")

    columns_sql = ', '.join(sanitized_columns)
    values_sql = ', '.join([f"%({col})s" for col in sanitized_columns])
    insert_query = sql.SQL(f"""
        INSERT INTO {table_name} ({columns_sql}) 
        VALUES ({values_sql})
    """)
    print(f"Insert query: {insert_query.as_string(conn)}")

    for index, row in df.iterrows():
        row_dict = {sanitize_column_name(col): row[col] for col in df.columns}
        #  debugging
        print(f"Inserting row {index}:")
        for col, value in row_dict.items():
            print(f"  Column '{col}': {value}")
        cursor.execute(insert_query, row_dict)

    conn.commit()
    cursor.close()
    print(f"Data inserted into {table_name}.")


def sanitize_column_name_for_db(col_name):
    """Sanitize the column name for the database (remove first underscore) and quote numbers or invalid names."""
    # Remove first underscore and quote columns like numbers or SQL reserved keywords
    if col_name.startswith('_'):
        col_name = col_name[1:]  # Remove the first underscore
    # Quote column names if they are non-standard (like numbers or SQL reserved keywords)
    return f'"{col_name}"' if col_name.isdigit() else col_name


def sanitize_columns(df):
    print(f"Sanitizing all columns in dataframe.")
    sanitized = {col: sanitize_column_name_for_db(col) for col in df.columns}
    print(f"Sanitized columns map: {sanitized}")
    return sanitized


def create_insert_query(df, table_name, sanitized_columns):
    """Create an SQL insert statement using sanitized column names."""
    columns_sql = ', '.join(sanitized_columns.values())
    values_sql = ', '.join([f"%({col})s" for col in df.columns])

    return sql.SQL(f"""
        INSERT INTO {table_name} ({columns_sql}) 
        VALUES ({values_sql})
    """)


from psycopg2 import sql


def create_update_query(table_name, sanitized_columns, japanese_columns, df):
    """Create an SQL update query for rows containing Japanese text."""

    sanitized_columns_no_quotes = {key: value.replace('"', '') for key, value in sanitized_columns.items()}
    sanitized_columns_no_quotes = {key: ('_' + value if value == 'key' else value)
                                   for key, value in sanitized_columns_no_quotes.items()}
    set_clause = ', '.join([f'"_{sanitized_columns_no_quotes[col]}_JP" = %({col})s' for col in japanese_columns])
    where_column = df.columns[0]
    where_clause = f'"{sanitized_columns_no_quotes[where_column]}" = %({where_column})s'

    query_string = f"""
        UPDATE {table_name} 
        SET {set_clause}
        WHERE {where_clause}
    """

    # Print query for debugging
    print(query_string)

    update_query = sql.SQL(query_string)

    return update_query


def check_japanese_columns(row, df):
    """Check if any column contains Japanese text and print debug information."""
    japanese_columns = []
    for col in df.columns:
        cell_content = row[col]
        if is_japanese(cell_content):
            print(f"(CSV) Detected Japanese text in column '{col}': {cell_content}")
            japanese_columns.append(col)
    return japanese_columns


def add_japanese_columns_if_needed(cursor, table_name, sanitized_columns, japanese_columns):
    """Add Japanese columns to the table if they don't exist."""
    print(f"cursor: {cursor}")
    print(f"table name: {table_name}")
    print(f"sanitized columns: {sanitized_columns}")
    print(f"japanese columns: {japanese_columns}")

    table_name_lower = table_name.lower()

    existing_columns_query = f"""
    SELECT column_name
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE table_name = '{table_name_lower}'
    """
    cursor.execute(existing_columns_query)
    existing_columns = cursor.fetchall()

    if not existing_columns:
        raise ValueError(f"Error: Table '{table_name}' has no existing columns or does not exist.")

    print(f"\nExisting columns in {table_name} before modification:")
    for column in existing_columns:
        print(f"  - {column[0]}")

    # Loop through each Japanese column
    for col in japanese_columns:
        column_name = sanitized_columns[col]
        column_name = column_name.replace('"', '')  # Clean up the column name
        column_name_jp = f"_{column_name}_JP"  # Japanese dupe for column name

        print(f"\nChecking if '{column_name_jp}' exists in {table_name}...")

        # Check if the Japanese column already exists in the table
        check_column_query = f"""
        SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE table_name = '{table_name_lower}' AND column_name = '{column_name_jp}'
        """
        cursor.execute(check_column_query)
        column_exists = cursor.fetchone()

        if not column_exists:
            # ALTER TABLE statement to add the Japanese column
            alter_table_query = f"""
            ALTER TABLE "{table_name_lower}"
            ADD COLUMN "{column_name_jp}" TEXT
            """
            print(f"\n  sql: {alter_table_query}")

            cursor.execute(alter_table_query)
        else:
            print(f"Column '{column_name_jp}' already exists in table '{table_name}'")

    cursor.execute(existing_columns_query)
    updated_columns = cursor.fetchall()

    print(f"\nExisting columns in {table_name} after modification:")
    for column in updated_columns:
        print(f"  - {column[0]}")


def insert_or_update_row(cursor, row, df, table_name, sanitized_columns, insert_query):
    """Insert or update a single row depending on whether Japanese text is found."""
    japanese_columns = check_japanese_columns(row, df)
    row_dict = {sanitize_column_name(col): row[col] for col in df.columns}
    row_dict_unsanitized = {col: row[col] for col in df.columns}

    row_index = row.name
    found_japanese_text = []

    if japanese_columns:
        for col in japanese_columns:
            sanitized_col = sanitize_column_name(col)
            row_dict[f"{sanitized_col}_JP"] = row[col]
            japanese_text = row[col]
            found_japanese_text.append((col, row_index, japanese_text))

        for col, index, text in found_japanese_text:
            print(f"Found Japanese text in: \n     column '{col}'\n    row '{index}'\n    text: '{text}'")

        add_japanese_columns_if_needed(cursor, table_name, sanitized_columns, japanese_columns)

        update_query = create_update_query(table_name, sanitized_columns, japanese_columns, df)
        print("Row Dict:", row_dict_unsanitized)
        cursor.execute(update_query, row_dict_unsanitized)
        # cursor.execute(update_query)
    else:
        print(f"Skipping row without Japanese text (row index {row_index}): {row.to_dict()}")


def insert_data_from_df_with_japanese(df, table_name, conn):
    cursor = conn.cursor()
    sanitized_columns = sanitize_columns(df)
    print(f"Sanitized columns for Japanese check: {sanitized_columns}")

    insert_query = create_insert_query(df, table_name, sanitized_columns)
    print(f"Insert query with Japanese columns: {insert_query.as_string(conn)}")

    for _, row in df.iterrows():
        if str(row[df.columns[0]]).startswith('#'):
            print(f"Skipping row with # in first column: {row[df.columns[0]]}")
            continue
        insert_or_update_row(cursor, row, df, table_name, sanitized_columns, insert_query)

    conn.commit()
    cursor.close()
    print(f"Data with Japanese text handled for {table_name}.")
