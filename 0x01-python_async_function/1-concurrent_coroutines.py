#!/usr/bin/env python3
"""
Asynchronous routine that spawns wait_random n times with specified max_delay
and returns list of delays in ascending order.
"""
import asyncio
from typing import List

wait_random = __import__('0-basic_async_syntax').wait_random

async def wait_n(n: int, max_delay: int) -> List[float]:
    """
    Spawns wait_random n times with the specified max_delay.

    Args:
        n (int): Number of times to spawn wait_random.
        max_delay (int): The maximum delay for each wait_random call.

    Returns:
        List[float]: List of all delays in ascending order.
    """
    tasks = [wait_random(max_delay) for _ in range(n)]
    delays = []
    
    for future in asyncio.as_completed(tasks):
        delay = await future
        delays.append(delay)
    
    return delays
