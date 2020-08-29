from extract_entities import EntityExtractor
from metrics import evaluate_metrics, write_article, write_results_table, write_metrics_table
from plots import plot_metrics, plot_times
from preprocess_corpus import preprocess_english_dataset, preprocess_italian_dataset
import pandas as pd
from functools import reduce
from utils import mean, mean_one, print_latex_table
from timeit import default_timer as timer


def test_english_dataset(n_articles, sentences_per_article):
    print('[*] Testing english dataset!')

    # Preprocessing
    print('[*] Preprocessing...')
    preprocess_english_dataset(file='datasets/en/dataset_orig.csv', output='./datasets/en/dataset_cleaned.csv')

    # Read cleaned dataset
    df = pd.read_csv('datasets/en/dataset_cleaned.csv')

    tool_names = ['Spacy', 'Polyglot', 'NL', 'Dandelion', 'NLTK', 'Stanford', 'GCloud', 'Stanza']

    # Prepare Accuracies, Recalls, Precisions and f1 scores for every tool
    spacy_acc, polyglot_acc, dandelion_acc, nl_acc, nltk_acc, stanford_acc, gcloud_acc, stanza_acc = [], [], [], [], [], [], [], []
    spacy_rec, polyglot_rec, dandelion_rec, nl_rec, nltk_rec, stanford_rec, gcloud_rec, stanza_rec = [], [], [], [], [], [], [], []
    spacy_pre, polyglot_pre, dandelion_pre, nl_pre, nltk_pre, stanford_pre, gcloud_pre, stanza_pre = [], [], [], [], [], [], [], []
    spacy_f1, polyglot_f1, dandelion_f1, nl_f1, nltk_f1, stanford_f1, gcloud_f1, stanza_f1 = [], [], [], [], [], [], [], []

    extractor = EntityExtractor(language='en')

    for index in range(n_articles):  # iterate over articles
        str_index = str(index + 1)

        print('[*] Working on article #{}'.format(str_index))

        # get chunked dataframe
        spliced_df = df.loc[index * sentences_per_article:].head(sentences_per_article)
        # combine {sentences_per_article} subsequent sentences to form an article
        article = '\n'.join(spliced_df['Sentence'].tolist())
        # flatten all entities for each sentence into one list
        true_entities = list(
            set(reduce(
                lambda x, y: x + y, [
                    entities.split(', ') for entities in spliced_df['Entities'].tolist()
                ])
            )
        )

        # Write article to txt file
        output_text_file = './datasets/en/generated_articles/article_{}.txt'.format(str_index)
        print('[*] Writing article to {}...'.format(output_text_file))
        write_article(article, str_index, to_file=output_text_file)

        # print(article)
        # print(true_entities)

        # extract entities with each tool
        spacy_entities = extractor.extract_entities(article, tool='spacy')
        polyglot_entities = extractor.extract_entities(article, tool='polyglot')
        dandelion_entities = extractor.extract_entities(article, tool='dandelion')
        nl_entities = extractor.extract_entities(article, tool='nl')
        nltk_entities = extractor.extract_entities(article, tool='nltk')
        stanford_entities = extractor.extract_entities(article, tool='stanford')
        gcloud_entities = extractor.extract_entities(article, tool='gcloud')
        stanza_entities = extractor.extract_entities(article, tool='stanza')

        # Evaluate accuracy, recall, precision, f1 for each tool
        print('[*] Evaluating metrics...')
        spacy_metrics = evaluate_metrics(true_entities, spacy_entities)
        polyglot_metrics = evaluate_metrics(true_entities, polyglot_entities)
        dandelion_metrics = evaluate_metrics(true_entities, dandelion_entities)
        nl_metrics = evaluate_metrics(true_entities, nl_entities)
        nltk_metrics = evaluate_metrics(true_entities, nltk_entities)
        stanford_metrics = evaluate_metrics(true_entities, stanford_entities)
        gcloud_metrics = evaluate_metrics(true_entities, gcloud_entities)
        stanza_metrics = evaluate_metrics(true_entities, stanza_entities)

        # Write results table
        output_results_file = './results/en/article_{}_entities.csv'.format(str_index)
        print('[*] Writing results table to {}...'.format(output_results_file))
        all_entities = [true_entities, spacy_entities, polyglot_entities, dandelion_entities, nl_entities,
                        nltk_entities, stanford_entities, gcloud_entities, stanza_entities]
        all_names = ['True Entities', 'Spacy Entities', 'Polyglot Entities', 'Dandelion Entities',
                     'NaturalLanguage Entities', 'NLTK Entities', 'Stanford Entities', 'Google Cloud Entities',
                     'Stanza Entities']
        write_results_table(all_entities, all_names, to_file=output_results_file)

        # Write metrics table
        output_metrics_file = './results/en/article_{}_results.txt'.format(str_index)
        print('[*] Writing metrics table to {}...'.format(output_metrics_file))
        all_metrics = [spacy_metrics, polyglot_metrics, dandelion_metrics, nl_metrics, nltk_metrics, stanford_metrics,
                       gcloud_metrics, stanza_metrics]
        write_metrics_table(all_metrics, tool_names, to_file=output_metrics_file)

        spacy_acc.append(spacy_metrics[0])
        polyglot_acc.append(polyglot_metrics[0])
        dandelion_acc.append(dandelion_metrics[0])
        nl_acc.append(nl_metrics[0])
        nltk_acc.append(nltk_metrics[0])
        stanford_acc.append(stanford_metrics[0])
        gcloud_acc.append(gcloud_metrics[0])
        stanza_acc.append(stanza_metrics[0])

        spacy_rec.append(spacy_metrics[1])
        polyglot_rec.append(polyglot_metrics[1])
        dandelion_rec.append(dandelion_metrics[1])
        nl_rec.append(nl_metrics[1])
        nltk_rec.append(nltk_metrics[1])
        stanford_rec.append(stanford_metrics[1])
        gcloud_rec.append(gcloud_metrics[1])
        stanza_rec.append(stanza_metrics[1])

        spacy_pre.append(spacy_metrics[2])
        polyglot_pre.append(polyglot_metrics[2])
        dandelion_pre.append(dandelion_metrics[2])
        nl_pre.append(nl_metrics[2])
        nltk_pre.append(nltk_metrics[2])
        stanford_pre.append(stanford_metrics[2])
        gcloud_pre.append(gcloud_metrics[2])
        stanza_pre.append(stanza_metrics[2])

        spacy_f1.append(spacy_metrics[3])
        polyglot_f1.append(polyglot_metrics[3])
        dandelion_f1.append(dandelion_metrics[3])
        nl_f1.append(nl_metrics[3])
        nltk_f1.append(nltk_metrics[3])
        stanford_f1.append(stanford_metrics[3])
        gcloud_f1.append(gcloud_metrics[3])
        stanza_f1.append(stanza_metrics[3])

        print('\n')

    # Compute averages
    print('[*] Averaging results...')
    avg_spacy_accuracy, avg_spacy_recall, avg_spacy_precision, avg_spacy_f1 = mean(spacy_acc, spacy_rec, spacy_pre, spacy_f1)
    avg_polyglot_accuracy, avg_polyglot_recall, avg_polyglot_precision, avg_polyglot_f1 = mean(polyglot_acc, polyglot_rec, polyglot_pre, polyglot_f1)
    avg_dandelion_accuracy, avg_dandelion_recall, avg_dandelion_precision, avg_dandelion_f1 = mean(dandelion_acc, dandelion_rec, dandelion_pre, dandelion_f1)
    avg_nl_accuracy, avg_nl_recall, avg_nl_precision, avg_nl_f1 = mean(nl_acc, nl_rec, nl_pre, nl_f1)
    avg_nltk_accuracy, avg_nltk_recall, avg_nltk_precision, avg_nltk_f1 = mean(nltk_acc, nltk_rec, nltk_pre, nltk_f1)
    avg_stanford_accuracy, avg_stanford_recall, avg_stanford_precision, avg_stanford_f1 = mean(stanford_acc, stanford_rec, stanford_pre, stanford_f1)
    avg_gcloud_accuracy, avg_gcloud_recall, avg_gcloud_precision, avg_gcloud_f1 = mean(gcloud_acc, gcloud_rec, gcloud_pre, gcloud_f1)
    avg_stanza_accuracy, avg_stanza_recall, avg_stanza_precision, avg_stanza_f1 = mean(stanza_acc, stanza_rec, stanza_pre, stanza_f1)

    # Plot bar chart
    print('[*] Plotting accuracies...')
    accuracies = [avg_spacy_accuracy, avg_polyglot_accuracy, avg_nl_accuracy, avg_dandelion_accuracy, avg_nltk_accuracy, avg_stanford_accuracy, avg_gcloud_accuracy, avg_stanza_accuracy]
    recalls = [avg_spacy_recall, avg_polyglot_recall, avg_nl_recall, avg_dandelion_recall, avg_nltk_recall, avg_stanford_recall, avg_gcloud_recall, avg_stanza_recall]
    precisions = [avg_spacy_precision, avg_polyglot_precision, avg_nl_precision, avg_dandelion_precision, avg_nltk_precision, avg_stanford_precision, avg_gcloud_precision, avg_stanza_precision]
    f1scores = [avg_spacy_f1, avg_polyglot_f1, avg_nl_f1, avg_dandelion_f1, avg_nltk_f1, avg_stanford_f1, avg_gcloud_f1, avg_stanza_f1]
    plot_metrics(accuracies, recalls, precisions, f1scores, tool_names, file='results/en/result.png', lang='en')

    # Print Latex table
    print_latex_table(accuracies, recalls, precisions, f1scores, tool_names)

    print('[*] Done!')


def test_italian_dataset(n_articles, sentences_per_article):
    print('\n\n[*] Testing italian dataset!')

    # Preprocessing
    print('[*] Preprocessing...')
    preprocess_italian_dataset(file='datasets/it/I-CAB_All/NER-09/I-CAB-evalita09-NER-training.iob2',
                               output='./datasets/it/dataset_cleaned.csv')

    # Read dataset
    df = pd.read_csv('datasets/it/dataset_cleaned.csv')
    tool_names = ['Spacy', 'Polyglot', 'NL', 'Dandelion', 'Tint', 'GCloud']

    # Prepare Accuracies, Recalls, Precisions and f1 scores for every tool
    spacy_acc, polyglot_acc, dandelion_acc, nl_acc, tint_acc, gcloud_acc = [], [], [], [], [], []
    spacy_rec, polyglot_rec, dandelion_rec, nl_rec, tint_rec, gcloud_rec = [], [], [], [], [], []
    spacy_pre, polyglot_pre, dandelion_pre, nl_pre, tint_pre, gcloud_pre = [], [], [], [], [], []
    spacy_f1, polyglot_f1, dandelion_f1, nl_f1, tint_f1, gcloud_f1 = [], [], [], [], [], []

    extractor = EntityExtractor(language='it')

    for index in range(n_articles):  # iterate over articles
        str_index = str(index + 1)

        print('[*] Working on article #{}'.format(str_index))

        # get chunked dataframe
        spliced_df = df.loc[index * sentences_per_article:].head(sentences_per_article)
        # combine sentences_per_article subsequent sentences to form an article
        article = '\n'.join(spliced_df['Sentence'].tolist())
        # flatten all entities for each sentence into one list
        true_entities = list(
            set(reduce(
                lambda x, y: x + y, [
                    entities.split(', ') for entities in spliced_df['Entities'].tolist()
                ])
            )
        )

        # print(article)
        # print(true_entities)

        # Write article to txt file
        output_text_file = './datasets/it/generated_articles/article_{}.txt'.format(str_index)
        print('[*] Writing article to {}...'.format(output_text_file))
        write_article(article, str_index, to_file=output_text_file)

        # extract entities with each tool
        spacy_entities = extractor.extract_entities(article, tool='spacy')
        polyglot_entities = extractor.extract_entities(article, tool='polyglot')
        dandelion_entities = extractor.extract_entities(article, tool='dandelion')
        nl_entities = extractor.extract_entities(article, tool='nl')
        tint_entities = extractor.extract_entities(article, tool='tint')
        gcloud_entities = extractor.extract_entities(article, tool='gcloud')

        # Evaluate accuracy, recall, precision, f1 for each tool
        print('[*] Evaluating metrics...')
        spacy_metrics = evaluate_metrics(true_entities, spacy_entities)
        polyglot_metrics = evaluate_metrics(true_entities, polyglot_entities)
        dandelion_metrics = evaluate_metrics(true_entities, dandelion_entities)
        nl_metrics = evaluate_metrics(true_entities, nl_entities)
        tint_metrics = evaluate_metrics(true_entities, tint_entities)
        gcloud_metrics = evaluate_metrics(true_entities, gcloud_entities)

        # Write results table
        output_results_file = './results/it/article_{}_entities.csv'.format(str_index)
        print('[*] Writing results table to {}...'.format(output_results_file))
        all_entities = [true_entities, spacy_entities, polyglot_entities, dandelion_entities, nl_entities,
                        tint_entities, gcloud_entities]
        all_names = ['True Entities', 'Spacy Entities', 'Polyglot Entities', 'Dandelion Entities',
                     'NaturalLanguage Entities', 'Tint Entities', 'Google Cloud Entities']
        write_results_table(all_entities, all_names, to_file=output_results_file)

        # Write metrics table
        output_metrics_file = './results/it/article_{}_results.txt'.format(str_index)
        print('[*] Writing metrics table to {}...'.format(output_metrics_file))
        all_metrics = [spacy_metrics, polyglot_metrics, dandelion_metrics, nl_metrics, tint_metrics, gcloud_metrics]
        write_metrics_table(all_metrics, tool_names, to_file=output_metrics_file)

        spacy_acc.append(spacy_metrics[0])
        polyglot_acc.append(polyglot_metrics[0])
        dandelion_acc.append(dandelion_metrics[0])
        nl_acc.append(nl_metrics[0])
        tint_acc.append(tint_metrics[0])
        gcloud_acc.append(gcloud_metrics[0])

        spacy_rec.append(spacy_metrics[1])
        polyglot_rec.append(polyglot_metrics[1])
        dandelion_rec.append(dandelion_metrics[1])
        nl_rec.append(nl_metrics[1])
        tint_rec.append(tint_metrics[1])
        gcloud_rec.append(gcloud_metrics[1])

        spacy_pre.append(spacy_metrics[2])
        polyglot_pre.append(polyglot_metrics[2])
        dandelion_pre.append(dandelion_metrics[2])
        nl_pre.append(nl_metrics[2])
        tint_pre.append(tint_metrics[2])
        gcloud_pre.append(gcloud_metrics[2])

        spacy_f1.append(spacy_metrics[3])
        polyglot_f1.append(polyglot_metrics[3])
        dandelion_f1.append(dandelion_metrics[3])
        nl_f1.append(nl_metrics[3])
        tint_f1.append(tint_metrics[3])
        gcloud_f1.append(gcloud_metrics[3])

        print('\n')

    # Compute averages
    print('[*] Averaging results...')
    avg_spacy_accuracy, avg_spacy_recall, avg_spacy_precision, avg_spacy_f1 = mean(spacy_acc, spacy_rec, spacy_pre, spacy_f1)
    avg_polyglot_accuracy, avg_polyglot_recall, avg_polyglot_precision, avg_polyglot_f1 = mean(polyglot_acc, polyglot_rec, polyglot_pre, polyglot_f1)
    avg_dandelion_accuracy, avg_dandelion_recall, avg_dandelion_precision, avg_dandelion_f1 = mean(dandelion_acc, dandelion_rec, dandelion_pre, dandelion_f1)
    avg_nl_accuracy, avg_nl_recall, avg_nl_precision, avg_nl_f1 = mean(nl_acc, nl_rec, nl_pre, nl_f1)
    avg_tint_accuracy, avg_tint_recall, avg_tint_precision, avg_tint_f1 = mean(tint_acc, tint_rec, tint_pre, tint_f1)
    avg_gcloud_accuracy, avg_gcloud_recall, avg_gcloud_precision, avg_gcloud_f1 = mean(gcloud_acc, gcloud_rec, gcloud_pre, gcloud_f1)

    # Plot bar chart
    print('[*] Plotting accuracies...')
    accuracies = [avg_spacy_accuracy, avg_polyglot_accuracy, avg_nl_accuracy, avg_dandelion_accuracy, avg_tint_accuracy, avg_gcloud_accuracy]
    recalls = [avg_spacy_recall, avg_polyglot_recall, avg_nl_recall, avg_dandelion_recall, avg_tint_recall, avg_gcloud_recall]
    precisions = [avg_spacy_precision, avg_polyglot_precision, avg_nl_precision, avg_dandelion_precision, avg_tint_precision, avg_gcloud_precision]
    f1scores = [avg_spacy_f1, avg_polyglot_f1, avg_nl_f1, avg_dandelion_f1, avg_tint_f1, avg_gcloud_f1]
    plot_metrics(accuracies, recalls, precisions, f1scores, tool_names, file='results/it/result.png', lang='it')

    # Print Latex table
    print_latex_table(accuracies, recalls, precisions, f1scores, tool_names)

    print('[*] Done!\n\n')


def measure_elapsed_time(n_articles, lang):
    print("[*] Measuring elapsed time for '{}' language...".format(lang))

    if lang == 'en':
        times = {'spacy': [], 'polyglot': [], 'dandelion': [], 'nl': [], 'nltk': [], 'stanford': [], 'gcloud': [], 'stanza': []}
    else:
        times = {'spacy': [], 'polyglot': [], 'dandelion': [], 'nl': [], 'tint': [], 'gcloud': []}

    extractor = EntityExtractor(language=lang)

    for index in range(n_articles):
        with open('datasets/{}/generated_articles/article_{}.txt'.format(lang, index + 1), 'r') as file:

            print('[*] Working on article #{}'.format(index + 1))

            article = file.read().split('\n\n')[-1]

            for tool in times.keys():
                start = timer()
                _ = extractor.extract_entities(article, tool, quiet=True)
                end = timer()
                times[tool].append(end - start)

    print('[*] Averaging results...')

    # Sort by time
    tools, data = [], []
    sorted_data = sorted(times.items(), key=lambda x: mean_one(x[1]))
    for (key, v) in sorted_data:
        data.append(mean_one(v))
        tools.append(key)

    # Plot bar chart
    plot_times(data, tools, lang, save_to='results/{}/time.png'.format(lang))

    print('[*] Done!\n')


if __name__ == '__main__':
    n_articles = 50
    sentences_per_article = 10

    test_english_dataset(n_articles, sentences_per_article)
    test_italian_dataset(n_articles, sentences_per_article)

    measure_elapsed_time(n_articles, lang='en')
    measure_elapsed_time(n_articles, lang='it')
