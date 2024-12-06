from scripts.ticket_generator import generate_ticket_content as ticket_generator_function

def create_synthetic_ticket():
    """
    Generate and create a ticket using AI-generated content
    """
    categories = [
        "Hardware Issues",
        "Software Problems",
        "Network Connectivity",
        "Account Access",
        "Email Issues",
        "Printer Problems",
        "Custom"
    ]
    
    print("\nAvailable categories:")
    for i, category in enumerate(categories, 1):
        print(f"{i}. {category}")
    
    choice = input("\nSelect a category number (or press Enter for random): ")
    
    selected_category = None
    if choice.isdigit() and 1 <= int(choice) <= len(categories):
        selected_category = categories[int(choice) - 1]
        if selected_category == "Custom":
            selected_category = input("Enter custom category: ")
    
    generated_title, generated_description = ticket_generator_function(selected_category) # type: ignore
    
    if generated_title and generated_description:
        print("\nGenerated Ticket Content:")
        print(f"\nTitle: {generated_title}")
        print(f"\nDescription: {generated_description}")
        
        create = input("\nWould you like to create this ticket? (y/n): ")
        if create.lower() == 'y':
            from create_ticket import create_test_ticket
            create_test_ticket(generated_title, generated_description)

if __name__ == "__main__":
    create_synthetic_ticket()