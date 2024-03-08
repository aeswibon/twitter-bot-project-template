import base64
import json

import requests
from django.conf import settings
from django.http import HttpResponseRedirect
from django_redis import get_redis_connection
from django_redis.client import DefaultClient
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from project_name.bot.api.serializer import BotSerializer
from project_name.bot.models import Bot
from project_name.utils.constants import AUTH_URL, POST_TWEET_URL, TOKEN_URL
from project_name.utils.helper import (
    generate_code_challenge,
    generate_code_verifier,
    make_token,
)


class BotViewset(viewsets.GenericViewSet):
    # create an OAuth2Session instance with the client ID, redirect URI, and scopes
    _twitter = make_token()

    # get the default redis connection
    _redis: DefaultClient = get_redis_connection("default")

    _code_verifier = generate_code_verifier()
    _code_challenge = generate_code_challenge(_code_verifier)

    queryset = Bot.objects.all()
    serializer_class = BotSerializer

    def __process_token(self, token):
        """
        Process the token and store it in Redis.
        """
        str_token = '"{}"'.format(token)
        json_token = json.loads(str_token)
        self._redis.set("token", json_token)  # store the token in redis
        return json.loads(json_token.replace("'", '"'))

    def __tweet(self, token):
        """
        Tweet a message.
        """

        bot = self.queryset.first()
        if not bot:
            raise Exception("No bot found")

        payload = "Hello from the {}".format(bot.name)

        # sending a tweet
        res = requests.request(
            "post",
            POST_TWEET_URL,
            json={"text": payload},
            headers={
                "Authorization": "Bearer {}".format(token.get("access_token")),
                "Content-Type": "application/json",
            },
        )

        if res.status_code != 201:
            raise Exception("Error in tweeting")

        bot.delete()

    @action(detail=False, methods=["post"])
    def home(self, request, *args, **kwargs) -> HttpResponseRedirect:
        """
        Redirect to the Twitter authorization URL.
        """
        auth_url, state = self._twitter.authorization_url(
            AUTH_URL,
            code_challenge=self._code_challenge,
            code_challenge_method="S256",
        )
        self._redis.set("oauth_state", state)
        return HttpResponseRedirect(redirect_to=auth_url)

    @action(detail=False, methods=["get"])
    def callback(self, request, *args, **kwargs) -> Response:
        """
        Handle the callback from Twitter.
        """
        code = request.GET.get("code")
        state = request.GET.get("state")

        # Validation checks

        if not code or not state:
            return Response(
                {"error": "Missing code or state"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        session_state = self._redis.get("oauth_state").decode("utf-8")
        if state != session_state:
            return Response(
                {"error": "Invalid state"}, status=status.HTTP_400_BAD_REQUEST
            )

        self._redis.set("state", state)
        self._redis.set("code", code)

        # Exchange the authorization code for an access token
        token = self._twitter.fetch_token(
            token_url=TOKEN_URL,
            client_secret=settings.CLIENT_SECRET,
            code_verifier=self._code_verifier,
            code=code,
        )

        dict_token = self.__process_token(token)

        # tweets
        self.__tweet(dict_token)
        return Response({"message": "Tweeted successfully!"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def refresh(self, request, *args, **kwargs) -> Response:
        """
        Refresh the access token.
        """
        token = self._redis.get("token").decode("utf-8")
        data = self.__process_token(token)

        # for authorization
        encode_string = base64.b64encode(
            str.encode(f"{settings.CLIENT_ID}:{settings.CLIENT_SECRET}")
        ).decode("ascii")

        # refresh the token
        refreshed_token = self._twitter.refresh_token(
            token_url=TOKEN_URL,
            client_id=settings.CLIENT_ID,
            client_secret=settings.CLIENT_SECRET,
            refresh_token=data["refresh_token"],
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"Basic {encode_string}",
            },
        )

        dict_token = self.__process_token(refreshed_token)

        # tweets
        self.__tweet(dict_token)
        return Response({"message": "Tweeted successfully!"}, status=status.HTTP_200_OK)
