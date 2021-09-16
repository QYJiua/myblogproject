def wrapper_out1(f):
    print('out1========')
    def inner(*args, **kwargs):
        print('in1==========')
        ret = f(*args, **kwargs)
        print('in2=============')
    print('out1=========')
    return inner

def wrapper_out2(f):
    print('out2**************')
    def inner(*args, **kwargs):
        print('in2**********')
        ret = f(*args, **kwargs)
        print('in2*************')
    print('out2*************')
    return inner

@wrapper_out2
@wrapper_out1
def test():
    print('-----test--------')
    return 1

if __name__ == '__main__':
    test()