import sqlite3

def get_total_count(db_name):
    # Connect to the database
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # Query to get the total count
    c.execute('SELECT SUM(total_count) FROM counts')
    total_count = c.fetchone()[0]  # Fetch the result

    # Close the database connection
    conn.close()

    return total_count if total_count is not None else 0  # Return 0 if no records found

def print_counts(db_name):
    # Connect to the database
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # Query to get all entries in the counts table
    c.execute('SELECT * FROM counts')
    rows = c.fetchall()

    # Print each row
    for row in rows:
        print(row)

    # Close the database connection
    conn.close()

# Example usage
if __name__ == "__main__":
    db_name = 'stats_20000_runs.db'  # Specify the database name
    total_count = get_total_count(db_name)
    print(f"Total picks: {total_count}")
    print_counts(db_name)
