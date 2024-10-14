#!/usr/bin/env python3
"""
Module to create an asyncio Task from wait_random coroutine.
"""
import asyncio
from typing import Callable

wait_random = __import__('0-basic_async_syntax').wait_random


def task_wait_random(max_delay: int) -> asyncio.Task:
    """
    Creates and returns an asyncio.Task for wait_random coroutine.

    Args:
        max_delay (int): The maximum delay to pass to wait_random.

    Returns:
        asyncio.Task: A Task object wrapping the wait_random coroutine.
    """
    return asyncio.create_task(wait_random(max_delay))
