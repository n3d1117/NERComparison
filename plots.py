import matplotlib.pyplot as plt
import numpy as np


def plot_metrics(a, r, p, f1, names, file, lang):
    ind = np.arange(len(a))
    width = 0.17

    fig = plt.figure()
    ax = fig.add_subplot(111)

    rects1 = ax.bar(ind, a, width, color='tomato')
    rects2 = ax.bar(ind + width, r, width, color='yellowgreen')
    rects3 = ax.bar(ind + width * 2, p, width, color='royalblue')
    rects4 = ax.bar(ind + width * 3, f1, width, color='gold')

    ax.set_ylabel('Risultati')
    ax.set_xticks(ind + width + width/2)
    ax.set_xticklabels(names)
    ax.legend((rects1[0], rects2[0], rects3[0], rects4[0]), ('accuracy', 'recall', 'precision', 'f1'))

    plt.title('Metriche di performance per estrattori di entità ({})'.format(lang))
    plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=True)
    plt.savefig(file)


def plot_times(data, tools, lang, save_to):

    fig = plt.figure()
    ax = fig.add_subplot(111)

    colors = ['tomato', 'yellowgreen', 'royalblue', 'gold', 'darkorchid', 'deepskyblue', 'lightsteelblue', 'darkgreen']

    a = ax.bar(tools, data, width=0.6)
    for i, bar in enumerate(a):
        bar.set_color(colors[i])

    plt.title('Tempi di computazione per estrattori di entità ({})'.format(lang))
    ax.set_ylabel('Tempo (s)')

    plt.savefig(save_to)

    print('[*] Saved time plot to {}'.format(save_to))

