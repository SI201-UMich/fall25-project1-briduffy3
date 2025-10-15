import pandas as pd
import unittest

csv_file = 'penguins.csv'
df = pd.read_csv(csv_file)


print(df.columns.tolist())
print(df.iloc[0]) 
print(len(df))

class Proj1test(unittest.TestCase):

    def setUp(self):
        pass

    def test_avg_body_mass_general(self):
        data = {
            'species': ['Adelie', 'Adelie'],
            'island': ['Torgersen', 'Torgersen'],
            'body_mass_g': [3700, 3800],
            'sex': ['male', 'female']
        }
        df = pd.DataFrame(data)
        result = calc_avg_body_mass_by_island_species_sex(df)
        self.assertEqual(result[('Torgersen', 'Adelie', 'male')], 3700)
        self.assertEqual(result[('Torgersen', 'Adelie', 'female')], 3800)

    def test_percentage_bill_length_general(self):
        data = {
            'species': ['Adelie', 'Adelie', 'Adelie'],
            'island': ['Torgersen', 'Torgersen', 'Torgersen'],
            'bill_length_mm': [41, 39, 45],
            'sex': ['male', 'female', 'male']
        }
        df = pd.DataFrame(data)
        result = calc_percent_long_bills_per_island(df, threshold=40)
        self.assertAlmostEqual(result['Torgersen'], 2/3*100)

    # edge case 1
    def test_avg_body_mass_missing_values(self):
        data = {
            'species': ['Adelie', 'Adelie'],
            'island': ['Dream', 'Dream'],
            'body_mass_g': [3700, None],
            'sex': ['female', 'female']
        }
        df = pd.DataFrame(data)
        result = calc_avg_body_mass_by_island_species_sex(df)
        self.assertEqual(result[('Dream', 'Adelie', 'female')], 3700)

    # Edge case 2
    def test_percentage_bill_length_missing(self):
        data = {
            'species': ['Adelie', 'Adelie'],
            'island': ['Biscoe', 'Biscoe'],
            'bill_length_mm': [None, 41],
            'sex': ['male', 'female']
        }
        df = pd.DataFrame(data)
        result = calc_percent_long_bills_per_island(df, threshold=40)
        self.assertEqual(result['Biscoe'], 100.0)