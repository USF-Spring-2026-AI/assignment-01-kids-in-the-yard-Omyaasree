import pandas as pd
import random
import math

class Person:
    """Represents an individual in the family tree with attributes from Table 1."""
    def __init__(self, first_name, last_name, year_born, gender):
        self.first_name = first_name
        self.last_name = last_name
        self.year_born = year_born
        self.gender = gender
        self.year_died = None
        self.partner = None

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

class PersonFactory:
    """Handles data file reading and probabilistic person generation."""
    def __init__(self):
        self.life_expectancy = None
        self.first_names = None
        self.last_names = None
        self.rates = None
        self.rank_probs = None

    def read_files(self):
        """Reads all required CSV files from the current directory [cite: 27-28]."""
        self.life_expectancy = pd.read_csv('life_expectancy.csv')
        self.first_names = pd.read_csv('first_names.csv')
        self.last_names = pd.read_csv('last_names.csv')
        self.rates = pd.read_csv('birth_and_marriage_rates.csv')
        self.rank_probs = pd.read_csv('rank_to_probability.csv')

    def get_lifespan_year(self, year_born):
        """Calculates Year Died based on decade expectancy +/- 10 years[cite: 32]."""
        decade = (year_born // 10) * 10
        row = self.life_expectancy[self.life_expectancy['year'] == decade]
        avg_life = row['expectancy'].values[0] if not row.empty else 75.0
        return year_born + int(avg_life + random.uniform(-10, 10))

    def create_person(self, year_born, last_name=None, gender=None):
        """Creates a Person with randomized attributes based on data files[cite: 32]."""
        gender = gender or random.choice(['M', 'F'])
        decade = (year_born // 10) * 10
        
        # First Name based on Year and Gender frequency
        potential_names = self.first_names[(self.first_names['year'] == decade) & 
                                          (self.first_names['gender'] == gender)]
        first_name = random.choice(potential_names['name'].tolist()) if not potential_names.empty else "John"
        
        # Last Name logic for non-descendants (partners) [cite: 32]
        if not last_name:
            ranks = self.rank_probs['rank'].tolist()
            weights = self.rank_probs['probability'].tolist()
            chosen_rank = random.choices(ranks, weights=weights, k=1)[0]
            last_name = self.last_names[self.last_names['rank'] == chosen_rank]['name'].values[0]
            
        p = Person(first_name, last_name, year_born, gender)
        p.year_died = self.get_lifespan_year(year_born)
        return p

class FamilyTree:
    """Driver class managing iterative generation and user queries."""
    def __init__(self):
        self.factory = PersonFactory()
        self.all_people = [] # The "array list" tracking every person in the tree [cite: 38]

    def run(self):
        print("Reading files...")
        self.factory.read_files()
        
        print("Generating family tree...")
        # Initialize the first two people born in 1950 [cite: 22, 24]
        p1 = Person("Desmond", "Jones", 1950, "M")
        p2 = Person("Molly", "Jones", 1950, "F")
        p1.year_died = self.factory.get_lifespan_year(1950)
        p2.year_died = self.factory.get_lifespan_year(1950)
        p1.partner = p2
        
        self.all_people.extend([p1, p2])
        
        # Use a queue for iterative processing (Breadth-First Generation)
        queue = [p1] # Track the primary descendant of each couple/unit
        
        while queue:
            parent = queue.pop(0)
            
            # 1. Determine Birth Rate and apply the "Wiggle" 
            decade = (parent.year_born // 10) * 10
            rate_row = self.factory.rates[self.factory.rates['year'] == decade]
            base_rate = rate_row['birth_rate'].values[0] if not rate_row.empty else 2.0
            
            # Calculation: between (rate - 1.5) and (rate + 1.5), rounding up
            min_kids = math.ceil(base_rate - 1.5)
            max_kids = math.ceil(base_rate + 1.5)
            num_children = random.randint(min_kids, max_kids)

            # 2. Distribute child birth years [cite: 34-35]
            if num_children > 0:
                # Years distributed between parent Year Born + 25 and + 45
                child_years = sorted([random.randint(parent.year_born + 25, parent.year_born + 45) 
                                     for _ in range(num_children)])
                
                for b_year in child_years:
                    if b_year > 2120: # Stop if we exceed 2120 
                        continue
                        
                    # Create child (inherits last name)
                    child = self.factory.create_person(b_year, last_name=parent.last_name)
                    self.all_people.append(child)
                    
                    # 3. Determine if the child has a partner [cite: 32]
                    mar_rate = rate_row['marriage_rate'].values[0] if not rate_row.empty else 0.5
                    if random.random() < mar_rate:
                        p_year = b_year + random.randint(-10, 10)
                        child.partner = self.factory.create_person(p_year) # Picks new last name
                        self.all_people.append(child.partner)
                        
                        # Add to queue to generate the next generation
                        queue.append(child)
                    else:
                        # Single parents still generate children in this simulation
                        queue.append(child)

        self.menu()

    def menu(self):
        """Handles user interaction [cite: 38-72]."""
        while True:
            print("\nAre you interested in:")
            print("(T)otal number of people in the tree")
            print("Total number of people in the tree by (D)ecade")
            print("(N)ames duplicated")
            choice = input("> ").upper()

            if choice == 'T':
                print(f"The tree contains {len(self.all_people)} people total") 
            elif choice == 'D':
                decades = {}
                for p in self.all_people:
                    d = (p.year_born // 10) * 10
                    decades[d] = decades.get(d, 0) + 1
                for d in sorted(decades.keys()):
                    print(f"{d}: {decades[d]}") 
            elif choice == 'N':
                full_names = [p.get_full_name() for p in self.all_people]
                duplicates = set([n for n in full_names if full_names.count(n) > 1])
                print(f"There are {len(duplicates)} duplicate names in the tree:")
                for name in sorted(duplicates):
                    print(f"* {name}") 

if __name__ == "__main__":
    FamilyTree().run()