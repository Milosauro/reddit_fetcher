# Reddit Fetcher

A modular Python application that interacts with the Reddit API to fetch and display the latest posts from a specified subreddit.

## Features

- OAuth authentication with the Reddit API
- Fetch the latest posts from any subreddit
- Display post information including title, author, and upvote count
- Filter posts by various criteria including upvotes and comments
- Export posts to JSON format
- Comprehensive error handling and logging
- Rate limit handling with automatic retries

## Project Structure

```
reddit_fetcher/
├── config/                  # Configuration management
│   ├── __init__.py
│   ├── settings.py          # Application settings
│   └── credentials.py       # API credentials handling
├── core/                    # Core application logic
│   ├── __init__.py
│   ├── auth.py              # Authentication module
│   ├── api_client.py        # Reddit API client
│   └── data_models.py       # Data models/structures
├── services/                # Business logic services
│   ├── __init__.py
│   ├── reddit_service.py    # Reddit API service layer
│   └── post_service.py      # Post processing logic
├── utils/                   # Utility functions
│   ├── __init__.py
│   ├── logger.py            # Logging utilities
│   ├── error_handler.py     # Error handling utilities
│   └── validators.py        # Input validation utilities
├── presentation/            # Output formatting
│   ├── __init__.py
│   ├── console_formatter.py # Console output formatting
│   └── output_manager.py    # Output management
├── main.py                  # Application entry point
├── requirements.txt         # Project dependencies
└── tests/                   # Test directory
    ├── __init__.py
    ├── test_api_client.py
    ├── test_data_models.py
    └── ...
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/reddit_fetcher.git
   cd reddit_fetcher
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your Reddit API credentials:
   - Create a Reddit developer application at https://www.reddit.com/prefs/apps
   - Create a `.env` file in the project root with the following content:
     ```
     REDDIT_CLIENT_ID=your_client_id
     REDDIT_CLIENT_SECRET=your_client_secret
     REDDIT_USER_AGENT=python:reddit-fetcher:v1.0 (by /u/your_username)
     ```

## Usage

### Basic Usage

```bash
python main.py -s python -l 5
```

This will fetch the 5 latest posts from the r/python subreddit.

### Command Line Arguments

- `-s, --subreddit`: The name of the subreddit to fetch posts from (default: "python")
- `-l, --limit`: The number of posts to fetch (default: 5)
- `-v, --verbose`: Enable verbose logging

### Examples

Fetch 10 latest posts from r/news:
```bash
python main.py -s news -l 10
```

Fetch posts with verbose logging:
```bash
python main.py -s science -l 5 -v
```

## Testing

Run the tests with pytest:

```bash
pytest
```

## Error Handling

The application handles various errors including:
- Authentication failures
- API rate limits
- Network issues
- Invalid subreddit names
- Invalid input parameters

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -am 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
