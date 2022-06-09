"""Setup policies for Windows env

problem: https://github.com/encode/httpx/issues/914
"""


import sys
import asyncio


def setup_policies():
    """Setup policies for Windows environment
    """
    if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
