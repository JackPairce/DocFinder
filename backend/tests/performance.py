import os
from unittest import TestCase
import time
import numpy as np
import pandas as pd

from ..app.utils.text_processing import process_text
from ..app.utils.file_operations import download_file, read_csv
from ..app.utils.optimization import parallelize_dataframe


def timeit(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} took {end - start} seconds")
        return result, end - start

    return wrapper


# @timeit
def square(n):
    return n * n


class TestPerformance(TestCase):
    def test_performance(self):

        data = np.array(range(1000000))
        print("simple")
        _, simple = timeit(square)(data)
        print("parallel process")
        _, parallel = timeit(parallelize_dataframe)(data, square)

        self.assertLess(parallel, simple)

    def test_performance_word2vec(self):
        LNK = "https://www.gutenberg.org/cache/epub/feeds/pg_catalog.csv"
        CSV_FILE = "/tmp/pg_catalog.csv"
        # download the csv file
        download_file(LNK, CSV_FILE)

        # read the csv file
        data = read_csv(CSV_FILE)

        # rename column Text# to id and delete column LoCC
        data.rename(columns={"Text#": "id"}, inplace=True)
        data.drop(columns=["LoCC"], inplace=True)

        # Filter "Type" by "Text" only
        data = data[data["Type"] == "Text"]

        # Filter "Languages" by "en" and "fr", and rename them
        data = data[data["Language"].isin(["en", "fr"])]
        data["Language"] = data["Language"].replace({"en": "english", "fr": "french"})

        # process Authors and Bookshelves columns
        # split the Authors and Bookshelves columns by ";" and remove date from the Authors column then split it by "," and join it by " ".
        data["Authors"] = (
            data["Authors"]
            .str.replace(r"\d{4}-\d{4}", "")
            .str.replace(",", "")
            .str.strip()
        )
        data["Authors"] = data["Authors"].str.split(";")

        # split the Bookshelves column by ";"
        data["Bookshelves"] = data["Bookshelves"].str.split(";")

        # split the Subjects column by ";"
        data["Subjects"] = data["Subjects"].str.split(";")

        # remove nan values of each row
        data.dropna(inplace=True)

        nb_rows = 10
        data = data[:nb_rows]
        print(f"calculating {nb_rows} rows")

        # use Sentence Transformers (all-MiniLM-L6-v2) to encode the "subject_vector" column and save it on same column.
        # issued, authors, title, subjects
        target = data.apply(
            lambda row: f"{row['Issued']} {",".join(row['Authors'])} {row['Title']} {",".join(row['Subjects'])} {",".join(row['Bookshelves'])}",
            axis=1,
        )

        @timeit
        def process_simple(data):
            return process_text(data)

        @timeit
        def process_parallel(data):
            return parallelize_dataframe(data, process_text)

        print("simple")
        _, simple = process_simple(target)
        print("parallel")
        _, parallel = process_parallel(target)

        self.assertLess(parallel, simple)


if __name__ == "__main__":
    TestPerformance().test_performance_word2vec()
