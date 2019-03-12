
def assert_compare_within(o, o2, within = 0.0001):
    comparison = compare_within_diff(o, o2, within)
    if comparison != None:
        raise Exception(comparison)


def compare_within(o, o2, within = 0.0001):
    if not compare_within_diff(o, o2, within):
        return False
    return True

    

def compare_within_diff(o, o2, within = 0.0001):
    if type(o) != type(o2):
        return "got " + str(type(o)) + " but expected " + str(type(o2))
    else:
        if type(o) == list or type(o) == tuple:
            if len(o) != len(o2):
                return " got length " + str(len(o)) + " but expected length " + str(len(o2))
            for  i in range(len(o)):
                comparison = compare_within_diff(o[i], o2[i], within)
                if comparison != None:
                    return comparison
        elif type(o) == float or type(o) == int:
            if not abs(o2-o) < within:
                return " got " + str(o) + " but expected " + str(o2)
        else:
            raise Exception("not implemented type")    
    return None

