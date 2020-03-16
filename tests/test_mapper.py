import graphql
import pytest
from graphql.utilities import is_equal_type
from mygraphql.mapper import MAPPER


class NOT_AN_INT: pass


def test_mapping_int():
    assert is_equal_type(
        MAPPER.map(int),
        graphql.GraphQLNonNull(graphql.GraphQLInt)
    )


def test_overriding_int():
    def new_int_mapper(mapper, ty):
        if ty is int:
            return NOT_AN_INT

    local_mapper = MAPPER.new()
    local_mapper.add_mapper(new_int_mapper)

    assert is_equal_type(
        MAPPER.map(int),
        graphql.GraphQLNonNull(graphql.GraphQLInt)
    )
