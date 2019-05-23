from .condit import Condit
from . import hdings
import numpy as np

import matplotlib.pyplot as plt


def filter_death(condit: Condit):
    pass


def filter_by_max_value(condit: Condit):
    pass


def filter_outliers(condit: Condit):
    pass


def tall_df_to_frame_df(condit):
    pass


def plot_death_array(condit: Condit, axes):
    if not len(axes) == 4:
        print('in condit#plot_death_array, wrong number of subplots')
        return

    # death_groups = condit.combined_df.groupby(hdings.DEATH)
    # for group in death_groups :
    # death_groups.get_group(0)
    axes[0].get_figure().suptitle(condit.name_str + ' ' + str(condit.wells.keys())[9:])
    axes[0].set_title('unfiltered data')
    # self.frame_df.mean(1).plot(marker='o', linestyle='', ax=ax)

    # condit.combined_df.median(1).plot(marker='o', linestyle='', ax=axes[0])
    cmap = plt.get_cmap('tab20c').colors
    unfiltered_median = condit.combined_df.groupby(hdings.FRAME)[hdings.DIST]
    unfiltered_median.median().plot(marker='o', linestyle='', ax=axes[0], label='median', color=cmap[0])
    unfiltered_median.mean().plot(marker='o', linestyle='', ax=axes[0], label='mean', color=cmap[2])
    axes[0].legend()
    # axes[0].set_xlim(1,50)

    MAX = 50
    filter_by_max_df = condit.combined_df[condit.combined_df[hdings.DIST] <= MAX]
    filter_by_max_df1 = filter_by_max_df.groupby(hdings.FRAME)[hdings.DIST]
    axes[1].plot(filter_by_max_df1.median(), marker='o', linestyle='', color=cmap[0], label='median')
    axes[1].plot(filter_by_max_df1.mean(), marker='o', linestyle='', label='mean', color=cmap[2])
    axes[1].set_title('dist <= {}'.format(MAX))

    filter_by_death_df = filter_by_max_df[filter_by_max_df[hdings.DEATH] != 2]
    # print(filter_by_death_df)
    filter_by_death_df = filter_by_death_df.groupby(hdings.FRAME)[hdings.DIST]
    axes[2].plot(filter_by_death_df.median(), marker='o', linestyle='', label='median', color=cmap[4])
    axes[2].plot(filter_by_death_df.mean(), marker='o', linestyle='', label='mean', color=cmap[6])
    axes[2].set_title('dist <= {}, and removed death'.format(MAX))
    axes[2].legend()

    frame_groups = filter_by_max_df.groupby(hdings.FRAME)
    cnts = {'death': [], 'mitotic': [], 'live': [], 'frames': []}

    frame = 1
    for k, g in frame_groups:
        group = g.groupby(hdings.DEATH)
        # print(group.groups)
        try:
            cnts['death'].append(group.get_group(2)[hdings.DIST].count())
        except:
            cnts['death'].append(0)
        try:
            cnts['mitotic'].append(group.get_group(1)[hdings.DIST].count())
        except:
            cnts['mitotic'].append(0)
        try:
            cnts['live'].append(group.get_group(0)[hdings.DIST].count())
        except:
            cnts['live'].append(0)
        cnts['frames'].append(frame)
        frame += 1
    print(cnts)
    temp_dead_col = [l + d for l, d in zip(cnts['live'], cnts['death'])]
    temp_mit_col = [d + m for d, m in zip(temp_dead_col, cnts['mitotic'])]

    axes[3].fill_between(cnts['frames'], temp_dead_col, y2=cnts['live'], step='mid', label='dead', color=cmap[0])
    axes[3].fill_between(cnts['frames'], temp_mit_col, y2=temp_dead_col, step='mid', label='mitotic', color=cmap[8])
    axes[3].fill_between(cnts['frames'], cnts['live'], step='mid', label='live', color=cmap[4])

    axes[3].legend()
    axes[3].set_ylim(0, 60)

    # print('okay?')
    for ax in axes[:3]:
        ax.set_ylim(1, 25)
        ax.set_ylabel('Median distance (pixels)')
        ax.set_xlabel('Frame number')  # print('okay.')
        ax.legend()

    # print('better be')

def plot2(condit: Condit, axes):
    if not len(axes) == 4:
        print('in condit#plot_death_array, wrong number of subplots')
        return

    # death_groups = condit.combined_df.groupby(hdings.DEATH)
    # for group in death_groups :
    # death_groups.get_group(0)
    axes[0].get_figure().suptitle(condit.name_str + ' ' + str(condit.wells.keys())[9:])
    axes[0].set_title('unfiltered data')
    # self.frame_df.mean(1).plot(marker='o', linestyle='', ax=ax)

    # condit.combined_df.median(1).plot(marker='o', linestyle='', ax=axes[0])
    cmap = plt.get_cmap('tab20c').colors
    unfiltered_median = condit.combined_df.groupby(hdings.FRAME)[hdings.DIST]
    subplot2(unfiltered_median,axes[0],cmap[0])
    # axes[0].set_xlim(1,50)

    MAX = 50
    filter_by_max_df = condit.combined_df[condit.combined_df[hdings.DIST] <= MAX]
    filter_by_max_df1 = filter_by_max_df.groupby(hdings.FRAME)[hdings.DIST]
    subplot2(filter_by_max_df1,axes[1],cmap[0])

    axes[1].set_title('dist <= {}'.format(MAX))

    filter_by_death_df = filter_by_max_df[filter_by_max_df[hdings.DEATH] != 2]
    # print(filter_by_death_df)
    filter_by_death_df = filter_by_death_df.groupby(hdings.FRAME)[hdings.DIST]

    subplot2(filter_by_death_df,axes[2],cmap[4])
    axes[2].set_title('dist <= {}, and removed death'.format(MAX))

    frame_groups = filter_by_max_df.groupby(hdings.FRAME)
    cnts = {'death': [], 'mitotic': [], 'live': [], 'frames': []}

    frame = 1
    for k, g in frame_groups:
        group = g.groupby(hdings.DEATH)
        # print(group.groups)
        try:
            cnts['death'].append(group.get_group(2)[hdings.DIST].count())
        except:
            cnts['death'].append(0)
        try:
            cnts['mitotic'].append(group.get_group(1)[hdings.DIST].count())
        except:
            cnts['mitotic'].append(0)
        try:
            cnts['live'].append(group.get_group(0)[hdings.DIST].count())
        except:
            cnts['live'].append(0)

        cnts['frames'].append(frame)
        frame += 1
    print(cnts)
    temp_dead_col = [l + d for l, d in zip(cnts['live'], cnts['death'])]
    temp_mit_col = [d + m for d, m in zip(temp_dead_col, cnts['mitotic'])]

    axes[3].fill_between(cnts['frames'], temp_dead_col, y2=cnts['live'], step='mid', label='dead', color=cmap[0])
    axes[3].fill_between(cnts['frames'], temp_mit_col, y2=temp_dead_col, step='mid', label='mitotic', color=cmap[8])
    axes[3].fill_between(cnts['frames'], cnts['live'], step='mid', label='live', color=cmap[4])

    axes[3].legend()
    axes[3].set_ylim(0, 60)

    # print('okay?')
    # for ax in axes[:3]:
    #     ax.set_ylim(1, 25)
    #     ax.set_ylabel('Median distance (pixels)')
    #     ax.set_xlabel('Frame number')  # print('okay.')
    #     ax.legend()
    # print('better be')

def subplot2(dist_df, ax, co):
    dist_df_stats = dist_df.describe()
    print(dist_df_stats.index)
    print(dist_df_stats.columns)
    # print(co)
    # print([*co,.5])
    dist_df_stats['50%'].plot(marker='o',
                                 linestyle='',
                                 ax=ax,
                                 label='median',
                                 color=co)

    dist_df_stats['75%'].plot(marker='o',
                                 linestyle='',
                                 ax=ax,
                                 label='upper and lower quartiles',
                                 color=(*co,.5),
                              markeredgewidth=0)

    dist_df_stats['25%'].plot(marker='o',
                                 linestyle='',
                                 ax=ax,
                                 label='',
                                 color=(*co,.5),
                              markeredgewidth=0)

    ax.legend()
    # ax.plot(list(range(85)),[30]*85)
    ax.set_ylim(1, 25)
    ax.set_ylabel('Median distance (pixels)')
    ax.set_xlabel('Frame number')  # print('okay.')
    ax.legend()
