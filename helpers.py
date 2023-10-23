import csv


def read_csv(csv_fname, as_dict=True, delimiter=',', has_headers=True):
    with open(csv_fname, newline=str()) as handler:
        if as_dict:
            assert has_headers, "Doesn't have headers"
            for row in csv.DictReader(handler, delimiter=delimiter):
                yield row
        else:
            reader = csv.reader(handler, delimiter=delimiter)
            if has_headers:
                next(reader)
            for row in reader:
                yield row
