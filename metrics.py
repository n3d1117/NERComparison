import pandas as pd
from tabulate import tabulate


def evaluate_metrics(truth, run):

    # Metrics (accuracy, recall, precision, f1)
    true_pos = float(len(set(run) & set(truth)))
    if float(len(run)) >= float(true_pos):
        false_pos = len(run) - true_pos
    else:
        false_pos = true_pos - len(run)
    true_neg = 0
    if len(truth) >= len(run):
        false_neg = len(truth) - len(run)
    else:
        false_neg = 0

    accuracy = (float(true_pos) + float(true_neg)) / float(len(truth))
    recall = (float(true_pos)) / float(len(truth))
    if float(false_pos) + float(true_pos) > 0:
        precision = float(true_pos) / (float(false_pos) + float(true_pos))
    else:
        precision = 0
    if precision + recall > 0:
        f1 = 2 * ((precision * recall) / (precision + recall))
    else:
        f1 = 0

    # Confusion matrix
    d = {'Predetti Negativi': [true_neg, false_neg], 'Predetti Positivi': [false_pos, true_pos]}
    confusion_matrix = pd.DataFrame(d, index=['Negativi', 'Positivi'])

    return accuracy, recall, precision, f1, confusion_matrix


def write_article(article, index, to_file):
    f = open(to_file, 'w')
    f.write('\nArticle #{}\n\n'.format(index))
    f.write(article)
    f.close()


def write_results_table(entities, names, to_file):
    dataframes = []
    for i in range(len(entities)):
        dataframes.append(pd.Series(entities[i], index=None, dtype=object, name=names[i], copy=False, fastpath=False))
    table = pd.concat(dataframes, axis=1).fillna('')
    table.to_csv(to_file)


def write_metrics_table(metrics, tools, to_file):
    df = pd.DataFrame(columns=['accuracy', 'recall', 'precision', 'f1'], index=tools)
    for i in range(len(metrics)):
        df.loc[tools[i]] = pd.Series({'accuracy': metrics[i][0], 'recall': metrics[i][1], 'precision': metrics[i][2], 'f1': metrics[i][3]})
    file = open(to_file, 'w')
    file.write('\nRisultati\n\n')
    file.write(tabulate(df, headers='keys', tablefmt='grid'))
    file.write('\n\nMatrici di confusione')
    for i in range(len(metrics)):
        file.write('\n\n{}\n'.format(tools[i]))
        file.write(tabulate(metrics[i][4], headers='keys', tablefmt='grid'))
    file.close()
