import sys


def tracefunc(frame, event, arg, indent=[0]):
    if event == "call":
        print(frame.f_code)
        print(type(frame.f_code.__doc__))

    return



sys.settrace(tracefunc)

# c = 10
