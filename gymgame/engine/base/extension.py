import types

def extension(cls):

    def decorate_extension(ext_cls):
        dict = ext_cls.__dict__
        for k, v in dict.items():
            if type(v) is not types.MethodType and type(v) is not types.FunctionType:
                continue
            setattr(cls, k, v)
        return ext_cls

    return decorate_extension