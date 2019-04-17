import pandas as pd
import brutils as br
import numpy as np
import apple_pie as ap
import brutils as br


well_file = '/Volumes/baylieslab/Current Lab Members/Whitney/Rhabdo Project/Tissue Culture/Timelapse/Rhabdomyosarcoma plate movies/Post-mycoplasma data (starting 9:18:18)/RH30/18-11-07.rht/Csv/B02.csv'

well_name = 'B02'

w = ap.Well('exper',well_name,well_file)

cd_tic = br.dtic('create_dists one well')
# w.create_dists()

inputt = None
output = None

for i,g in w.cdf.groupby(ap.hdings.T_ID) :
    inputt = g
    ouptut = br.create_df_dists2(g,ap.hdings.X,ap.hdings.Y,ap.hdings.DIST,ap.hdings.FRAME)

    break

print(output)


# br.dtoc(cd_tic)

