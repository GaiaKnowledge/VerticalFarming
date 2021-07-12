def env(x,y):
    if x.__class__.__name__ == 'Pbox':
        return x.env(y)
    elif y.__class__.__name__ == 'Pbox':
        return y.env(x)
    else:
        raise NotImplementedError('At least one argument needs to be a Pbox')

def min(x,y):
    if x.__class__.__name__ == 'Pbox':
        return x.min(y)
    if y.__class__.__name__ == 'Pbox':
        return y.min(x)
    else:
        raise NotImplementedError('At least one argument needs to be a Pbox')

def max(x,y):
    if x.__class__.__name__ == 'Pbox':
        return x.max(y)
    if y.__class__.__name__ == 'Pbox':
        return y.max(x)
    else:
        raise NotImplementedError('At least one argument needs to be a Pbox')
