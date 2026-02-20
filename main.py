from Person_create import PersonFactory
from family_tree import FamilyTree

def main():
    print("Reading files...")
    factory = PersonFactory()
    tree = FamilyTree(factory)

    print("Generating family tree...")
    desmond = factory.create_person(1950, last_name="Jones", gender="male")
    molly = factory.create_person(1950, last_name="Jones", gender="female")
    
    desmond.set_partner(molly)
    molly.set_partner(desmond)
    
    tree.add_root_person(desmond)
    tree.add_root_person(molly)

    tree.generate_descendants(desmond)
    tree.generate_descendants(molly)

    while True:
        print("\nAre you interested in:")
        print("(T)otal number of people in the tree")
        print("Total number of people in the tree by (D)ecade")
        print("(N)ames duplicated")
        print("(Q)uit")
        
        choice = input("> ").upper()

        if choice == 'T':
            total = tree.get_total_count()
            print(f"The tree contains {total} people total")
        
        elif choice == 'D':
            counts = tree.get_count_by_decade()
            for decade in sorted(counts.keys()):
                print(f"{decade}: {counts[decade]}")
        
        elif choice == 'N':
            duplicates = tree.get_duplicate_names()
            if not duplicates:
                print("No duplicate names found.")
            else:
                print(f"There are {len(duplicates)} duplicate names in the tree:")
                for name in duplicates:
                    print(f"* {name}")
        
        elif choice == 'Q':
            print("Exiting program.")
            break
        
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()