

def compare_within(o, o2, within = 0.0001):
    if type(o) != type(o2):
        return False
    else:
        if type(o) == list or type(o) == tuple:
            if len(o) != len(o2):
                return False
            for  i in range(len(o)):
                if not compare_within(o[i], o2[i], within):
                    return False
        elif type(o) == float or type(o) == int:
            if not abs(o2-o) < within:
                return False
        else:
            raise Exception("not implemented type")    
    return True
                
