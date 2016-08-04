# Do not import models here because these procedures are used from command line
# scripts.  Pass the model class as an argument instead.

def zip_default(keys, values, default=' '):
    '''
    Zips two lists into a dictionary.  But, contrary to plain `zip`, if the
    list containing the keys is longer then the list containing the values add
    the `default` value as the value for the remaining keys.
    '''
    while len(keys) > len(values):
        values.append(default)
    return dict(zip(keys, values))

def diff_list(left, right):
    '''
    Compute set difference of lists, but keeps the order of fields in the left
    operand (a real set difference would ignore order).
    '''
    for i in right:
        if i in left:
            left.remove(i)
    return left

def remove_abstract_fields(cls, abs, extra=None):
    '''
    Remove the abstract model fields from a subclass of it.

    Accept extra fields to remove too.
    '''
    fields = list(map(lambda x: x.name, cls._meta.get_fields()))
    ignore = list(map(lambda x: x.name, abs._meta.get_fields()))
    if extra:
        ignore += extra
    return diff_list(fields, ignore)

def get_model(model, pk=None):
    '''
    Try to get a workable instance.  If we get a primary key number try that,
    if we get a string try to convert it into a number, if we get nothing
    create a new instance.  If we get total garbage just error.
    '''
    if str == type(pk):
        try:
            pk = int(pk)
        except ValueError:
            return None
    if type(None) == type(pk):
        inst = model()
    elif int == type(pk):
        try:
            inst = model.objects.get(id=pk)
        except model.DoesNotExist:
            # make a new instance if the one provided does not exist
            inst = model()
    else:
        return None
    return inst

def get_new_model(model, pk=None):
    '''
    Wraper around `get_model` for models with a `processed` field.  This works
    because all models in this package have the `processed` field.  This is
    most often used to get a batch, either by number or a new one if the batch
    number cannot be used.
    '''
    inst = get_model(model, pk)
    if hasattr(inst, 'processed') and inst.processed:
        # and make a new one if the provided one has already been used
        inst = model()
    return inst

