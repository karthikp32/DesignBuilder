# Simple Web Server Design

## Overview
This document describes the design for a simple web server that can handle HTTP requests, serve static content, and respond with dynamic responses. The goal is to create a minimal, modular system suitable for testing automation tools like DesignBuilder.

---

## Components

### 1. HTTP Server
- **Type:** Service
- **Responsibilities:**
  - Accept incoming HTTP requests.
  - Route requests to appropriate handlers.
  - Return HTTP responses.
- **Dependencies:** 
  - Request Handler
  - Router
  - Logger
- **Interfaces:**
  - `start_server(port: int)` → starts listening for HTTP requests.
  - `stop_server()` → gracefully stops the server.

---

### 2. Router
- **Type:** Module
- **Responsibilities:**
  - Map URL paths and HTTP methods to request handlers.
  - Support dynamic and static routes.
- **Dependencies:** None
- **Interfaces:**
  - `add_route(path: str, method: str, handler: Callable)`
  - `get_handler(path: str, method: str)` → returns a handler function.

---

### 3. Request Handler
- **Type:** Module
- **Responsibilities:**
  - Process HTTP requests and generate responses.
  - Separate handlers for static content and dynamic API responses.
- **Dependencies:** Logger
- **Interfaces:**
  - `handle_static(request: Request)` → returns static file content.
  - `handle_dynamic(request: Request)` → returns dynamic response.

---

### 4. Logger
- **Type:** Module
- **Responsibilities:**
  - Log incoming requests, errors, and server events.
- **Dependencies:** None
- **Interfaces:**
  - `log_request(request: Request)`
  - `log_error(error: str)`

---

### 5. Static File Storage
- **Type:** Storage
- **Responsibilities:**
  - Store static files like HTML, CSS, JS.
  - Serve files upon request.
- **Dependencies:** File system access
- **Interfaces:**
  - `get_file(file_path: str)` → returns file content.

---

### 6. Dynamic API Module
- **Type:** Service
- **Responsibilities:**
  - Handle API requests and generate JSON responses.
  - Example endpoints: `/status`, `/time`
- **Dependencies:** None
- **Interfaces:**
  - `get_status()` → returns server status
  - `get_time()` → returns current server time

---

## System Flow

1. Client sends HTTP request → HTTP Server receives request.
2. HTTP Server passes request to Router → Router finds matching handler.
3. Request Handler processes request:
   - If static → reads file from Static File Storage
   - If dynamic → calls Dynamic API Module
4. Response is sent back to client.
5. Logger records the request and any errors.

---

## Notes
- The system should be modular to allow replacing HTTP server with another implementation.
- All components should have unit tests.
- Designed to be simple for automation and testing with DesignBuilder.

