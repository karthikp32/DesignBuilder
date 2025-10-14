# Tiny Web Server Design (for Testing)

## Overview
A minimal web server that accepts HTTP requests, routes them to handlers, and returns responses. Designed for testing the automated component extraction, implementation, and caching system.

---

## Components

### HTTP Server
- **Responsibilities:**
  - Listen on a port and accept incoming requests.
  - Delegate requests to the Router.
- **Dependencies:** Router, Logger
- **Interfaces:**
  - `start(port: int)`  
  - `stop()`

### Router
- **Responsibilities:**
  - Map URL paths to handler functions.
- **Dependencies:** None
- **Interfaces:**
  - `add_route(path: str, handler: Callable)`  
  - `route_request(path: str)`

### Handler
- **Responsibilities:**
  - Generate responses for requests.
- **Dependencies:** Logger  
- **Interfaces:**
  - `handle(request: dict)` → returns response.

### Logger
- **Responsibilities:**
  - Log all incoming requests and errors.
- **Dependencies:** None  
- **Interfaces:**
  - `log(message: str)`

---

## Flow
1. HTTP Server receives request → passes path to Router.  
2. Router finds the matching handler → calls `handle()`.  
3. Handler produces response → returned to client.  
4. Logger records the request.

---

## Notes
- All components should have simple tests.  
- Ideal for validating caching and planner logic.  
