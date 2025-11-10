from fastapi import Request

def log_request(request:Request) -> None:
    print(f"[LOGGING!!!] {request.method} {request.url}")