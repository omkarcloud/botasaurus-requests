# Botasaurus Requests

botasaurus-requests is a fork of the [hrequests](https://github.com/daijro/hrequests) library with the playwright dependencies removed.

## Installation

```bash
pip install botasaurus-requests
```

## Usage

```python
from botasaurus_requests import request

driver = Driver()
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