import logging
import os
import random
import socket
import string
import traceback
from contextlib import closing

from aiohttp import web
from aiohttp.web_exceptions import HTTPForbidden
from aiohttp.web_request import Request
from subprocess import Popen

from aiohttp.web_response import json_response

last_port = 37000


def check_auth(request):
    auth = request.headers.get("Authorization", "")
    if auth.upper() != "Token freibzghn78034z4fnb43u80gfzhbun9034h7u0bngh430".upper():  # high security because the token is very long, much bits
        raise HTTPForbidden()


def find_free_ports():
    global last_port
    last_port += 2
    if last_port >= 38000:
        last_port = 37000
    return last_port - 1, last_port - 2


async def device_proxy(request: Request):
    check_auth(request)
    master, consumer = find_free_ports()
    secretkey = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
    Popen(["python3", "master.py",
           "-m", "0.0.0.0:{}".format(master),
           "-c", "0.0.0.0:{}".format(consumer),
           "-k", secretkey])
    return json_response(data={
        "master": master,
        "consumer": consumer,
        "secretkey": secretkey
    })

async def restart(request: Request):
    check_auth(request)
    os._exit(1)


def main():
    # logging setup
    logging.getLogger(__name__).addHandler(logging.NullHandler())
    app = web.Application(middlewares=[])
    app.router.add_route("GET", "/mastermaster", device_proxy)
    app.router.add_route("GET", "/masterblaster", restart)

    web.run_app(app, host="0.0.0.0", port="8080")
    # quit
    # noinspection PyProtectedMember
    os._exit(0)


if __name__ == "__main__":
    try:
        main()
    except:
        traceback.print_exc()
    finally:
        # quit
        # noinspection PyProtectedMember
        os._exit(1)
