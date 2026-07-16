from phoneme_data import PHONEMES


def get_phoneme_info(symbol: str) -> dict:
    """
    Returns information about an IPA phoneme.

    Parameters
    ----------
    symbol : str
        IPA symbol.

    Returns
    -------
    dict
        Dictionary containing phonetic information.
    """

    phoneme = PHONEMES.get(symbol)

    if phoneme is None:
        return {
            "found": False,
            "message": f"Phoneme '{symbol}' not found."
        }

    return {
        "found": True,
        **phoneme
    }



