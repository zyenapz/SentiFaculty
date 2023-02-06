import csv, os

def get_corpus_polarities():
    corpus_dict = dict()

    __location__  = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(__location__, 'corpus.txt'), newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='\n')

        for row in reader:
            data = row[0].split('\t')
            corpus_dict[data[0]] = data[1]

    return corpus_dict
