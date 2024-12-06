from teamdynamix.tdnext.tickets.tickets import TicketManager
#from teamdynamix.blackout.blackout import BlackoutWindowManager
#from teamdynamix.impacts.impacts import ImpactManager
#from teamdynamix.maintenance.maintenance import MaintenanceManager
#from teamdynamix.priorities.priorities import PriorityManager
#from teamdynamix.sources.sources import SourceManager
#from teamdynamix.searches.searches import SearchManager
#from teamdynamix.statuses.statuses import StatusManager
#from teamdynamix.tasks.tasks import TaskManager
#from teamdynamix.types.types import TypeManager
#from teamdynamix.urgencies.urgencies import UrgencyManager

class TDNext:
    """Base class for technician-level operations in TeamDynamix"""
    
    def __init__(self, client):
        """Initialize TDNext with all available managers
        
        Args:
            client: TeamDynamix API client instance with authentication
        """
        self._client = client
        
        # Initialize all managers
        self.tickets = TicketManager(client)
        #self.blackout = BlackoutWindowManager(client)
        #self.impacts = ImpactManager(client)
        #self.maintenance = MaintenanceManager(client)
        #self.priorities = PriorityManager(client)
        #self.sources = SourceManager(client)
        #self.searches = SearchManager(client)
        #self.statuses = StatusManager(client)
        #self.tasks = TaskManager(client)
        #self.types = TypeManager(client)
        #self.urgencies = UrgencyManager(client) 