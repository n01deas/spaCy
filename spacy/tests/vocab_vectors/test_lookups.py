# coding: utf-8
from __future__ import unicode_literals

import pytest
from spacy.lookups import Lookups
from spacy.vocab import Vocab

from ..util import make_tempdir


def test_lookups_api():
    table_name = "test"
    data = {"foo": "bar", "hello": "world"}
    lookups = Lookups()
    lookups.add_table(table_name, data)
    assert len(lookups) == 1
    assert table_name in lookups
    assert lookups.has_table(table_name)
    table = lookups.get_table(table_name)
    assert table.name == table_name
    assert len(table) == 2
    assert table.get("hello") == "world"
    table.set("a", "b")
    assert table.get("a") == "b"
    table = lookups.get_table(table_name)
    assert len(table) == 3
    with pytest.raises(KeyError):
        lookups.get_table("xyz")
    with pytest.raises(ValueError):
        lookups.add_table(table_name)
    table = lookups.remove_table(table_name)
    assert table.name == table_name
    assert len(lookups) == 0
    assert table_name not in lookups
    with pytest.raises(KeyError):
        lookups.get_table(table_name)


# This fails on Python 3.5
@pytest.mark.xfail
def test_lookups_to_from_bytes():
    lookups = Lookups()
    lookups.add_table("table1", {"foo": "bar", "hello": "world"})
    lookups.add_table("table2", {"a": 1, "b": 2, "c": 3})
    lookups_bytes = lookups.to_bytes()
    new_lookups = Lookups()
    new_lookups.from_bytes(lookups_bytes)
    assert len(new_lookups) == 2
    assert "table1" in new_lookups
    assert "table2" in new_lookups
    table1 = new_lookups.get_table("table1")
    assert len(table1) == 2
    assert table1.get("foo") == "bar"
    table2 = new_lookups.get_table("table2")
    assert len(table2) == 3
    assert table2.get("b") == 2
    assert new_lookups.to_bytes() == lookups_bytes


# This fails on Python 3.5
@pytest.mark.xfail
def test_lookups_to_from_disk():
    lookups = Lookups()
    lookups.add_table("table1", {"foo": "bar", "hello": "world"})
    lookups.add_table("table2", {"a": 1, "b": 2, "c": 3})
    with make_tempdir() as tmpdir:
        lookups.to_disk(tmpdir)
        new_lookups = Lookups()
        new_lookups.from_disk(tmpdir)
    assert len(new_lookups) == 2
    assert "table1" in new_lookups
    assert "table2" in new_lookups
    table1 = new_lookups.get_table("table1")
    assert len(table1) == 2
    assert table1.get("foo") == "bar"
    table2 = new_lookups.get_table("table2")
    assert len(table2) == 3
    assert table2.get("b") == 2


# This fails on Python 3.5
@pytest.mark.xfail
def test_lookups_to_from_bytes_via_vocab():
    table_name = "test"
    vocab = Vocab()
    vocab.lookups.add_table(table_name, {"foo": "bar", "hello": "world"})
    assert len(vocab.lookups) == 1
    assert table_name in vocab.lookups
    vocab_bytes = vocab.to_bytes()
    new_vocab = Vocab()
    new_vocab.from_bytes(vocab_bytes)
    assert len(new_vocab.lookups) == 1
    assert table_name in new_vocab.lookups
    table = new_vocab.lookups.get_table(table_name)
    assert len(table) == 2
    assert table.get("hello") == "world"
    assert new_vocab.to_bytes() == vocab_bytes


# This fails on Python 3.5
@pytest.mark.xfail
def test_lookups_to_from_disk_via_vocab():
    table_name = "test"
    vocab = Vocab()
    vocab.lookups.add_table(table_name, {"foo": "bar", "hello": "world"})
    assert len(vocab.lookups) == 1
    assert table_name in vocab.lookups
    with make_tempdir() as tmpdir:
        vocab.to_disk(tmpdir)
        new_vocab = Vocab()
        new_vocab.from_disk(tmpdir)
    assert len(new_vocab.lookups) == 1
    assert table_name in new_vocab.lookups
    table = new_vocab.lookups.get_table(table_name)
    assert len(table) == 2
    assert table.get("hello") == "world"
