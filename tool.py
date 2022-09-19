def is_num(x):
    try:
        float(x)
    except ValueError:
        return False
    else:
        return True