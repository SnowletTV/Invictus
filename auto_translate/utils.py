import os.path as path
import random
import json
import auto_translate.extras as extras
import httpx
from itertools import islice


def create_session(
        max_alive: int = 5,
        max_con: int = 30,
        max_timeout: int = 50,
        verify: bool = True,
        base_url: str = "",
):
    """
    | Creates the HTTPX session to handle requests. Supports asynchronous sessions.
    | SOCK5 Proxy protection is activated for the asynchronous session

    :param int max_alive: Number of maximum alive connections. 5 by default
    :param int max_con: Number of maximum allowed connections at once. 30 by default
    :param int max_timeout: Time in seconds before raising a timeout error. 50 by default
    :param bool verify: SSL verification, whether client should verify or not. True by default
    :param str base_url:  A URL to use as the base when building request URLs.
    :return: HTTPX Session
    """
    with open(path.abspath(path.join(__file__, "../proxies.json")), "r") as f:
        proxies = json.load(f)
    chosen_agent = random.choice(extras.POSSIBLE_AGENTS)
    chosen_proxy = random.choice(proxies)
    limits = httpx.Limits(
        max_keepalive_connections=max_alive, max_connections=max_con
    )
    ses = httpx.AsyncClient(
        headers=chosen_agent,
        limits=limits,
        timeout=max_timeout,
        proxies=chosen_proxy,
        verify=verify,
        base_url=base_url,
    )
    return ses


def chunks(data, size):
    it = iter(data)
    for i in range(0, len(data), size):
        yield {k: data[k] for k in islice(it, size)}
