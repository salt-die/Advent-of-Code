def prod(iter, *, start=1, cast=int):
    """This version of product made to cast numpy types to python types so we don't have to worry about overflows.
    """
    m = start
    for i in iter:
        m *= cast(i)
    return m