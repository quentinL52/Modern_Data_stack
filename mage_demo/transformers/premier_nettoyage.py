import pandas as pd
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def clean_dataframe(df, *args, **kwargs):
    """
    Nettoie le DataFrame
    """
    df_clean = df.copy()
    df_clean['publication'] = pd.to_datetime(df_clean['publication'], dayfirst=True, errors='coerce')
    df_clean['publication'] = df_clean['publication'].dt.strftime('%d-%m-%Y')
    df_clean = df_clean.drop_duplicates()
    return df_clean


@test
def test_output(output, *args) -> None:
    """
    Tests de validation
    """
    assert output is not None, 'La sortie est non définie'
    assert len(output) > 0, 'Le DataFrame est vide'
    date_format = output['publication'].str.match(r'\d{2}-\d{2}-\d{4}')
    assert date_format.all(), 'Format de date incorrect'
    assert len(output) == len(output.drop_duplicates()), 'Il reste des doublons dans le DataFrame'