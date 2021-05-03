import sys

from distest import TestCollector
from distest import run_dtest_bot

test_collector = TestCollector()


@test_collector()
async def test_ping(interface):
    await interface.assert_reply_contains("M.ping", "Pong!")


if __name__ == "__main__":
    run_dtest_bot(sys.argv, test_collector)
