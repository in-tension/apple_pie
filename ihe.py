import apple_pie as ap
import brutils as br

exp = ap.make_cur_exper()

condit = br.one_value(exp.condits)
well = br.one_value(condit.wells)

well.plot_looper()
# def some_condition(cur_group) :
#     if len(cur_group) <= 5 :
#         return False
#     else :
#         return True
# dfpl = br.DfPlotLooper2(well.cdf2, ap.hdings.T_ID, ap.hdings.FRAME, ap.hdings.DIST, title=str(well), some_condition=some_condition)