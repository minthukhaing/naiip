import re
from typing import List, Dict, Optional
import models.phoneme_transpitor as pp

# Constants
ALL_PREFIXES = [
    "ဆရာတော်", "ဆရာမ", "ဆရာ", "သုဓမ္မာ", "သုဓမ္မ", "အဂ္ဂိ", "အဂ္ဂ", 
    "မဟာကထာနံ", "မဟာ", "ဇောတိကဓဇ", "သဒ္ဓမ္မဇောတိကဓဇ", "မဏိဇောတဓရ", 
    "သတိုး", "သရေ", "စည်သူ", "သီဟသူရ", "သူရင်း", "သူရဲ", "သူရိန်", 
    "သူရိယ", "သူရသ္သတီ", "သူရဇ္ဇ", "သူရာ", "သူရ", "သီရိပျံချီ", 
    "သီရိ", "ဇေယျကျော်ထင်", "အလင်္ကာကျော်စွာ", "သိပ္ပကျော်စွာ", 
    "ပြည်ထောင်စုလွှတ်တော်", "ပြည်ထောင်စု", "တံခွန်", "ဇာနည်", 
    "လမ်းစဉ်ဇာနည်", "ပညာဗလ", "ဒေါ်",
]

MONO = [
    "က", "ခ", "ဂ", "ဃ", "င", "စ", "ဆ", "ဇ", "ဈ", "ဉ", "ည", "ဋ", 
    "ဌ", "ဍ", "ဎ", "ဏ", "တ", "ထ", "ဒ", "ဓ", "န", "ပ", "ဖ", "ဗ", 
    "ဘ", "မ", "ယ", "ရ", "လ", "ဝ", "သ", "ဟ", "ဠ", "အ",
]

 
def preprocess(text):
    text = text.replace("ဿ", "သ္သ")
    # text = text.replace("ငြ", "ည")
    text = text.replace("အရုဏ်", "အာရုဏ်")
    text = text.replace("အရုဏ", "အာရုဏ")
    text = text.replace("\u1026\u1038", "အူး")
    text = text.replace("ဥူး", "အူး")
    # text = text.replace("\u1026", "အူ")
    text = text.replace("ဥူ", "အူ")
    text = text.replace("ဥုံ", "အုမ်")
    text = text.replace("ဥု", "အူ")
    text = text.replace("ဥ", "အု")
    text = text.replace("န်ုပ်", "န်နုပ်")
    #text = text.replace("ဪ", "အော်")
    #text = text.replace("ဩ", "အော")
    text = text.replace("ဤ", "အီ")
    # text = text.replace("၏", "အိ")
    # text = text.replace("ဧ", "အေ")
    text = text.replace("ဣိ", "အိ")
    text = text.replace("ဣီ", "အီ")
    text = text.replace("ဣူ", "အူ")
    text = text.replace("ဣု", "အု")
    # text = text.replace("ဣ", "အိ")
    text = text.replace("၍", "ရွေ့")
    text = text.replace("၎င်း", "လည်းကောင်း")
    text = text.replace("၌", "နှိုက်")
    text = text.replace("ွှံ့", "ွှန့်")
    text = text.replace("ွံ့", "ွန့်")
    text = text.replace("ျွှံ့", "ျွှန့်")
    text = text.replace("ြွှံ့", "ြွှန့်")
    text = re.sub(r'[\u200B\u200C]', '', text)
    return text

def flatten_stack(text: str) -> str:
    """
    Flatten stacked characters in the text.
    
    Args:
        text (str): Input text with stacked characters
    
    Returns:
        str: Text with flattened stacked characters
    """
    stack_patterns = [
        re.compile(r"([\u1000-\u1020])\u1039", re.UNICODE),
        re.compile(r"([\u1000-\u1020\u1004\u103A])\u1039", re.UNICODE),
    ]

    for index, pattern in enumerate(stack_patterns):
        while pattern.search(text):
            if index == 0:
                text = pattern.sub(lambda match: f"{match.group(1)}\u103A", text)
            else:
                text = pattern.sub(lambda match: match.group(1), text)

    return text

def get_phoneme_mapping(
    phoneme_dict: Dict[str, Dict[str, str]], 
    label: str, 
    index: int, 
    phoneme_key: str, 
    syllable_list: List[str]
) -> str:
    """
    Get phoneme mapping for a given label.
    
    Args:
        phoneme_dict (Dict): Phoneme dictionary
        label (str): Current label
        index (int): Index of the label
        phoneme_key (str): Phoneme key
        syllable_list (List[str]): List of syllables
    
    Returns:
        str: Mapped phoneme
    """
    
    print(f"-------------final syllable list: {syllable_list}")
    
    if label in phoneme_dict:
        phoneme = phoneme_dict[label][phoneme_key]
    else:
        mono_is_last = (label in MONO and syllable_list[-1] == label)
        phoneme = pp.transcript(label, phoneme_key, syllable_list, mono_is_last)
    
    return phoneme

def get_intermediate_map(
    merged_label: str,
    phoneme_dict: Dict[str, Dict[str, str]],
    index: int,
    phoneme_key: str,
    merged_list: List[str]
) -> str:
    """
    Get intermediate phoneme mapping.
    
    Args:
        merged_label (str): Merged label
        phoneme_dict (Dict): Phoneme dictionary
        index (int): Index of the label
        phoneme_key (str): Phoneme key
        merged_list (List[str]): List of merged labels
    
    Returns:
        str: Mapped word
    """
    if merged_label in phoneme_dict and phoneme_dict[merged_label].get(phoneme_key, "") != "":
        mapped_word = phoneme_dict[merged_label][phoneme_key]
    else:
        flattened_text = flatten_stack(merged_label)
        final_syllable_list = syllable_split(flattened_text)
        mapped_word = ''.join(
            get_phoneme_mapping(phoneme_dict, entry, i, phoneme_key, merged_list)
            for i, entry in enumerate(final_syllable_list)
        )
    
    return mapped_word

def get_prefix_splitted_map(
    text: str,
    phoneme_dict: Dict[str, Dict[str, str]],
    phoneme_key: str
) -> str:
    """
    Get phoneme mapping for prefix-splitted text.
    
    Args:
        text (str): Input text
        phoneme_dict (Dict): Phoneme dictionary
        phoneme_key (str): Phoneme key
    
    Returns:
        str: Mapped phoneme
    """
    if text in phoneme_dict and phoneme_dict[text].get(phoneme_key, "") != "":
        mapped_phoneme = phoneme_dict[text][phoneme_key]
    elif text in phoneme_dict and phoneme_dict[text].get(phoneme_key, "") == "":
        flattened_text = flatten_stack(text)
        syllable_list = syllable_split(flattened_text)
        mapped_phoneme = ''.join(
            get_phoneme_mapping(phoneme_dict, entry, i, phoneme_key, syllable_list)
            for i, entry in enumerate(syllable_list)
        )
    else:
        syllable_list = syllable_split(text)
        merge_list = merge_consecutive(syllable_list, phoneme_dict)
        print(f'------------------mergeList: {merge_list}')
        mapped_phoneme = ' '.join(
            get_intermediate_map(entry, phoneme_dict, i, phoneme_key, merge_list)
            for i, entry in enumerate(merge_list)
        )
    
    return mapped_phoneme

def get_phoneme_map(
    text: str,
    phoneme_dict: Dict[str, Dict[str, str]],
    phoneme_key: str
) -> str:
    """
    Get complete phoneme mapping for input text.
    
    Args:
        text (str): Input text
        phoneme_dict (Dict): Phoneme dictionary
        phoneme_key (str): Phoneme key
    
    Returns:
        str: Mapped word
    """
    prefix_splitted_string = []
    remaining = text
    index = 0

    while index < len(text):
        splitted_text = split_prefix_name(remaining, ALL_PREFIXES)
        prefix_splitted_string.append(splitted_text)
        remaining = remaining[len(splitted_text):]
        index += len(splitted_text)

    mapped_word = ' '.join(
        get_prefix_splitted_map(entry, phoneme_dict, phoneme_key)
        for entry in prefix_splitted_string
    )

    return mapped_word

def get_raw_unicode(text: str) -> str:
    """
    Converts a string into its raw Unicode escape representation.

    Args:
        text: The input string.

    Returns:
        The string with each character replaced by its \\uXXXX escape sequence.
    """
    return "".join([f"\\u{ord(c):04X}" for c in text])

import unicodedata

def normalize_text(text: str) -> str:
    """
    Normalizes a string to Unicode Normalization Form C (NFC).

    Args:
        text: The input string.

    Returns:
        The normalized string.
    """
    return unicodedata.normalize('NFC', text)

def split_prefix_name(text: str, prefixes: list) -> str:
    """
    Checks if a string starts with any of the given prefixes.

    Args:
        text: The input string.
        prefixes: A list of possible prefixes.

    Returns:
        The matching prefix if found, otherwise the original string.
    """
    for prefix in prefixes:
        if text.startswith(prefix):
            return prefix
    return text

import re

def get_syllable(label: str, burmese_consonant: str, others: str) -> list:
    """
    Splits a label into syllables using a set of regular expression rules.

    Args:
        label: The input string to be split.
        burmese_consonant: A string of Burmese consonants.
        others: A string of other characters.

    Returns:
        A list of syllables.
    """
    reg_exp = re.compile(
        r"(?<![္])([" + burmese_consonant + r"])(?![်္ ့])|([" + others + r"])",
        re.UNICODE,
    )

    reg_label = reg_exp.sub(
        lambda m: f" {m.group(1) or ''}{m.group(2) or ''}", label
    ).strip()

    reg_exp2 = re.compile(r"([က-ၴ])([a-zA-Z0-9])", re.UNICODE)
    reg_label = reg_exp2.sub(r"\1 \2", reg_label)

    reg_exp3 = re.compile(r"([0-9၀-၉])\s+([0-9၀-၉])\s*", re.UNICODE)
    reg_label = reg_exp3.sub(r"\1\2", reg_label)

    reg_exp4 = re.compile(r"([0-9၀-၉])\s+(\+)", re.UNICODE)
    reg_label = reg_exp4.sub(r"\1\2", reg_label).strip()

    return reg_label.split(" ")

def syllable_split(label: str) -> list:
    """
    Splits a string into syllables, first by spaces, then by Burmese rules.

    Args:
        label: The input string.

    Returns:
        A list of syllables.
    """
    burmese_consonant = "ကခဂဃငစဆဇဈညဉဋဌဍဎဏတထဒဓနပဖဗဘမယရလဝသဟဠအ"
    others = r"ဣဤဥဦဧဩဪဿ၌၍၏၀-၉၊။!-/:-@[-`{-~\s.,"

    return [
        syllable
        for word in label.split(" ")
        for syllable in get_syllable(word, burmese_consonant, others)
    ]

def merge_consecutive(lst: list, mapping: dict) -> list:
    """
    Merges consecutive elements in a list if their combination is a key
    in the provided mapping. Prefers the longest possible match.

    Args:
        lst: The input list of strings.
        mapping: The dictionary used for checking and merging.

    Returns:
        A new list with merged elements.
    """
    new_list = []
    i = 0
    max_length = max((len(key) for key in mapping.keys()), default=0)

    while i < len(lst):
        match_found = False

        # Check for the longest possible match
        for length in range(min(max_length, len(lst) - i), 1, -1):
            substring = "".join(lst[i : i + length])
            if substring in mapping:
                new_list.append(substring)
                i += length
                match_found = True
                break

        if not match_found:
            new_list.append(lst[i])
            i += 1
            
    return new_list