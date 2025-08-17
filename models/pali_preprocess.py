import re
import unicodedata
import models.pali_translitor as pp

all_prefixes = [
    "သဒ္ဓမ္မဇောတိကဓဇ",
    "သဒ္ဓမ္မဇောတိက",
    "ဗဟုဇနဟိတဓရ",
    "ဓမ္မဘဏ္ဍာဂါရိက",
    "ကမ္မဋ္ဌာနာစရိယ",
    "တိပိဋကဓရ",
    "ဓမ္မကထိက",
    "ဂန္ထဝါစက",
    "ဒေါက်တာ",
    "ဒောက်တာ",
    "ဆရာလေး",
    "ဆရာတော်",
    "ပဏ္ဍိတ",
    "အဘိဓဇ",
    "ဘဒ္ဒန္တ",
    "အဂ္ဂ",
    "အူး",
    "ဒေါ်",
    "မဟာ",
    "ရှင်မဟာ",
    "ရှင်",
    "အရှင်",
    "အသျှင်",
    "မ",
]

def preprocess(text):
    replacements = [
        ("ဿ", "သ္သ"),
        ("ည", "ဉ္ဉ"),
        ("\u1026\u1038", "အူး"),
        ("ဥူး", "အူး"),
        ("\u1026", "အူ"),
        ("ဥူ", "အူ"),
        ("ဥုံ", "အုံ"),
        ("ဥု", "အူ"),
        ("ဥ", "အု"),
        ("န်ုပ်", "န်နုပ်"),
        ("ဪ", "အော်"),
        ("ဩ", "အော"),
        ("ဤ", "အီ"),
        ("၏", "အိ"),
        ("ဧ", "အေ"),
        ("ဣိ", "အိ"),
        ("ဣီ", "အီ"),
        ("ဣူ", "အူ"),
        ("ဣု", "အု"),
        ("ဣ", "အိ"),
        ("၍", "ရွေ့"),
        ("၎င်း", "လည်းကောင်း"),
        ("၌", "နှိုက်"),
    ]
    
    for old, new in replacements:
        text = text.replace(old, new)
    
    text = re.sub(r'[\u200B\u200C]', '', text)
    return text

def flatten_stack(text):
    stack_patterns = [
        re.compile(r"([\u1000-\u1020])\u1039", re.UNICODE),
        re.compile(r"([\u1000-\u1020\u1004\u103A])\u1039", re.UNICODE),
    ]

    for index, pattern in enumerate(stack_patterns):
        while pattern.search(text):
            if index == 0:
                text = pattern.sub(lambda m: f"{m.group(1)}\u103A", text)
            else:
                text = pattern.sub(lambda m: m.group(1), text)
    
    return text



def get_pali_mapping(label):
    romanized = pp.transliterate(label)
    return romanized

def syllable_split(text):
    # Implement your syllable splitting logic here
    # This is a placeholder implementation
    return [text]

def get_prefix_spilitted_map(text, word_dict):
    if text in word_dict and word_dict[text] != "":
        mapped_prefix = word_dict[text].capitalize()
    else:
        flattened_text = flatten_stack(text)
        syllable_list = syllable_split(flattened_text)
        mapped_prefix = ''.join(get_pali_mapping(syllable) for syllable in syllable_list)
    
    return mapped_prefix.capitalize()

def split_prefix_name(text, prefixes):
    # Implement your prefix splitting logic here
    # This is a placeholder implementation
    for prefix in sorted(prefixes, key=len, reverse=True):
        if text.startswith(prefix):
            return prefix
    return text[0]

def capitalize(string):
    return string if not string else string[0].upper() + string[1:]

def get_map(text, word_dict):
    prefix_spilitted_string = []
    remaining = text
    index = 0

    while index < len(text):
        prefix = split_prefix_name(remaining, all_prefixes)
        prefix_spilitted_string.append(prefix)
        remaining = remaining[len(prefix):]
        index += len(prefix)

    mapped_word = ' '.join(
        get_prefix_spilitted_map(entry, word_dict) 
        for entry in prefix_spilitted_string
    )

    return mapped_word
def get_raw_unicode(text):
    """Return the raw Unicode representation of the input text."""
    return ''.join(f'\\u{ord(c):04X}' for c in text)

def normalize_text(text):
    """Normalize the input text using NFC (Normalization Form C)."""
    return unicodedata.normalize('NFC', text)

def split_prefix_name(text, prefixes):
    """Split the input text into prefix and name if the text starts with any of the given prefixes."""
    for prefix in prefixes:
        if text.startswith(prefix):
            return prefix
    return text

def get_syllable(label, burmese_consonant, others):
    """
    Split the input label into syllables based on Burmese consonants and other characters.
    
    Args:
        label (str): The input label to split into syllables.
        burmese_consonant (str): A string of Burmese consonants.
        others (str): A string of other characters.
    
    Returns:
        list: A list of syllables.
    """
    # Regular expression pattern to match Burmese consonants and other characters
    pattern = re.compile(r'(?<![္])([' + burmese_consonant + r'])(?![်္ ့])|([' + others + r'])', re.UNICODE)
    
    # Replace matches with a space-separated string
    reg_label = re.sub(pattern, lambda match: f" {match.group(1) or ''}{match.group(2) or ''}", label).strip()
    
    # Regular expression pattern to match Burmese consonants followed by Latin characters
    pattern2 = re.compile(r'([က-ၴ])([a-zA-Z0-9])', re.UNICODE)
    
    # Replace matches with a space-separated string
    reg_label = re.sub(pattern2, lambda match: f"{match.group(1)} {match.group(2)}", reg_label)
    
    # Regular expression pattern to match consecutive digits or Myanmar digits
    pattern3 = re.compile(r'([0-9၀-၉])\s+([0-9၀-၉])\s*', re.UNICODE)
    
    # Replace matches with a concatenated string
    reg_label = re.sub(pattern3, lambda match: f"{match.group(1)}{match.group(2)}", reg_label)
    
    # Regular expression pattern to match digits or Myanmar digits followed by a plus sign
    pattern4 = re.compile(r'([0-9၀-၉])\s+(\+)', re.UNICODE)
    
    # Replace matches with a concatenated string
    reg_label = re.sub(pattern4, lambda match: f"{match.group(1)}{match.group(2)}", reg_label).strip()
    
    # Split the resulting string into syllables
    return reg_label.split()

def syllable_split(label):
    """
    Split the input label into syllables.
    
    Args:
        label (str): The input label to split into syllables.
    
    Returns:
        list: A list of syllables.
    """
    burmese_consonant = 'ကခဂဃငစဆဇဈညဉဋဌဍဎဏတထဒဓနပဖဗဘမယရလဝသဟဠအ'
    others = r'ဣဤဥဦဧဩဪဿ၌၍၏၀-၉၊။!-/:-@[-`{-~\s.,'
    
    # Split the label into words and then split each word into syllables
    return [syllable for word in label.split() for syllable in get_syllable(word, burmese_consonant, others)]

def merge_consecutive(lst, mapping):
    """
    Merge consecutive elements in the input list based on the given mapping.
    
    Args:
        lst (list): The input list to merge consecutive elements.
        mapping (dict): A dictionary mapping consecutive elements to their merged values.
    
    Returns:
        list: The merged list.
    """
    new_list = []
    max_length = max(len(key) for key in mapping.keys())
    
    i = 0
    while i < len(lst):
        match_found = False
        
        # Check for the longest possible match (max_length -> 2)
        for length in range(max_length, 1, -1):
            if i + length <= len(lst):
                substring = ''.join(lst[i:i + length])
                if substring in mapping:
                    # new_list.append(mapping[substring])  # Replace with mapped value
                    new_list.append(substring)  # Replace with mapped key
                    i += length
                    match_found = True
                    break
        
        if not match_found:
            new_list.append(lst[i])
            i += 1
    
    return new_list

# Example usage:
label = "မြန်မာစာ"
burmese_consonant = 'ကခဂဃငစဆဇဈညဉဋဌဍဎဏတထဒဓနပဖဗဘမယရလဝသဟဠအ'
others = r'ဣဤဥဦဧဩဪဿ၌၍၏၀-၉၊။!-/:-@[-`{-~\s.,'