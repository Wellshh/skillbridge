# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
"""Generic data structures for high-level remote collections."""

from __future__ import annotations

from collections.abc import Iterator
from typing import (
    Generic,
    TypeVar,
    cast,
    overload,
)

from allegrobridge.client.base._rpc import SessionApi as _Base
from allegrobridge.exceptions import AllegroProtocolError

T = TypeVar('T')
K = TypeVar('K')
D = TypeVar('D')


class _Collection(_Base, Generic[T]):
    """Generic base class for remote object collections.

    Provides standardized collection access protocols including explicit snapshotting,
    direct iteration, and guards against implicit truth value checks to prevent unintentional
    remote queries.

    Type Parameters:
        T: The record type representing individual items in the remote collection.
    """

    def _snapshot(self) -> list[T]:
        raise NotImplementedError

    def snapshot(self) -> list[T]:
        """Fetches a full snapshot of remote records in a single RPC roundtrip.

        Returns:
            A list of strongly-typed records retrieved from the remote session.
        """
        return self._snapshot()

    def __iter__(self) -> Iterator[T]:
        """Iterates over a snapshot of the remote collection.

        Yields:
            Individual records from the freshly fetched snapshot.
        """
        return iter(self.snapshot())

    def __bool__(self) -> bool:
        """Prevents implicit boolean evaluation of the remote collection.

        Raises:
            TypeError: Always raised to disallow implicit truth checking without snapshot().
        """
        raise TypeError('remote collections have no local truth value; use snapshot()')


class _KeyedCollection(_Collection[T], Generic[K, T]):
    """Generic base class for key-addressable remote object collections.

    Extends `_Collection` to provide mapping semantics (such as bracket indexing,
    safe `.get()`, and membership tests `in`) for entities indexed by a primary key
    (e.g., component `refdes` or net `name`).

    Type Parameters:
        K: The primary key type used to look up records (e.g. str).
        T: The record type representing individual items in the remote collection.
    """

    def _query_key(self, key: K) -> list[T]:
        raise NotImplementedError

    def __getitem__(self, key: K) -> T:
        """Retrieves a single record matching the given primary key.

        Args:
            key: The primary identifier of the entity to retrieve.

        Returns:
            The matching record.

        Raises:
            KeyError: If no record matches the given key.
            AllegroProtocolError: If more than one record matches the given key.
        """
        items = self._query_key(key)
        if not items:
            raise KeyError(key)
        if len(items) > 1:
            raise AllegroProtocolError(f'multiple records match {key!r}')
        return items[0]

    @overload
    def get(self, key: K) -> T | None: ...

    @overload
    def get(self, key: K, default: D) -> T | D: ...

    def get(self, key: K, default: D | None = None) -> T | D | None:
        """Safely retrieves a record by key, returning a default value if not found.

        Args:
            key: The primary identifier of the entity to retrieve.
            default: The fallback value returned when the key does not exist.

        Returns:
            The matching record if found, otherwise `default`.
        """
        try:
            return self[key]
        except KeyError:
            return default

    def __contains__(self, key: object) -> bool:
        """Checks whether an entity with the given primary key exists in the remote database.

        Args:
            key: The primary identifier to check.

        Returns:
            True if the entity exists, False otherwise.
        """
        try:
            self[cast('K', key)]
        except KeyError:
            return False
        return True
