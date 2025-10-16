# Brian Duffy (solo)
# I used AI to help me write my test cases/figure out what the edge cases should be and to find some ideas for possible calulation although the actual code was written by me.

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

    def test_avg_body_mass_multiple_groups(self):
        data = {
            'species': ['Adelie', 'Adelie', 'Gentoo'],
            'island': ['Torgersen', 'Torgersen', 'Biscoe'],
            'body_mass_g': [3700, 3800, 5000],
            'sex': ['male', 'female', 'male']
        }
        df = pd.DataFrame(data)
        result = calc_avg_body_mass_by_island_species_sex(df)
        self.assertEqual(result[('Biscoe', 'Gentoo', 'male')], 5000)

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

    def test_avg_body_mass_all_missing(self):
        data = {
            'species': ['Adelie', 'Adelie'],
            'island': ['Dream', 'Dream'],
            'body_mass_g': [None, None],
            'sex': ['female', 'female']
        }
        df = pd.DataFrame(data)
        result = calc_avg_body_mass_by_island_species_sex(df)
        self.assertEqual(result, {})

    # calc_percent_long_bills_per_island tests

    def test_percentage_bill_length_general(self):
        data = {
            'species': ['Adelie', 'Adelie', 'Adelie'],
            'island': ['Torgersen', 'Torgersen', 'Torgersen'],
            'bill_length_mm': [41, 39, 45],
            'sex': ['male', 'female', 'male']
        }
        df = pd.DataFrame(data)
        result = calc_percent_long_bills_per_island(df, threshold=40)
        self.assertAlmostEqual(result['Torgersen'], 2 / 3 * 100)

    def test_percentage_bill_length_multiple_islands(self):
        data = {
            'species': ['Adelie', 'Adelie', 'Adelie'],
            'island': ['Biscoe', 'Biscoe', 'Dream'],
            'bill_length_mm': [41, 39, 45],
            'sex': ['male', 'female', 'female']
        }
        df = pd.DataFrame(data)
        result = calc_percent_long_bills_per_island(df, threshold=40)
        self.assertAlmostEqual(result['Biscoe'], 1 / 2 * 100)
        self.assertEqual(result['Dream'], 100.0)

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

    def test_percentage_bill_length_all_missing(self):
        data = {
            'species': ['Adelie', 'Adelie'],
            'island': ['Dream', 'Dream'],
            'bill_length_mm': [None, None],
            'sex': ['female', 'female']
        }
        df = pd.DataFrame(data)
        result = calc_percent_long_bills_per_island(df, threshold=40)
        self.assertEqual(result, {})

# functions

def calc_avg_body_mass_by_island_species_sex(df):
    filtered = df.dropna(subset=['body_mass_g', 'sex', 'species', 'island'])
    groups = filtered.groupby(['island', 'species', 'sex'])['body_mass_g'].mean()
    return groups.to_dict()

def calc_percent_long_bills_per_island(df, threshold=40):
    filtered = df.dropna(subset=['bill_length_mm', 'island'])
    if filtered.empty:
        return {}
    def perc(subdf):
        return (subdf['bill_length_mm'] > threshold).sum() / len(subdf) * 100 if len(subdf) > 0 else 0
    results = filtered.groupby('island').apply(perc)
    return results.to_dict()

    
def write_results_to_txt(avg_mass_dict, percent_long_bill_dict, filename='penguin_analysis.txt'):
    with open(filename, 'w') as f:
        for key, val in avg_mass_dict.items():
            f.write(f"Island: {key[0]}, Species: {key[1]}, Sex: {key[2]} -> Avg Mass: {val:.2f} g\n")
        for key, val in percent_long_bill_dict.items():
            f.write(f"Island: {key} -> {val:.2f}%\n")


if __name__ == '__main__':
    unittest.main()