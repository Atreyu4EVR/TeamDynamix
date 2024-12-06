from unittest.mock import patch, Mock

def test_create_ticket(tdx_client):
    # Create a proper mock JWT token
    mock_jwt = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MTYyMzkwMjJ9.fake"

    with patch('requests.post') as mock_post, patch('requests.request') as mock_request:
        # Mock the admin authentication response
        mock_auth_response = Mock()
        mock_auth_response.status_code = 200
        mock_auth_response.text = mock_jwt
        mock_post.return_value = mock_auth_response

        # Mock the ticket creation response
        mock_ticket_response = Mock()
        mock_ticket_response.status_code = 200
        mock_ticket_response.json.return_value = {
            "ID": 123,
            "TypeID": 1,
            "Title": "Test Ticket",
            "Description": "Test Description"
        }
        mock_request.return_value = mock_ticket_response

        # Create tickets instance and test
        tickets = tdx_client.tickets
        response = tickets.create(
            AppID=122,
            AccountID=8811,
            RequestorUid=2222,
            TypeID=4713,
            Title="Test Ticket",
            StatusID=123,
            PriorityID=864,
            Description="Test Description",
            SourceID=1648,
            RequestorEmail="requestor_email",
            ResponsibleGroupID=1110
        )

        assert response.ID == 123
        assert response.Title == "Test Ticket"

def test_rate_limiting(tdx_client):
    # Create a proper mock JWT token
    mock_jwt = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MTYyMzkwMjJ9.fake"

    with patch('teamdynamix.utils.rate_limiter.time') as mock_time, \
         patch('requests.post') as mock_post, \
         patch('requests.request') as mock_request:
        
        # Mock admin authentication
        mock_auth_response = Mock()
        mock_auth_response.status_code = 200
        mock_auth_response.text = mock_jwt
        mock_post.return_value = mock_auth_response

        # Configure time mock
        timestamps = []
        def get_time():
            if not timestamps:
                timestamps.append(0)
            else:
                timestamps.append(timestamps[-1] + 0.1)
            return timestamps[-1]
            
        mock_time.time.side_effect = get_time
        mock_time.sleep = Mock()

        # Mock ticket creation response
        mock_ticket_response = Mock()
        mock_ticket_response.status_code = 200
        mock_ticket_response.json.return_value = {
            "ID": 1232514,
            "TypeID": 4713,
            "Title": "Test Ticket",
            "Description": "Test Description"
        }
        mock_request.return_value = mock_ticket_response

        tickets = tdx_client.tickets

        # Make 125 requests (more than the limit of 120)
        # Each request will be timestamped 0.1 seconds apart
        for _ in range(125):
            tickets.create(
                AppID=122,
                AccountID=8811,
                RequestorUid=2222,
                TypeID=4713,
                Title="Test Ticket",
                StatusID=123,
                PriorityID=864,
                Description="Test Description",
                SourceID=1648,
                RequestorEmail="requestor_email",
                ResponsibleGroupID=1110
            )

        # Verify that sleep was called after the rate limit was exceeded
        mock_time.sleep.assert_called()

        # Additional assertions to verify rate limiting behavior
        assert len(timestamps) > 120  # Verify we made more than the limit
        assert timestamps[-1] - timestamps[0] < 60  # Verify requests happened within the time window