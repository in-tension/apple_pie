import apple_pie as ap

import brutils as br
import importlib as imp


def reload(package) :
    d=br.dtic('reload')
    import os
    imp.reload(package)
    for key, val in package.__dict__.items():
        if type(val) == type(os) :

            imp.reload(val)
            print(key)
    imp.reload(package)
    br.dtoc(d)

def reload_exp(exp) :
    #temp = ap
    reload(ap)

    return ap.Exper.make_from_existing(exp)
# print('dafuq')
if True :
    exp = ap.make_cur_exper()

    br.PlotLooper3(exp)




    condit = br.one_value(exp.condits)
    well = exp.wells['B19']
#
# well.plot_looper()
# def some_condition(cur_group) :
#     if len(cur_group) <= 5 :
#         return False
#     else :
#         return True
# dfpl = br.DfPlotLooper2(well.cdf2, ap.hdings.T_ID, ap.hdings.FRAME, ap.hdings.DIST, title=str(well), some_condition=some_condition)