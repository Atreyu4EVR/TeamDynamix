# This file is licensed under the PolyForm Noncommercial License.
# For non-commercial use only.
# Commercial use requires a separate license.
# Contact ronvallejo@gmail.com for details.

from teamdynamix.tdnext.tickets.tickets import TicketManager, Ticket
from teamdynamix.http_client import TeamDynamix
from dotenv import load_dotenv
from scripts.ticket_generator import generate_ticket_content
import os

load_dotenv()

username = os.getenv('TDX_USERNAME')
password = os.getenv('TDX_PASSWORD')
base_url = os.getenv('BASE_URL')
app_id = os.getenv('TDX_APP_ID')
web_services_key = os.getenv('TDX_WEB_SERVICES_KEY')
token = os.getenv('TDX_TOKEN')
requestor_uid = os.getenv('REQUESTOR_UID')
requestor_email = os.getenv('REQUESTOR_EMAIL')

print("Environment variables loaded:")
print(f"Base URL: {base_url}")
print(f"Username: {username}")
print(f"App ID: {app_id}")

def create_test_ticket(title: str = None, description: str = None): # type: ignore
    status_list = [
        (28549, "New"),
        (28550, "Open"),
        (28551, "In Process"),
        (28552, "Resolved"),
        (28553, "Closed"),
        (28554, "Cancelled"),
        (28555, "On Hold")
    ]

    # Only prompt for title/description if they weren't provided
    if not title or not description:
        from scripts.ticket_generator import generate_ticket_content
        title, description = generate_ticket_content()

    # Add status selection
    print("\nAvailable Status Options:")
    for id, name in status_list:
        print(f"{id}: {name}")
    
    while True:
        status_input = input("\nEnter status ID (default is New - 28549): ").strip()
        if not status_input:
            status_id = 28549  # Default to "New"
            break
        try:
            status_id = int(status_input)
            if status_id in [id for id, _ in status_list]:
                break
            print("Invalid status ID. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

    # Initialize the client
    tdx_client = TeamDynamix(
        base_url=base_url,
        username=username,
        password=password
    )
    ticket_manager = TicketManager(tdx_client)

    try:
        ticket = ticket_manager.create(
            AppID=app_id,
            AccountID=8811,
            RequestorUid=requestor_uid,
            TypeID=4713,
            Title=title,
            StatusID=status_id,
            SourceID=1648,
            RequestorEmail=requestor_email,
            ResponsibleGroupID=1110,
            Description=description,
            PriorityID=864
        )
        
        print(f"Successfully created ticket ID: {ticket.ID}")
        print(f"Title: {ticket.Title}")
        print(f"Status: {ticket.StatusID}")
        
    except Exception as e:
        print(f"Error creating ticket: {str(e)}")

def main():
    while True:
        create_test_ticket()
        
        # Ask if user wants to create another ticket
        continue_creating = input("\nWould you like to create another ticket? (y/n): ").strip().lower()
        if continue_creating != 'y':
            print("Exiting ticket creation.")
            break

if __name__ == "__main__":
    main()