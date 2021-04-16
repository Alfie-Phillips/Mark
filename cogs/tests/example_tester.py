import asyncio
import sys
import asyncio
import sys
from distest import TestCollector
from distest import run_dtest_bot
from discord import Embed, Member, Status
from distest import TestInterface


test_collector = TestCollector()

@test_collector()
async def test_ping(interface):
    await interface.assert_reply_contains("M.ping", "Pong!")

if __name__ == "__main__":
    run_dtest_bot(sys.argv, test_collector)