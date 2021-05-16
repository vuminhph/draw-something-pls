def overrides(interface_class):
    """
    This function allows any method to be marked as overridden 
    if implementing an interface, by typing:

    @overrides(interface_class)

    above the method definition.
    """
    def overrider(method):
        assert(method.__name__ in dir(interface_class))
        return method
    return overrider


def singleton(class_):
    """
    Define an Instance operation that lets clients access its instance.
    """
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance
