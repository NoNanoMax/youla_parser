from fastapi import Request
from scrapping.playwright_manager import PWResources


def get_pw_res(request: Request) -> PWResources:
    return request.app.state.pw_res