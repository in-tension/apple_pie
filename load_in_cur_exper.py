
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
    d=br.dtic('reload_exp')
    reload(ap)
    reload(br)

    temp =  ap.Exper.make_from_existing(exp)
    br.dtoc(d)
    return temp

exper = ap.make_cur_exper()
condit = br.one_value(exper.condits)

