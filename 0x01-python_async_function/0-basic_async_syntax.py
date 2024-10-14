#!/usr/bin/env python3
"""
Asynchronous coroutine that waits for a random delay and returns it.
"""
import random
import asyncio


async def wait_random(max_delay: int = 10) -> float:
    """
    Waits for a random delay between 0 and max_delay seconds and returns it.

    Args:
        max_delay (int): The maximum delay in seconds. Defaults to 10.

    Returns:
        float: The actual wait time in seconds.
    """
    wait_time = random.uniform(0, max_delay)
    await asyncio.sleep(wait_time)
    return wait_time
