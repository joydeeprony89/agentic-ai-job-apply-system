"""
Platform-specific asyncio helpers to ensure compatibility across different operating systems.
"""
import asyncio
import sys
import platform
import os
from typing import Callable, Any, List, Tuple, Optional, TypeVar, Coroutine

T = TypeVar('T')

# Check if we're running on Windows
IS_WINDOWS = platform.system() == 'Windows'

# Check Python version
PY_VERSION = sys.version_info

async def sleep(seconds: float) -> None:
    """
    Cross-platform compatible asyncio sleep.
    
    Args:
        seconds: Number of seconds to sleep
    """
    await asyncio.sleep(seconds)

async def gather_with_concurrency(n: int, *tasks) -> List[Any]:
    """
    Run tasks with a concurrency limit.
    
    Args:
        n: Maximum number of concurrent tasks
        tasks: Tasks to run
        
    Returns:
        List of task results
    """
    semaphore = asyncio.Semaphore(n)
    
    async def sem_task(task):
        async with semaphore:
            return await task
    
    return await asyncio.gather(*(sem_task(task) for task in tasks))

async def run_tasks_in_batches(tasks: List[Tuple[str, Coroutine]], batch_size: int, return_exceptions: bool = True) -> List[Tuple[str, Any]]:
    """
    Run tasks in batches with a maximum concurrency.
    
    Args:
        tasks: List of (name, task) tuples
        batch_size: Maximum number of concurrent tasks
        return_exceptions: Whether to return exceptions or raise them
        
    Returns:
        List of (name, result) tuples
    """
    results = []
    
    for i in range(0, len(tasks), batch_size):
        batch = tasks[i:i+batch_size]
        names = [name for name, _ in batch]
        coros = [task for _, task in batch]
        
        batch_results = await asyncio.gather(*coros, return_exceptions=return_exceptions)
        
        for j, result in enumerate(batch_results):
            results.append((names[j], result))
    
    return results

def get_event_loop() -> asyncio.AbstractEventLoop:
    """
    Get the current event loop or create a new one in a cross-platform compatible way.
    
    Returns:
        Event loop
    """
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        # If there's no event loop in the current thread, create one
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop

def run_async(coro: Coroutine) -> Any:
    """
    Run a coroutine in a cross-platform compatible way.
    
    Args:
        coro: Coroutine to run
        
    Returns:
        Result of the coroutine
    """
    loop = get_event_loop()
    return loop.run_until_complete(coro)