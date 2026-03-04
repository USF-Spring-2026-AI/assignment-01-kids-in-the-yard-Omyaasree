from Person import Person
import pandas as pd
import random

class PersonFactory:
    def __init__(self):
        # read all teh necessary files 
        # life_expectancy, first names, last names and probabilty of gender , rank to probability
        self.life_expectancy_df = pd.read_csv('life_expectancy.csv')
        self.first_names_df = pd.read_csv('first_names.csv')
        self.gender_prob_df = pd.read_csv('gender_name_probability.csv')
        self.last_names_df = pd.read_csv('last_names.csv')
        self.birth_marriage_rates_df = pd.read_csv('birth_and_marriage_rates.csv')
        rank_to_prob_df = pd.read_csv('rank_to_probability.csv')



        self.last_name_weights = []

        # Convert column headers to float weights for use in weighted random selection
        for p in rank_to_prob_df.columns:
            probability_value = float(p)
            self.last_name_weights.append(probability_value)

    def manual_weighted_choice(self, items, weights):
        if weights == []:
            if items == []:
                return None
            return random.choice(items)

        # Accumulate weights to create a range for the target random number
        total_weight = 0
        for w in weights:
            total_weight = total_weight + w

        target_number = random.uniform(0, total_weight)
        # find which interval the target number falls into
        running_total = 0
        for i in range(len(items)):
            current_item_weight = weights[i]
            running_total = running_total + current_item_weight
            
            if running_total >= target_number:
                return items[i]

        last_position = len(items) - 1

        return items[last_position]

    def get_decade_string(self, year):
        if year < 1950: year = 1950
        if year > 2120: year = 2120

        result = (year // 10) * 10

        return f"{result}s"

    def determine_gender(self, decade):
        # Randomly assigns a gender; can be expanded for specific CSV probabilities.
        return random.choice(['male', 'female'])

    def get_random_first_name(self, decade, gender):
        # Filters names by decade and gender to pick a name based on frequency weights
        names_for_decade = self.first_names_df[
            (self.first_names_df['decade'] == decade) & 
            (self.first_names_df['gender'] == gender)
        ]
        names = names_for_decade['name'].tolist()
        weights = names_for_decade['frequency'].tolist()
        
        return self.manual_weighted_choice(names, weights)

    def get_random_last_name(self, decade):
        names_for_decade = self.last_names_df[self.last_names_df['Decade'] == decade]
        names = names_for_decade['LastName'].tolist()

        return self.manual_weighted_choice(names, self.last_name_weights)

    def get_life_expectancy(self, year_born):
        # Apply the required +/- 10 year random variation
        row = self.life_expectancy_df[self.life_expectancy_df['Year'] == year_born]
        if row.empty:
            base_expectancy = 80.0 
        else:
            base_expectancy = row['Period life expectancy at birth'].values[0]
        
        random_offset = random.randint(-10, 10)

        lifespan = base_expectancy + random_offset

        year_died = int(year_born + lifespan)   

        return year_died

    def create_person(self, year_born, last_name=None, gender=None):
            decade = self.get_decade_string(year_born)
            if not gender:
                gender = self.determine_gender(decade)

            first_name = self.get_random_first_name(decade, gender)
            
            # If no last name is provided (e.g., root people), pull from random list
            if not last_name:
                last_name = self.get_random_last_name(decade)

            new_person = Person(first_name, last_name, year_born, 0, gender)
            # Initialize person and update year_died using the defined setter

            year_died = self.get_life_expectancy(year_born)
            new_person.year_died = year_died 
            
            return new_person