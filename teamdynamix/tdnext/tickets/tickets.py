__all__ = ['Ticket', 'TicketManager']

from typing import Dict, List, Optional, Any, Union
from uuid import UUID
from datetime import datetime
from teamdynamix.authentication.rate_limiter import RateLimiter 
from dataclasses import dataclass, field, fields

@dataclass(frozen=True)
class Ticket:
    """
    TeamDynamix Ticket class representing a support ticket and its operations.
    All properties are read-only after initialization.
    """
    # Basic properties
    ID: int
    _client: Any = field(repr=False, compare=False)
    ParentID: Optional[int] = None
    ParentTitle: Optional[str] = None
    ParentClass: Optional[str] = None
    TypeID: Optional[int] = None
    TypeName: Optional[str] = None
    TypeCategoryID: Optional[int] = None
    TypeCategoryName: Optional[str] = None
    Classification: Optional[str] = None
    FormID: Optional[int] = None
    FormName: Optional[str] = None
    Title: Optional[str] = None
    Description: Optional[str] = None
    Uri: Optional[str] = None
    ClassificationName: Optional[str] = None
    # Account and source information
    AccountID: Optional[int] = None
    AccountName: Optional[str] = None
    SourceID: Optional[int] = None
    SourceName: Optional[str] = None
    # Status and priority
    StatusID: Optional[int] = None
    StatusName: Optional[str] = None
    StatusClass: Optional[str] = None
    ImpactID: Optional[int] = None
    ImpactName: Optional[str] = None
    UrgencyID: Optional[int] = None
    UrgencyName: Optional[str] = None
    PriorityID: Optional[int] = None
    PriorityName: Optional[str] = None
    PriorityOrder: Optional[float] = None
    # SLA information
    SlaID: Optional[int] = None
    SlaName: Optional[str] = None
    IsSlaViolated: Optional[bool] = None
    IsSlaRespondByViolated: Optional[bool] = None
    IsSlaResolveByViolated: Optional[bool] = None
    RespondByDate: Optional[datetime] = None
    ResolveByDate: Optional[datetime] = None
    SlaBeginDate: Optional[datetime] = None
    # Hold status
    IsOnHold: Optional[bool] = None
    PlacedOnHoldDate: Optional[datetime] = None
    GoesOffHoldDate: Optional[datetime] = None
    # Creation and modification info
    CreatedDate: Optional[datetime] = None
    CreatedUid: Optional[str] = None
    CreatedFullName: Optional[str] = None
    CreatedEmail: Optional[str] = None
    ModifiedDate: Optional[datetime] = None
    ModifiedUid: Optional[str] = None
    ModifiedFullName: Optional[str] = None
    # Requestor information
    RequestorName: Optional[str] = None
    RequestorFirstName: Optional[str] = None
    RequestorLastName: Optional[str] = None
    RequestorEmail: Optional[str] = None
    RequestorPhone: Optional[str] = None
    RequestorUid: Optional[str] = None
    # Time tracking
    ActualMinutes: Optional[int] = None
    EstimatedMinutes: Optional[int] = None
    DaysOld: Optional[int] = None
    StartDate: Optional[datetime] = None
    EndDate: Optional[datetime] = None
    
    # Responsibility assignment
    ResponsibleUid: Optional[str] = None
    ResponsibleFullName: Optional[str] = None
    ResponsibleEmail: Optional[str] = None
    ResponsibleGroupID: Optional[int] = None
    ResponsibleGroupName: Optional[str] = None
    # Response tracking
    RespondedDate: Optional[datetime] = None
    RespondedUid: Optional[str] = None
    RespondedFullName: Optional[str] = None
    # Completion information
    CompletedDate: Optional[datetime] = None
    CompletedUid: Optional[str] = None
    CompletedFullName: Optional[str] = None
    # Review information
    ReviewerUid: Optional[str] = None
    ReviewerFullName: Optional[str] = None
    ReviewerEmail: Optional[str] = None
    ReviewingGroupID: Optional[int] = None
    ReviewingGroupName: Optional[str] = None
    # Budget tracking
    TimeBudget: Optional[float] = None
    ExpensesBudget: Optional[float] = None
    TimeBudgetUsed: Optional[float] = None
    ExpensesBudgetUsed: Optional[float] = None
    # Task conversion info
    IsConvertedToTask: Optional[bool] = None
    ConvertedToTaskDate: Optional[datetime] = None
    ConvertedToTaskUid: Optional[str] = None
    ConvertedToTaskFullName: Optional[str] = None
    TaskProjectID: Optional[int] = None
    TaskProjectName: Optional[str] = None
    TaskPlanID: Optional[int] = None
    TaskPlanName: Optional[str] = None
    TaskID: Optional[int] = None
    TaskTitle: Optional[str] = None
    TaskStartDate: Optional[datetime] = None
    TaskEndDate: Optional[datetime] = None
    TaskPercentComplete: Optional[int] = None
    
    # Additional properties
    OpportunityID: Optional[int] = None
    OpportunityName: Optional[str] = None
    LocationID: Optional[int] = None
    LocationName: Optional[str] = None
    LocationRoomID: Optional[int] = None
    LocationRoomName: Optional[str] = None
    RefCode: Optional[str] = None
    ServiceID: Optional[int] = None
    ServiceName: Optional[str] = None
    ServiceCategoryID: Optional[int] = None
    ServiceCategoryName: Optional[str] = None
    ArticleID: Optional[int] = None
    ArticleSubject: Optional[str] = None
    ArticleStatus: Optional[str] = None
    ArticleCategoryPathNames: Optional[str] = None
    AppID: Optional[int] = None
    
    # Collections
    Attributes: Optional[List[Dict[str, Any]]] = None
    Attachments: Optional[List[Dict[str, Any]]] = None
    Tasks: Optional[List[Dict[str, Any]]] = None
    Notify: Optional[List[Dict[str, Any]]] = None
    

    @classmethod
    def from_dict(cls, client, data: Dict[str, Any]) -> 'Ticket':
        """Create a Ticket instance from a dictionary of attributes."""
        # Filter out unknown fields from the response data
        valid_fields = {f.name for f in fields(cls)}
        filtered_data = {k: v for k, v in data.items() if k in valid_fields}
        return cls(_client=client, **filtered_data)
    
    def _base_url(self, endpoint: str = "") -> str:
        """
        Construct the base URL for ticket endpoints.
        
        Args:
            endpoint: Additional endpoint path
            
        Returns:
            Complete endpoint URL
        """
        return f"/{self.AppID}/tickets/{self.ID}{endpoint}"

    @RateLimiter()
    def remove_asset(self, asset_id: int) -> bool:
        """
        Removes an asset from ticket.
        Rate limit: 60 calls per IP address every 60 seconds.
        
        Args:
            asset_id: ID of the asset to remove
            
        Returns:
            True if successful, False otherwise
        """
        return self._client.delete(self._base_url(f"/assets/{asset_id}"))

    @RateLimiter()
    def add_asset(self, asset_id: int) -> bool:
        """
        Adds an asset to ticket.
        Rate limit: 60 calls per IP address every 60 seconds.
        
        Args:
            asset_id: ID of the asset to add
            
        Returns:
            True if successful, False otherwise
        """
        return self._client.post(self._base_url(f"/assets/{asset_id}"))

    @RateLimiter()
    def upload_attachment(self, attachment: Dict) -> Dict:
        """
        Uploads an attachment to a ticket.
        Rate limit: 60 calls per IP address every 60 seconds.
        
        Args:
            attachment: Attachment data
            
        Returns:
            Attachment information
        """
        return self._client.post(
            self._base_url("/attachments"),
            files=attachment
        )

    @RateLimiter()
    def get_contacts(self) -> List[Dict]:
        """
        Gets the ticket contacts.
        Rate limit: 60 calls per IP address every 60 seconds.
        
        Returns:
            List of contact information
        """
        return self._client.get(self._base_url("/contacts"))

    @RateLimiter()
    def delete_contact(self, contact_uid: str) -> bool:
        """
        Removes a contact from the ticket.
        Rate limit: 60 calls per IP address every 60 seconds.
        
        Args:
            contact_uid: UID of the contact to remove
            
        Returns:
            True if successful, False otherwise
        """
        return self._client.delete(self._base_url(f"/contacts/{contact_uid}"))

    @RateLimiter()
    def add_contact(self, contact_uid: str) -> bool:
        """
        Adds a contact to ticket.
        Rate limit: 60 calls per IP address every 60 seconds.
        
        Args:
            contact_uid: UID of the contact to add
            
        Returns:
            True if successful, False otherwise
        """
        return self._client.post(self._base_url(f"/contacts/{contact_uid}"))

    @RateLimiter()
    def get_feed(self) -> List[Dict]:
        """
        Gets the feed entries for a ticket.
        Rate limit: 60 calls per IP address every 60 seconds.
        
        Returns:
            List of feed entries
        """
        return self._client.get(self._base_url("/feed"))

    @RateLimiter()
    def update(self, item_update: Dict) -> Union[Dict, bool]:
        """
        Updates a ticket.
        Rate limit: 60 calls per IP address every 60 seconds.
        
        Args:
            item_update: Update data
            
        Returns:
            Feed entry if successful, False otherwise
        """
        return self._client.post(self._base_url("/feed"), json=item_update)

    @RateLimiter()
    def edit(self, updated_ticket: Dict, notify_new_responsible: bool = False) -> Dict:
        """
        Edits an existing ticket.
        Rate limit: 60 calls per IP address every 60 seconds.
        
        Args:
            updated_ticket: Updated ticket data
            notify_new_responsible: Whether to notify newly responsible people
            
        Returns:
            Updated ticket information
        """
        return self._client.post(
            self._base_url(f"?notifyNewResponsible={str(notify_new_responsible).lower()}"),
            json=updated_ticket
        )


class TicketManager:
    """Manages ticket operations for TeamDynamix"""
    
    def __init__(self, client):
        """
        Initialize TicketManager.
        
        Args:
            client: TeamDynamix API client instance
        """
        self._client = client

    def _build_url(self, appId: int, endpoint: str = "") -> str:
        """Build URL with required appId parameter"""
        return f"/api/{appId}/tickets{endpoint}"


    @RateLimiter(max_calls=120, period=60)
    def create(
        self,
        AppID: int,
        TypeID: int,
        Title: str,
        AccountID: int,
        StatusID: int,
        PriorityID: int,
        RequestorUid: str,
        Description: str,
        ServiceID: Optional[int] = None,
        SourceID: Optional[int] = None,
        ResponsibleGroupID: Optional[int] = None,
        Classification: Optional[str] = None,
        Attributes: Optional[List[Dict[str, Any]]] = None,
        Notify: Optional[List[Dict[str, Any]]] = None,
        EnableNotifyReviewer: bool = False,
        NotifyRequestor: bool = True,
        NotifyResponsible: bool = True,
        AllowRequestorCreation: bool = True,
        ApplyDefaults: bool = True,
        **additional_fields
    ) -> Ticket:
        """Creates a ticket."""
        try:
            app_id = int(AppID)
        except (TypeError, ValueError):
            raise ValueError(f"AppID must be an integer, got {type(AppID)}: {AppID}")
        # Construct the ticket data (body)
        ticket_data = {
            "TypeID": TypeID,
            "Title": Title,
            "AccountID": AccountID,
            "StatusID": StatusID,
            "PriorityID": PriorityID,
            "RequestorUid": RequestorUid,
            "Description": Description,
            **{k: v for k, v in additional_fields.items() if v is not None}
        }
        
        # Add optional fields if provided
        if ServiceID is not None: ticket_data["ServiceID"] = ServiceID
        if SourceID is not None: ticket_data["SourceID"] = SourceID
        if ResponsibleGroupID is not None: ticket_data["ResponsibleGroupID"] = ResponsibleGroupID
        if Classification is not None: ticket_data["Classification"] = Classification
        if Attributes is not None: ticket_data["Attributes"] = Attributes
        if Notify is not None: ticket_data["Notify"] = Notify
        
        # Make the API call
        response = self._client.post(
            f"api/{app_id}/tickets",
            json=ticket_data,
            params={
                "EnableNotifyReviewer": str(EnableNotifyReviewer).lower(),
                "NotifyRequestor": str(NotifyRequestor).lower(),
                "NotifyResponsible": str(NotifyResponsible).lower(),
                "AllowRequestorCreation": str(AllowRequestorCreation).lower(),
                "ApplyDefaults": str(ApplyDefaults).lower()
            }
        )
        
        return Ticket.from_dict(self._client, response)