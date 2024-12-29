from typing import Callable
import pandas as pd
from pandarallel import pandarallel


def parallelize_dataframe(df: pd.DataFrame, func: Callable, chunk_size=None):
    """
    This function parallelizes the execution of a function on a dataframe.
    """
    if chunk_size is None:
        chunk_size = len(df) // 4
    pandarallel.initialize()
    return df.groupby(pd.RangeIndex(len(df)) // chunk_size).parallel_apply(
        lambda x: func(x.tolist())
    )
