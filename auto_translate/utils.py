import os.path as path
import random
import json
import auto_translate.extras as extras
import httpx
from itertools import islice, zip_longest
import threading
import multiprocessing
from typing import Union
import queue

#: Thread Event to cancel threads when necessary
T_EVENT = threading.Event()
#: List of SOCKS5 proxies for client sessions
PROXIES = {}
#: Threading Lock to enter a code section one at a time
T_LOCK = threading.Lock()
#: Proxy Queue which contains all the proxies
PROXY_QUEUE: Union[queue.Queue, multiprocessing.Queue, None] = None
#: Multiprocessing Manager Queue which contains all the proxies
MULTI_PROXY_QUEUE: Union[multiprocessing.Queue, None] = None


def set_proxy_queue(_q: multiprocessing.Queue):
    """
    | Required to call once in the child process if running
    from a multiprocessing environment with create_session() callbacks

    :param _q: Multiprocessing Manager Queue
    :return: None
    """
    global MULTI_PROXY_QUEUE
    if not MULTI_PROXY_QUEUE:
        MULTI_PROXY_QUEUE = _q


def load_proxies(_proxy_q: Union[queue.Queue, multiprocessing.Queue]):
    """
    | Loads the list of HTTP SOCKS 5proxies. Only needs to be loaded once

    :param _proxy_q: Regular Queue or Multiprocessing Manager Queue
    :return:
    """
    # example format for HTTP SOCKS5 proxies:
    # http://user:password@IP:PORT
    with open(path.abspath(path.join(__file__, "../proxies.json")), "r") as f:
        proxies = json.load(f)
        for proxy in proxies:
            _proxy_q.put(proxy)


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
    global PROXY_QUEUE
    if not PROXY_QUEUE and MULTI_PROXY_QUEUE:
        # coming from multiprocessing environment
        PROXY_QUEUE = MULTI_PROXY_QUEUE
    try:
        if T_EVENT.is_set():
            raise InterruptedError(f"Thread execution cancelled!")
        chosen_agent = random.choice(extras.POSSIBLE_AGENTS)
        with T_LOCK:  # ensure that proxies are loaded only once
            if not PROXY_QUEUE or PROXY_QUEUE.empty():
                if not PROXY_QUEUE:
                    # queue was not initialized yet, coming from single process
                    PROXY_QUEUE = queue.Queue()
                load_proxies(PROXY_QUEUE)
        proxy = PROXY_QUEUE.get()
        limits = httpx.Limits(
            max_keepalive_connections=max_alive, max_connections=max_con
        )
        ses = httpx.AsyncClient(
            headers=chosen_agent,
            limits=limits,
            timeout=max_timeout,
            proxies=proxy,
            verify=verify,
            base_url=base_url,
        )
        return ses
    finally:
        # ensure that the proxy reference exists
        if proxy := locals().get("proxy"):
            # add the used proxy back into the queue for later use
            PROXY_QUEUE.put(proxy)


def chunks(data, size):
    it = iter(data)
    for i in range(0, len(data), size):
        yield {k: data[k] for k in islice(it, size)}


def chunk_list_of_tuples(lst, n):
    """Chunk a list of tuples into equally sized list of lists of tuples"""

    def grouper(iterable, n, fillvalue=None):
        "Collect data into fixed-length chunks or blocks"
        args = [iter(iterable)] * n
        return zip_longest(*args, fillvalue=fillvalue)

    return [list(filter(lambda x: x is not None, chunk)) for chunk in grouper(lst, n)]
