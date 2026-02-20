import random

class FamilyTree:
    def __init__(self, factory):
        self.factory = factory
        self.root_people = []
        self.all_people_list = []

    def add_root_person(self, person):
        self.root_people.append(person)
        self.all_people_list.append(person)

    def generate_descendants(self, person, year_limit=2120):
        
        decade = self.factory.get_decade_string(person.year_born)

        rates = self.factory.birth_marriage_rates_df[
            self.factory.birth_marriage_rates_df['decade'] == decade
        ].iloc[0] # get first row 

        has_partner = random.random() < rates['marriage_rate']

        if has_partner == True:
            year_offset = random.randint(-10, 10)
            partner_year = person.year_born + year_offset

            if partner_year < 1950:
                partner_year = 1950
            
            if partner_year > 2120:
                partner_year = 2120
                
            new_partner = self.factory.create_person(partner_year)
            
            person.set_partner(new_partner)
            
            self.all_people_list.append(new_partner)

        average_rate = rates['birth_rate']

        total_calculation = average_rate 
        num_children = round(total_calculation)

        if num_children < 0:
            num_children = 0

        birth_years = []
        if num_children > 0:
            if num_children == 1:
                birth_years = [person.year_born + 35]
            else:
                gap = 20 / (num_children - 1)
                birth_years = []

                gap = 20 / (num_children - 1)

                for i in range(num_children):
                    extra_years = i * gap
                    child_year = (person.year_born + 25) + extra_years
                    birth_years.append(int(child_year))

        for b_year in birth_years:
            if b_year > year_limit:
                continue
            
            child = self.factory.create_person(b_year, last_name=person.last_name)
            person.add_child(child)
            self.all_people_list.append(child)
            
            self.generate_descendants(child, year_limit)

    def get_total_count(self):
        return len(self.all_people_list)

    def get_count_by_decade(self):
        counts = {}
        for p in self.all_people_list:
            decade = self.factory.get_decade_string(p.year_born)
            counts[decade] = counts.get(decade, 0) + 1
        return counts

    def get_duplicate_names(self):
            name_counts = {}
            for p in self.all_people_list:
                full_name = p.get_full_name()
                if full_name in name_counts:
                    name_counts[full_name] = name_counts[full_name] + 1
                else:
                    name_counts[full_name] = 1
            
            duplicates_list = []
            all_names = name_counts.keys()
            for name in all_names:
                if name_counts[name] > 1:
                    duplicates_list.append(name)
            return duplicates_list
                        