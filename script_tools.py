
import matplotlib.pyplot as plt



def timelapse_plot_formating(ax,ymax=None) :
    ax.set_xlim(0,85)
    if not ymax == None :
        ax.set_ylim(0,ymax)

    ax.set_xlabel('Time (frames = 10min)')
    ax.set_ylabel('Displacement (pixels)')



