# endcoding: utf-8

'''
Created by
@author: Dianyi Hu
@date: 2023/12/21 
@time: 03:12
'''


from matplotlib.ticker import MaxNLocator
from seaborn import boxplot, violinplot, heatmap, kdeplot, barplot, move_legend, color_palette

from matplotlib.pyplot import setp
import matplotlib.colors as colors


gssmd_cmap = colors.ListedColormap(['green','yellow','red'])
gssmd_boundaries = [0,0.6,0.8,1]
gssmd_norm = colors.BoundaryNorm(gssmd_boundaries, gssmd_cmap.N, clip=True)


def analysis_fig_1(fig, df, x, y, hue=None):
    axe = fig.add_axes([0.13, 0.22, 0.65, 0.65])
    violinplot(data=df, x=x, y=y, hue=hue, split=True, inner=None, palette='Set2', ax=axe)
    setp(axe.collections, alpha=0.5)
    boxplot(data=df, x=x, y=y, palette='Set2', boxprops={'facecolor':(.4,.6,.8,.0)}, width=0.1, linewidth=1, ax=axe)
    if hue:
        move_legend(axe, 'upper_left', bbox_to_anchor=(1.03,1), frameon=False)


def analysis_fig_2(fig, df, x, y, hue):
    axe = fig.add_axes([0.13, 0.22, 0.65, 0.65])
    boxplot(data=df, x=x, y=y, hue=hue, palette='Set3', ax=axe)
    move_legend(axe, 'upper left', bbox_to_anchor=(1.03,1), frameon=False)


def analysis_fig_3(fig, df, x, y, hue):
    axe = fig.add_axes([0.13, 0.22, 0.65, 0.65])
    df_temp = df.pivot(hue, x, y)
    heatmap(df_temp, ax=axe, cmap=gssmd_cmap, norm=gssmd_norm, linewidths=0.5)


def analysis_fig_4(fig, df, hue):
    cat_dict = {}
    rescale_dict = {}

    col_hue = df.pop(hue)
    df.insert(df.shape[1], hue, col_hue)

    for index, col in df.items():
        if col.dtypes == 'object':
            col_catdict = {}
            obj_list = col.unique().to_list()
            obj_list.sort()
            for id, element in enumerate(obj_list):
                col_catdict.update({element: (id + 1) / (len(obj_list)+1)})
            df[index] = col.map(col_catdict)
            cat_dict.update({index: col_catdict})


    min_cat_cols = df[cat_dict.keys()].min().min()
    max_cat_cols = df[cat_dict.keys()].max().max()
    for index, col in df.items():
        if index in col_catdict.keys():
            df[index] = (col-min_cat_cols)/(max_cat_cols-min_cat_cols)
            rescale_dict.update({index: {'length': max_cat_cols, 'x0': min_cat_cols}})
            cat_dict.update({index: {k: (v-min_cat_cols)/(max_cat_cols-min_cat_cols) for k,v in cat_dict[index].items()}})
        else:
            df[index] = (col-col.min())/(col.max()-col.min())
            rescale_dict.update({'index':{'length': col.max()-col.min(), 'x0':col.min()}})

    hue_list = df[hue].unique().to_list()
    ax = fig.add_axes([0.13,0.15,0.65,0.65])
    ax.set_axis_off()

    for index,row in df.iterrows():
        if df[hue].nunique()>2:
            c_list = color_palette('hls') if df[hue].nunique()<6 else color_palette('hls', df[hue].nunique())
            ax.plot(range(len(row)), row, linewidth=0.6, alpha=0.6, color=c_list[hue_list.index(row[hue])])

    ax.set_ylim(0,1)

    i=0
    twin_axes = []
    for index, col in df.items():
        twin_axes.append(ax.twinx())
        twin_axes[-1].spines.right.set_position(('data', i))
        twin_axes[-1].spines[['left', 'top', 'bottom']].set_visible(False)
        if index in cat_dict.keys():
            twin_axes[-1].set_yticks(list(cat_dict[index].values()), list(cat_dict[index].keys()))
        else:
            twin_axes[-1].yaxis.set_major_locator(MaxNLocator(6))
            col = col*rescale_dict[index]['length']+rescale_dict[index]['x0']
            twin_axes[-1].set_ylim(col.min(), col.max())

            ax.text(i, 1.03, f'{col.max():.2f}', horizontalalignment='center')
            ax.text(i, -0.07, f'{col.min():.2f}', horizontalalignment='center')
        ax.text(i, 1.12, index, horizontalalignment='center')
        i += 1


def analysis_fig_5(fig, df, x, hue):
    axe = fig.add_axes([0.13, 0.22, 0.65, 0.65])
    kdeplot(data=df, x=x, hue=hue, fill=True, common_norm=False, palette='crest', alpha=0.5, linewidth=0, ax=axe)
    move_legend(axe, 'upper left', bbox_to_anchor=(1.03,1), frameon=False)


def analysis_fig_6(fig, df, x, y, hue):
    axe = fig.add_axes([0.13, 0.22, 0.65, 0.65])
    kdeplot(data=df, x=x, y=y, hue=hue, fill=True, palette='hls', errorbar='sd', alpha=0.5, ax=axe)
    move_legend(axe, 'upper left', bbox_to_anchor=(1.03,1), frameon=False)
