import random
import sqlite3
import os

def create_database(db_name):
    # Initialize the database
    conn = sqlite3.connect(db_name)  # Create or open a database file
    c = conn.cursor()

    # Create a table to store the counts if it doesn't exist
    c.execute('''
    CREATE TABLE IF NOT EXISTS counts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        run_count INTEGER,
        total_count INTEGER
    )
    ''')
    return conn, c

def random_name_picker(names, target_name, runs):
    total_count = 0  # Total counter for target name
    
    for _ in range(runs):  # Repeat the process for the specified number of runs
        run_count = 0  # Counter for this run
        shuffled_names = random.sample(names, len(names))  # Shuffle names without repetition
        for name in shuffled_names[:10]:  # Pick the first 10 names
            print(name)
            if name == target_name:
                run_count += 1  # Increment the counter if target name is picked

        total_count += run_count  # Update the total count
        print(f"'{target_name}' was picked {run_count} times in this run.")  # Output the count for this run

    return total_count  # Return the total count for all runs

# Example usage
names_list = [
]

# Specify the number of runs and target name
num_runs = 20000  # Set to 20000 runs
target_name = ""  # Set your target name here
db_name = f'name_stats_{num_runs}_runs.db'  # Create a unique database name
conn, c = create_database(db_name)

# Run the random name picker and get the total count
total_count = random_name_picker(names_list, target_name, num_runs)

# Store the counts in the database
c.execute('INSERT INTO counts (run_count, total_count) VALUES (?, ?)', (num_runs, total_count))
conn.commit()  # Save (commit) the changes

# Close the database connection when done
conn.close()