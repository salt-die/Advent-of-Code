def glen(generator):
    """
    len implementation for generators.
    """
    return sum(1 for _ in generator)