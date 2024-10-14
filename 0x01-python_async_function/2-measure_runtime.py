#!/usr/bin/env python3
"""
Module to measure the runtime of the wait_n coroutine.
"""
import time
import asyncio
from typing import Callable

wait_n = __import__('1-concurrent_coroutines').wait_n


def measure_time(n: int, max_delay: int) -> float:
    """
    Measures the total execution time for wait_n(n, max_delay) and returns total_time / n.

    Args:
        n (int): Number of times to spawn wait_random.
        max_delay (int): The maximum delay for each wait_random call.

    Returns:
        float: Average execution time per call.
    """
    start_time = time.perf_counter()
    asyncio.run(wait_n(n, max_delay))
    end_time = time.perf_counter()
    
    total_time = end_time - start_time
    return total_time / n#!/usr/bin/env python3
"""
Module to measure the runtime of the wait_n coroutine.
"""
import time
import asyncio
from typing import Callable

wait_n = __import__('1-concurrent_coroutines').wait_n


def measure_time(n: int, max_delay: int) -> float:
    """
    Measures the total execution time for wait_n(n, max_delay) and returns total_time / n.

    Args:
        n (int): Number of times to spawn wait_random.
        max_delay (int): The maximum delay for each wait_random call.

    Returns:
        float: Average execution time per call.
    """
    start_time = time.perf_counter()
    asyncio.run(wait_n(n, max_delay))
    end_time = time.perf_counter()
    
    total_time = end_time - start_time
    return total_time / n
