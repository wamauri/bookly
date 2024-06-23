from fastapi import Header, APIRouter

headers = APIRouter()


@headers.get('/get_headers', status_code=200)
async def get_headers(
    accept: str = Header(None),
    content_type: str = Header(None),
    user_agent: str = Header(None),
    host: str = Header(None),
):
    request_header = {}
    request_header['Accept'] = accept
    request_header['Content-Type'] = content_type
    request_header['User-Agent'] = user_agent
    request_header['Host'] = host

    return request_header
