import re
from django.template.defaultfilters import slugify as django_slugify


def slugify(s):
    """
    Convert a string to a slug.

    Args:
        s (str): The string to be converted to a slug.

    Returns:
        str: The slugified string.
    """
    # Define custom alphabet mappings
    alphabet = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
        'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'
    }
    # Replace non-alphanumeric characters with dashes
    s = re.sub(r'[^\w\s-]', '', s)
    # If a character is not in the alphabet mapping, keep it as is
    return django_slugify(''.join(alphabet.get(w, w) for w in s.lower()))
