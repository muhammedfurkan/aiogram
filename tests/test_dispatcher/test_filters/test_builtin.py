from datetime import datetime
from typing import Set

import pytest

from aiogram.dispatcher.filters.builtin import (ChatIDArgumentType,
                                                ForwardedMessageFilter,
                                                IDFilter, Text,
                                                extract_chat_ids)
from aiogram.types import Message
from tests.types.dataset import MESSAGE, MESSAGE_FROM_CHANNEL


class TestText:
    @pytest.mark.parametrize(
        "param, key",
        [
            ("text", "equals"),
            ("text_contains", "contains"),
            ("text_startswith", "startswith"),
            ("text_endswith", "endswith"),
        ],
    )
    def test_validate(self, param, key):
        value = "spam and eggs"
        config = {param: value}
        res = Text.validate(config)
        if res != {key: value}:
            raise AssertionError


@pytest.mark.parametrize(
    ("chat_id", "expected"),
    (
        pytest.param(
            "-64856280",
            {
                -64856280,
            },
            id="single negative int as string",
        ),
        pytest.param(
            "64856280",
            {
                64856280,
            },
            id="single positive int as string",
        ),
        pytest.param(
            -64856280,
            {
                -64856280,
            },
            id="single negative int",
        ),
        pytest.param(
            64856280,
            {
                64856280,
            },
            id="single positive negative int",
        ),
        pytest.param(
            ["-64856280"],
            {
                -64856280,
            },
            id="list of single negative int as string",
        ),
        pytest.param(
            [-64856280],
            {
                -64856280,
            },
            id="list of single negative int",
        ),
        pytest.param(
            ["-64856280", "-64856280"],
            {
                -64856280,
            },
            id="list of two duplicated negative ints as strings",
        ),
        pytest.param(
            ["-64856280", -64856280],
            {
                -64856280,
            },
            id="list of one negative int as string and one negative int",
        ),
        pytest.param(
            [-64856280, -64856280],
            {
                -64856280,
            },
            id="list of two duplicated negative ints",
        ),
        pytest.param(
            iter(["-64856280"]),
            {
                -64856280,
            },
            id="iterator from a list of single negative int as string",
        ),
        pytest.param(
            [10000000, 20000000, 30000000],
            {10000000, 20000000, 30000000},
            id="list of several positive ints",
        ),
        pytest.param(
            [10000000, "20000000", -30000000],
            {10000000, 20000000, -30000000},
            id="list of positive int, positive int as string, negative int",
        ),
    ),
)
def test_extract_chat_ids(chat_id: ChatIDArgumentType, expected: Set[int]):
    if extract_chat_ids(chat_id) != expected:
        raise AssertionError


class TestForwardedMessageFilter:
    @pytest.mark.asyncio
    async def test_filter_forwarded_messages(self):
        filter = ForwardedMessageFilter(is_forwarded=True)

        forwarded_message = Message(
            forward_date=round(datetime(2020, 5, 21, 5, 1).timestamp()), **MESSAGE
        )

        not_forwarded_message = Message(**MESSAGE)

        assert await filter.check(forwarded_message)
        if await filter.check(not_forwarded_message):
            raise AssertionError

    @pytest.mark.asyncio
    async def test_filter_not_forwarded_messages(self):
        filter = ForwardedMessageFilter(is_forwarded=False)

        forwarded_message = Message(
            forward_date=round(datetime(2020, 5, 21, 5, 1).timestamp()), **MESSAGE
        )

        not_forwarded_message = Message(**MESSAGE)

        assert await filter.check(not_forwarded_message)
        if await filter.check(forwarded_message):
            raise AssertionError


class TestIDFilter:
    @pytest.mark.asyncio
    async def test_chat_id_for_channels(self):
        message_from_channel = Message(**MESSAGE_FROM_CHANNEL)

        filter = IDFilter(chat_id=message_from_channel.chat.id)

        assert await filter.check(message_from_channel)
