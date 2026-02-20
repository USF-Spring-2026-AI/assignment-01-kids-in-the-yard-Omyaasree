    # details of each simmulated person 

class Person:

    def __init__(self, first_name, last_name, year_born, year_died, gender):
        self.first_name = first_name
        self.last_name = last_name
        self.year_born = year_born
        self.year_died = year_died
        self.gender = gender
        
        self.partner = None
        self.children = []

    def add_child(self, child_person):
        self.children.append(child_person)

    def set_partner(self, partner_person):
        self.partner = partner_person

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.get_full_name()} ({self.year_born}-{self.year_died})"