# API Documentation - capibara6

## Table of Contents
- [Overview](#overview)
- [Authentication](#authentication)
- [Backend API Endpoints](#backend-api-endpoints)
- [Frontend Integration](#frontend-integration)
- [Error Handling](#error-handling)
- [Rate Limiting](#rate-limiting)
- [Examples](#examples)

## Overview

The capibara6 API provides endpoints for managing conversations, user data, and system operations. The system is divided into two main components:

1. **Backend API**: Flask server handling data persistence, email notifications, and health checks
2. **Frontend API**: JavaScript-based client-side functionality for the web interface

## Authentication

The capibara6 API currently uses a simple email-based identification system for conversation tracking. No complex authentication is required for the public-facing endpoints, as the system is designed for open interaction with email collection for follow-up purposes.

## Backend API Endpoints

### POST /api/save-conversation

Saves conversation data to the system and sends email notifications to both the user and administrators.

#### Request
- **URL**: `/api/save-conversation`
- **Method**: `POST`
- **Content-Type**: `application/json`

#### Request Body
```json
{
  "email": "string",
  "conversations": [
    {
      "message": "string",
      "timestamp": "string (ISO 8601 format)"
    }
  ]
}
```

**Fields**:
- `email` (string): User's email address for follow-up communication
- `conversations` (array): Array of conversation objects
  - `message` (string): The actual message content
  - `timestamp` (string): ISO 8601 formatted timestamp

#### Response
```json
{
  "success": true,
  "email_sent": true,
  "admin_notified": true,
  "message": "Datos guardados correctamente"
}
```

**Response Fields**:
- `success` (boolean): Indicates if the operation was successful
- `email_sent` (boolean): Indicates if user email was sent successfully
- `admin_notified` (boolean): Indicates if admin notification was sent
- `message` (string): Human-readable status message

#### Example Request
```bash
curl -X POST http://localhost:5000/api/save-conversation \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "conversations": [
      {
        "message": "Hello, I'm interested in capibara6",
        "timestamp": "2025-10-02T10:30:00.000Z"
      }
    ]
  }'
```

### GET /api/health

Health check endpoint to verify the backend server is running.

#### Request
- **URL**: `/api/health`
- **Method**: `GET`

#### Response
```json
{
  "status": "healthy",
  "timestamp": "string (ISO 8601 format)"
}
```

**Response Fields**:
- `status` (string): Current health status of the server
- `timestamp` (string): ISO 8601 formatted timestamp of the check

#### Example Request
```bash
curl -X GET http://localhost:5000/api/health
```

## Frontend Integration

The frontend JavaScript code communicates with the backend API through the chatbot functionality. The main integration points include:

### Chatbot API Calls

The chatbot functionality in `chatbot.js` handles the following:

1. **Sending Messages**: When users submit messages through the UI, the system collects them in memory until the user provides an email.
2. **Saving Conversations**: When the user submits their email, the full conversation is sent to `/api/save-conversation`.
3. **Real-time Display**: Messages are displayed in real-time in the chat interface.

### Email Collection Flow

1. The user engages with the chatbot
2. Messages are stored temporarily in the frontend
3. When the user clicks "Enviar a capibara6", they are prompted for their email
4. Once email is provided, the entire conversation is sent to `/api/save-conversation`

## Error Handling

### Backend Errors

The backend API handles various error conditions:

- **Invalid Email Format**: Returns 400 Bad Request with error message
- **SMTP Configuration Issues**: Returns 500 Internal Server Error
- **Database/Storage Issues**: Returns 500 Internal Server Error
- **Missing Required Fields**: Returns 400 Bad Request

### Response Format for Errors
```json
{
  "success": false,
  "error": "Error message describing the issue",
  "message": "User-friendly message"
}
```

## Rate Limiting

The current implementation does not include built-in rate limiting. Implement rate limiting at the infrastructure level (reverse proxy, load balancer) if needed for your deployment.

## Examples

### Complete Conversation Flow

1. **User interacts with chatbot** (messages stored in frontend memory)

2. **User provides email and submits**:
```javascript
// Pseudo-code for frontend
const conversationData = {
  email: "user@example.com",
  conversations: [
    { message: "Hello!", timestamp: new Date().toISOString() },
    { message: "I want to learn about capibara6", timestamp: new Date().toISOString() },
    { message: "Tell me about the TPU optimization", timestamp: new Date().toISOString() }
  ]
};

fetch('/api/save-conversation', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(conversationData)
})
.then(response => response.json())
.then(data => {
  if(data.success) {
    alert('¡Gracias! Su conversación ha sido guardada.');
  }
});
```

3. **Backend processes**:
   - Saves conversation to `user_data/conversations.json`
   - Saves conversation to timestamped text file in `user_data/`
   - Sends email confirmation to user
   - Sends notification to admin

### Health Check
```javascript
// Check if backend is available
fetch('/api/health')
  .then(response => response.json())
  .then(data => {
    if(data.status === 'healthy') {
      console.log('Backend is operational');
    }
  })
  .catch(error => {
    console.error('Backend is not responding:', error);
  });
```

## Response Codes

- `200 OK`: Request processed successfully
- `400 Bad Request`: Request missing required fields or has invalid data
- `500 Internal Server Error`: Server error during processing

## CORS Policy

The backend includes CORS headers to allow cross-origin requests from the frontend:

```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, OPTIONS
Access-Control-Allow-Headers: Content-Type
```

This allows the frontend to communicate with the backend API from different ports during development.