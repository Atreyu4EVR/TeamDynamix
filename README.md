# TeamDynamix Python Library

An unofficial Python library for interacting with the [TeamDynamix REST APIs](https://solutions.teamdynamix.com/TDWebApi/), providing a simple and intuitive scripts for managing TeamDynamix resources.

TeamDynamix is a powerful, enterprise-grade IT Service Management (ITSM) platform used by many respected educational and government organizations to manage ITIL-based operations and services. To learn more about TeamDynamix, visit [TeamDynamix.com](https://www.teamdynamix.com/).

> **Note**: This is an unofficial SDK and is not sanctioned or supported by TeamDynamix. Use at your own discretion and at your own risk.

## Status

This project is currently under active development. While some core functionality is implemented, we're continuously working on expanding coverage to remaining TeamDynamix APIs.

## Standard Client Patterns Implemented

Robust Base Client Class

```python
tdx_client = TeamDynamix(
    base_url="https://your-instance.teamdynamix.com",
    username="username",
    password="password"
)
```

- Single responsibility as HTTP client
- Handles authentication and requests
- Configurable through initialization

## Features

- Authentication handling with automatic token refresh
- Rate limiting support
- Comprehensive ticket management
- Type hints for better IDE support
- Dataclass-based models
- AI-powered test ticket generation using OpenAI

## Test Ticket Creation Tool

The `create_ticket.py` script provides an interactive way to generate test tickets with AI-generated content:

### Features

- Generates realistic ticket titles and descriptions using OpenAI
- Allows selection of ticket status (New, Open, In Process, etc.)
- Configurable through environment variables
- Interactive prompt for creating multiple tickets

### Setup

1. Copy `.env.example` to `.env`
2. Fill in your TeamDynamix credentials and API details
3. Add your OpenAI API key if using AI-generated content

### Usage

```bash
pip install teamdynamix
```

## Usage

```python
from teamdynamix import TDClient

client = TeamDynamix(
    base_url='https://your-instance.teamdynamix.com/TDWebApi',
    username='username',
    password='password'
)
```

### Test Ticket Generation

The library includes a utility for generating test tickets with synthetic data using OpenAI. This can be useful for testing and development purposes:

```python
from teamdynamix.utils import TicketGenerator

generator = TicketGenerator(client)
test_ticket = generator.create_test_ticket(category="Network Issues")
```

### Or initialize with BEID/Web Services Key

```python
client = TeamDynamix(
    base_url="https://your-instance.teamdynamix.com",
    beid="your_beid",
    web_services_key="your_web_services_key"
)
```

## Creating a Ticket

```python
ticket = client.tickets.create(
    AppID=123,
    TypeID=456,
    Title="Test Ticket",
    AccountID=789,
    StatusID=1,
    PriorityID=1,
    RequestorUid="user@example.com",
    Description="Test ticket description"
)
```

### Update ticket

```python
ticket.update({
    "Comments": "New comment",
    "NewStatus": 2
})
```

## Authentication

The library supports two authentication methods:

1. Username/Password
2. BEID/Web Services Key (Administrative access)

Environment variables can be used for admin credentials:

- `BEID`
- `WEB_SERVICES_KEY`

## Rate Limiting

All API methods are automatically rate-limited to comply with TeamDynamix API restrictions. The default limits are:

- Standard endpoints: 60 calls per minute
- Ticket creation: 120 calls per minute

## License

**Intent**: _This project was developed as a free service for fellow TeamDynamix users and is not supported by TeamDynamix. The license is intended to cover the use of the software for non-profit, educational, research, or personal projects._

**Non-Commercial Use:**
This project is provided under the [PolyForm Noncommercial License](https://polyformproject.org/licenses/noncommercial/1.0.0/). Feel free to use it for educational, research, or personal projects.

**Commercial Use:**
If you intend to use this software for profit-generating, revenue-driven, or otherwise commercial endeavors, please obtain a separate commercial license.

**Contact for Commercial License:**
[Ron Vallejo](https://github.com/Atreyu4EVR)
Email: [ronvallejo@gmail.com](mailto:ronvallejo@gmail.com)

## Reporting Issues

If you encounter any bugs or have feature requests, please file an issue on GitHub:

1. First, check if the issue has already been reported in the [Issues](https://github.com/Atreyu4EVR/TeamDynamix/issues) section.

2. If not, create a new issue with:
   - A clear, descriptive title
   - A detailed description of the issue
   - Steps to reproduce the problem
   - Expected vs actual behavior
   - Your environment details:
     - Python version
     - Library version
     - TeamDynamix instance (if relevant)
     - Operating system

Example bug report format:
