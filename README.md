# Botasaurus Requests

botasaurus-requests is a fork of the [hrequests](https://github.com/daijro/hrequests) library, featuring the following updates:

- Removal of the playwright dependencies, to make it more lightweight.
- Bug fixes to ensure smooth execution on Windows, eliminating runtime errors.
- Addition of the Google Referer header in the get method to make requests more humane.

## Installation

```bash
pip install botasaurus-requests
```

## Usage

```python
from botasaurus_requests import request

response = request.get(
    "https://www.g2.com/products/omkar-cloud/reviews",
    headers={
        "Referer": "https://www.google.com/",
    },
)
print(response.status_code)
```

## Credits

Kudos to [daijro](https://github.com/daijro) for creating [hrequests](https://github.com/daijro/hrequests).