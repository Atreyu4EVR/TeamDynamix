from unittest.mock import patch, Mock

def test_create_ticket(tdx_client):
    # Create a proper mock JWT token
    mock_jwt = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MTYyMzkwMjJ9.fake-signature"

    with patch('requests.request') as mock_request:
        # Configure the mock to return success for both auth and create
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "ID": 123,
            "TypeID": 1,
            "ServiceID": 67,
            "Title": "Test Ticket",
            "StatusID": 1,
            "SourceID": 8,
            "RequestorEmail": "test@example.com",
            "ResponsibleGroupID": 118,
            "Description": "Test Description",
            "PriorityID": 1
        }
        mock_response.text = mock_jwt
        mock_request.return_value = mock_response

        # Create tickets instance
        tickets = tdx_client.tickets

        # Test create method
        response = tickets.create(
            app_id=123,
            type_id=1,
            service_id=67,
            title="Test Ticket",
            status_id=1,
            source_id=8,
            requestor_email="test@example.com",
            responsible_group_id=118,
            description="Test Description",
            priority_id=1
        )

        assert response.ID == 123
        assert response.Title == "Test Ticket"
        assert response.Description == "Test Description"

def test_rate_limiting(tdx_client):
    with patch('teamdynamix.utils.rate_limiter.time') as mock_time:
        # Configure time mock to return fixed timestamps
        timestamps = []
        def get_time():
            # Return timestamps that are very close together (0.1 second apart)
            # This ensures we hit the rate limit
            if not timestamps:
                timestamps.append(0)
            else:
                timestamps.append(timestamps[-1] + 0.1)
            return timestamps[-1]
            
        mock_time.time.side_effect = get_time
        mock_time.sleep = Mock()

        # Configure request mock
        with patch('requests.request') as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "ID": 123,
                "TypeID": 1,
                "ServiceID": 67,
                "Title": "Test Ticket",
                "StatusID": 1,
                "SourceID": 8,
                "RequestorEmail": "test@example.com",
                "ResponsibleGroupID": 118
            }
            mock_request.return_value = mock_response

            tickets = tdx_client.tickets

            # Make 125 requests (more than the limit of 120)
            # Each request will be timestamped 0.1 seconds apart
            for _ in range(125):
                tickets.create(
                    app_id=123,
                    type_id=1,
                    service_id=67,
                    title="Test Ticket",
                    status_id=1,
                    source_id=8,
                    requestor_email="test@example.com",
                    responsible_group_id=118
                )

            # Verify that sleep was called after the rate limit was exceeded
            mock_time.sleep.assert_called()

            # Additional assertions to verify rate limiting behavior
            assert len(timestamps) > 120  # Verify we made more than the limit
            assert timestamps[-1] - timestamps[0] < 60  # Verify requests happened within the time window