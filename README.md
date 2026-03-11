# Inspirational Quote Microservice

A lightweight ZeroMQ microservice that returns a random inspirational quote when called with no input.

## Prerequisites

- Python 3

## Setup

1. Clone this repository and navigate into it:

   ```
   cd quotes_microservice
   ```

2. Create and activate a virtual environment:

   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required dependency:
   ```
   pip3 install pyzmq
   ```

## Running the Microservice

```
python quotes_microservice.py
```

You should see:

```
Inspirational Quote Microservice is running on port 5556...
```

The server will keep running and listen for requests on `tcp://localhost:5556`.

## How to Request a Quote

Send a JSON string over a ZMQ REQ socket with `"input"` set to `null` (or omitted entirely, or an empty string).

### Example Client (Python)

```python
import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5556")

# Send a request with no input
socket.send_string(json.dumps({"input": None}))

# Receive the response
response = json.loads(socket.recv_string())
print(response["quote"])
```

### Request Format

| Field   | Type                    | Description                              |
| ------- | ----------------------- | ---------------------------------------- |
| `input` | `null` / `""` / omitted | Must be empty or null to receive a quote |

### Response Format

**Success:**

```json
{
  "quote": "Believe you can & you're halfway there."
}
```

**Error (non-empty input provided):**

```json
{
  "error": "Input must be empty/null to receive a quote."
}
```

## Communication Contract

- **Protocol:** ZeroMQ (REQ/REP pattern)
- **Port:** 5556
- **Data format:** JSON strings sent/received via `send_string` / `recv_string`

## UML Sequence Diagram

```
Client                          Microservice
  |                                  |
  |  zmq REQ: {"input": null}       |
  |--------------------------------->|
  |                                  |  select random quote
  |  zmq REP: {"quote": "..."}      |
  |<---------------------------------|
  |                                  |
```
