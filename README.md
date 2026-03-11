# Inspirational Quote Microservice

A lightweight Flask microservice that returns a random, playful inspirational quote. Quotes are sourced from a built-in pool or generated via Groq LLM, and consecutive duplicates are never returned.

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

3. Install the required dependencies:

   ```
   pip3 install flask flask-cors groq python-dotenv
   ```

4. Create a `.env` file on root with your Groq API key:
   ```
   GROQ_API_KEY=your_api_key_here
   ```
   If no key is provided, the service will still work using the local quote pool as a fallback.

## Running the Service

```
python app.py
```

The server will be available at `http://localhost:5001`.

## HTTP API Endpoints

### `GET /quote`

Returns a random inspirational quote.

**Request:**
```
GET http://localhost:5001/quote
```

**Response (200):**
```json
{
  "quote": "Believe you can & you're halfway there. (No pressure though.)",
  "fallback_used": false
}
```

- `fallback_used`: `false` means the quote came from the LLM, `true` means it came from the local pool.

### `POST /quote`

Adds a new quote to the pool dynamically.

**Request:**
```
POST http://localhost:5001/quote
Content-Type: application/json

{
  "quote": "Stay curious, stay caffeinated."
}
```

**Response (201):**
```json
{
  "status": "Quote added successfully."
}
```

### Error Responses

| Status | Meaning                                    |
| ------ | ------------------------------------------ |
| 400    | Bad request (invalid input or duplicate quote) |
| 500    | Unexpected server error                    |

```json
{
  "error": "Description of the error."
}
```

## Frontend Integration Example

```javascript
// Fetch a quote
const response = await fetch("http://localhost:5001/quote");
const data = await response.json();
console.log(data.quote);

// Add a new quote
await fetch("http://localhost:5001/quote", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ quote: "Stay curious, stay caffeinated." }),
});
```

CORS is enabled, so requests from any origin (e.g., a local React/Vue dev server) will work out of the box.

## Architecture

```
Frontend (any origin)
    |
    |  HTTP (port 5001)
    v
Flask Server (app.py)
    |
    |  (optional) Groq API
    v
LLM Quote Generation
```

## Communication Contract

- **Port:** 5001
- **Data format:** JSON
- **CORS:** Enabled for all origins
- **No consecutive duplicates:** The service tracks the last returned quote and guarantees a different one each time.

## UML Sequence Diagram

```
Frontend                    Flask (app.py)                   Groq LLM
  |                              |                               |
  |  GET /quote                  |                               |
  |----------------------------->|                               |
  |                              |  generate quote request       |
  |                              |------------------------------>|
  |                              |  quote response               |
  |                              |<------------------------------|
  |                              |  (fallback to local pool      |
  |                              |   if LLM fails)               |
  |  200: {"quote": "..."}      |                               |
  |<-----------------------------|                               |
  |                              |                               |
```
