import statistics
import pandas as pd


def cleaned(sentence):
    return sentence.replace(' ,', '').replace(' .', '.').replace('( ', '(').replace(' )', ')').replace('$ ', '$')\
                   .replace(" '", "'").replace(" '", "'").replace(' "', '"').replace("' ", "'").replace(" :", ":")\
                   .replace(" ;", ";").replace(' °', '°').replace(' ª', 'ª').replace('« ', '«').replace(' »', '»')\
                   .replace(' ?', '?').replace(' !', '!')


def mean_one(array):
    return statistics.mean(array)


def mean(one, two, three, four):
    return statistics.mean(one), statistics.mean(two), statistics.mean(three), statistics.mean(four)


def print_latex_table(accuracies, recalls, precisions, f1scores, tool_names):
    data = [accuracies, recalls, precisions, f1scores]
    df = pd.DataFrame(columns=['accuracy', 'recall', 'precision', 'f1'], index=tool_names)
    for i in range(len(accuracies)):
        df.loc[tool_names[i]] = pd.Series(
            {'accuracy': data[0][i], 'recall': data[1][i], 'precision': data[2][i], 'f1': data[3][i]}
        )
    print(df.to_latex(bold_rows=True))

