import pytest
import graphql

from mygraphql.mapper import MAPPER

class NOT_AN_INT: pass


def test_mapping_int():
    assert MAPPER.map(int) is graphql.GraphQLInt


def test_overriding_int():
    def new_int_mapper(ty):
        if ty is int:
            return NOT_AN_INT

    local_mapper = MAPPER.new()
    local_mapper.add_mapper(new_int_mapper)

    assert MAPPER.map(int) is graphql.GraphQLInt
    assert local_mapper.map(int) is NOT_AN_INT

