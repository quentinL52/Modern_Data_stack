import pandas as pd
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer

@transformer
def merge_dataframes(df_cdd, df_cdi, df_stage, *args, **kwargs):
    """
    Fusionne les trois DataFrames
    """
    df_combined = pd.concat([df_cdd, df_cdi, df_stage], ignore_index=True)

    return df_combined