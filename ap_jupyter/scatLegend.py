#!/usr/bin/env python
# coding: utf-8

# In[1]:


## ScatLegend is based off a barplot legend widget written by DougRzz
## original code from https://github.com/DougRzz/Vaex-demo-notebook/blob/master/VAEX_interactive.ipynb
## github author: DougRzz https://github.com/DougRzz 


# In[2]:


import numpy as np
import ipywidgets as widgets
import bqplot as bq
from IPython.display import display as idisp


# In[5]:


class ScatLegend(object):
    """
    A legend widget using a horizontal bar chart for marks made of Scatter
    
    fig: fig with scatter marks 
    
    marks must have legend labels 
    (in mark, remove other legend by using: display_legend = False)
    
    usage:
        legend = ScatLegend(fig) 
        hb = ipywidgets.HBox(legend,fig)
        IPython.display.display(hb)
    """
    
    OPAC_DIM = 0.1     ## opacity values
    OPAC_BRIGHT = 1
    
    
    def __init__(self, lineFig):
        """
        """
        
        self.lineFig = lineFig
        self.marks = self.lineFig.marks
        y_ord = bq.OrdinalScale()
        x_sc = bq.LinearScale()
        
        legendLabels = []
        self.colours = [] 
        for mark in self.marks:            
            legendLabels += mark.labels
            self.colours += mark.colors[:len(mark.labels)]

        self.bars = bq.Bars(
            y=[1]*len(legendLabels) , # all bars have a amplitude of 1    ## ?
            x=legendLabels, 
            scales={'y': x_sc, 'x': y_ord},
            colors=self.colours ,
            padding = 0.6,
            orientation='horizontal',
            stroke = 'white')  ## remove the black border around the bar
            
        
        
        self.bars.opacities = [ScatLegend.OPAC_BRIGHT] * len(self.bars.x)
        
        ax_y = bq.Axis(scale=y_ord, orientation="vertical")
        ax_x = bq.Axis(scale=x_sc)
        ax_x.visible = False
        margin = dict(top=40, bottom=0, left=110, right=5)
        self.fig = bq.Figure(marks=[self.bars], axes=[ax_y, ax_x], fig_margin=margin)
        
        # Variable height depending on number of bars in legend
        self.fig.layout.height = str(45 + 20 * len(legendLabels)) + 'px'
        self.fig.layout.width = '170px'

        self.fig.min_aspect_ratio = 0.000000000001 # effectively remove aspect ratio constraint
        self.fig.max_aspect_ratio = 999999999999999 # effectively remove aspect ratio constraint
        self.fig.background_style = {'fill': 'White'}   
                    
        self.bars.on_element_click(self.changeOpacity)

        
    def changeOpacity(self, bars, target):
        """
        """
        sigNum = target['data']['index']

        if bars.opacities[sigNum] == ScatLegend.OPAC_BRIGHT :
            bars.opacities=bars.opacities[:sigNum] + [ScatLegend.OPAC_DIM] + bars.opacities[sigNum+1:]
            self.marks[sigNum].visible = False
        else:
            bars.opacities=bars.opacities[:sigNum] + [ScatLegend.OPAC_BRIGHT] + bars.opacities[sigNum+1:] 
            self.marks[sigNum].visible = True

