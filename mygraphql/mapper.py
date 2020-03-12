import graphql


class Mapper:

    def __init__(self, parent=None):
        self.parent = parent
        self.mappers = []

    def add_mapper(self, fn):
        self.mappers.append(fn)

    def new(self):
        return Mapper(self)

    def _map(self, orig_mapper, desc):
        for fn in self.mappers:
            result = fn(orig_mapper, desc)
            if result is not None:
                return result
        if self.parent is not None:
            return self.parent._map(orig_mapper, desc)


    def map(self, desc):
        mapped = self._map(self, desc)
        if mapped is None:
            raise ValueError(f'Could not map {desc} to graphql type')
        return mapped


MAPPER = Mapper()

_SCALAR_MAPS = {
    int: graphql.GraphQLInt,
    float: graphql.GraphQLFloat,
    str: graphql.GraphQLString,
    bool: graphql.GraphQLBoolean,
}

@MAPPER.add_mapper
def map_scalars(ty):
    return _SCALAR_MAPS.get(ty)