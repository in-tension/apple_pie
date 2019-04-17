
global butts
def tracefunc(frame, event, arg, indent=[0]):
    global butts
    butts = frame
    IND = 1
    if event == "call":

        # indent[0] += 2
        indent[0] += IND
        #print(' '*indent[0])
        #print(''.format(frame.f_code))

        # print("-" * indent[0] + "> call function", frame.f_code.co_name)
        #print('{}> call function {}, f_code: {}'.format(indent[0]*'-',frame.f_code.co_name, frame))
    elif event == "return":
        #print(' '*indent[0])
        # print("<" + "-" * indent[0], "exit function", frame.f_code.co_name)
        #print('<{} exit function {}'.format(indent[0]*'-',frame.f_code.co_name))
        indent[0] -= IND
    return


import sys

sys.settrace(tracefunc)

c = 10

#
# import importlib
# from importlib.abc import MetaPathFinder
#
# class AutoPackageReloader(MetaPathFinder) :
#
#     def find_spec(fullname,path,target) :
#         print("AutoPackInstaller.find_spec")
#         if fullname in sys.modules :
#             importlib.reload(fullname)
#         # print('fullname: {}'.format(fullname))
#         # print('path: {}'.format(path))
#         # print('target: {}'.format(target))
#         return None
#
#
#
#
#
#
# # sys.meta_path.append(AutoPackageReloader)
#
# sys.meta_path.insert(0,AutoPackageReloader)
# print(sys.meta_path)
#
# import csv
import csv

# print(csv.__dict__.keys())