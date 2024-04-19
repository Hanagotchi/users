import logging
from httpx import AsyncClient, Response, AsyncHTTPTransport
from os import environ

from exceptions.InternalServerErrorException import InternalServerErrorException
from exceptions.UserException import InvalidData

logger = logging.getLogger("social")
logger.setLevel("DEBUG")

SOCIAL_SERVICE_URL = environ["SOCIAL_SERVICE_URL"]

# Heroku dyno plan has a limit of 30 seconds...
# so, assign 3 retries of 10 seconds each :)
# https://devcenter.heroku.com/articles/request-timeout
NUMBER_OF_RETRIES = 3
TIMEOUT = 10


class SocialService:
    @staticmethod
    async def post(path: str, body: dict) -> Response:
        async with AsyncClient(
            transport=AsyncHTTPTransport(retries=NUMBER_OF_RETRIES), timeout=TIMEOUT
        ) as client:
            url = SOCIAL_SERVICE_URL + path
            response = await client.post(url, json=body)
            return response

    @staticmethod
    async def create_social_user(user_id: int):
        try:
            response = await SocialService.post("/social/users", body={"id": user_id})
            if response.status_code == 201:
                return
            else:
                raise InvalidData()
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise InternalServerErrorException("Social service")
