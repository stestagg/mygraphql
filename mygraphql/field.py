from inspect import Signature, signature

import graphql


def arg_from_parameter(mapper, param):
    default_value = param.default
    if default_value is Signature.empty:
        default_value = param.default
    return graphql.GraphQLArgument(
        mapper.map(param.annotation),
        default_value=default_value
    )

def make_resolver(fn):
    def resolve(obj, info, **args):
        return fn(**args)
    return resolve

def field_from_fn(mapper, fn_desc):
    sig = signature(fn_desc.fn)
    if sig.return_annotation is Signature.empty:
        raise ValueError('graphql functions must provide return type')
    result_type = mapper.map(sig.return_annotation)
    arg_types = {
        param.name: arg_from_parameter(mapper, param)
        for param in sig.parameters.values()
    }
    return graphql.GraphQLField(result_type, args=arg_types, resolve=make_resolver(fn_desc.fn))
