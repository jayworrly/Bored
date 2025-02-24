import sqlite3
import matplotlib.pyplot as plt
import unittest
import os
import numpy as np
from sklearn.linear_model import LinearRegression

def calculate_predictability(db_name, target_name, runs=2000, picks_per_run=10):
    # Connect to the database
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # Query to get total counts
    c.execute('SELECT SUM(total_count) FROM counts')
    total_target_count = c.fetchone()[0] or 0  # Total times target was picked

    # Calculate total picks
    total_picks = runs * picks_per_run

    # Calculate probability
    if total_picks > 0:
        probability = (total_target_count / total_picks) * 100  # Convert to percentage
    else:
        probability = 0

    # Close the database connection
    conn.close()

    return total_target_count, total_picks, probability

def visualize_data(total_target_count, total_picks, target_name):
    # Calculate percentages
    target_percentage = (total_target_count / total_picks) * 100 if total_picks > 0 else 0
    total_percentage = 100  # Total picks is always 100%

    # Create a simple bar chart to visualize the data
    labels = [f'{target_name} Picks', 'Total Picks']
    values = [target_percentage, total_percentage]

    plt.bar(labels, values, color=['blue', 'orange'])
    plt.ylabel('Percentage (%)')
    plt.title(f'Predictability of {target_name} Being Picked')
    plt.ylim(0, 110)  # Set y-axis limit to 110% for better visualization
    plt.show()

def perform_regression_analysis(db_name, target_name):
    # Connect to the database
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # Query to get all entries in the counts table
    c.execute('SELECT run_count, total_count FROM counts')
    data = c.fetchall()

    # Prepare data for regression
    runs = np.array([row[0] for row in data]).reshape(-1, 1)  # Reshape for sklearn
    counts = np.array([row[1] for row in data])

    # Create and fit the model
    model = LinearRegression()
    model.fit(runs, counts)

    # Make predictions
    predicted_counts = model.predict(runs)

    # Plotting
    plt.scatter(runs, counts, color='blue', label='Actual Counts')
    plt.plot(runs, predicted_counts, color='red', label='Regression Line')
    plt.xlabel('Number of Runs')
    plt.ylabel(f'{target_name} Picks')
    plt.title(f'Regression Analysis of {target_name} Picks')
    plt.legend()
    plt.show()

    # Close the database connection
    conn.close()

class TestPredictability(unittest.TestCase):
    def setUp(self):
        # Create a test database
        self.db_name = 'test_stats.db'
        self.test_runs = 2000
        self.test_count = 1187
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('''
        CREATE TABLE IF NOT EXISTS counts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_count INTEGER,
            total_count INTEGER
        )
        ''')
        # Insert test data
        c.execute('INSERT INTO counts (run_count, total_count) VALUES (?, ?)', 
                 (self.test_runs, self.test_count))
        conn.commit()
        conn.close()

    def test_calculate_predictability(self):
        total_count, total_picks, probability = calculate_predictability(
            self.db_name, "TestName", self.test_runs)
        self.assertEqual(total_count, self.test_count)
        self.assertEqual(total_picks, 20000)
        self.assertAlmostEqual(probability, 5.935, places=3)  # Check if probability is approximately 5.935%

    def tearDown(self):
        # Remove the test database after tests
        os.remove(self.db_name)

# Example usage
if __name__ == "__main__":
    db_name = 'stats.db'  # Specify your database name
    target_name = 'TargetName'  # Specify your target name
    runs = 2000  # Specify number of runs
    
    total_count, total_picks, probability = calculate_predictability(
        db_name, target_name, runs)

    print(f"'{target_name}' was picked a total of {total_count} times.")
    print(f"Total picks: {total_picks}")
    print(f"Probability of picking '{target_name}': {probability:.2f}%")

    # Visualize the data
    visualize_data(total_count, total_picks, target_name)

    # Perform regression analysis
    perform_regression_analysis(db_name, target_name)

    unittest.main()
