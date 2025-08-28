import models.mm_preprocess as p
import models.mm_transpitor as mm
import json
import asyncio
import models.phoneme_preprocess as pp
import models.phoneme_transpitor as pt

# ✅ Sync-style file loading moved to background thread
def load_mappings_sync():
    with open('./models/mm_eng_mapping.json', 'r', encoding='utf-8') as f:
        return json.load(f)
    
def load_mappings_sync_phone():

     # Load mapping for phoneme_mapping.json
    with open('./models/phoneme_mapping.json', 'r', encoding='utf-8') as f:
        response_phoneme = f.read()
        decoded_phoneme = json.loads(response_phoneme)

    # The phoneme mapping is a nested dictionary
    mapping_phoneme = {
        key: value for key, value in decoded_phoneme.items()
    }

    return mapping_phoneme
    

    

# ✅ Async wrapper around the sync loader
async def load_mappings():
    return await asyncio.to_thread(load_mappings_sync)

async def load_mappings_phone():
    return await asyncio.to_thread(load_mappings_sync_phone)

# ✅ Main function
async def myan1(txt):
    input_text = txt
    mapping_mm = await load_mappings()   
    word_dict = mapping_mm

   

    # Step 1: Preprocess
    normalized_text = p.normalize_text(input_text)
    processed_text = p.preprocess(normalized_text)

    word_list = processed_text.split(' ')
    mapped_names = ' '.join(p.get_map(word, word_dict) for word in word_list)
    output_text = ' '.join(p._capitalize(word) for word in mapped_names.split())

    return output_text


async def myan(input_text: str):

    word_dict = await load_mappings()   

    phoneme_dict = await load_mappings_phone()  
    normalized_text = p.normalize_text(input_text) 
    # Step 1: Preprocess
    processed_text = pp.preprocess(normalized_text)

    word_list = processed_text.split(' ')

    mapped_names = ' '.join([p.get_map(word, word_dict) for word in word_list])
    output_text = ' '.join(p._capitalize(word) for word in mapped_names.split())

    mapped_mm_phonemes = ' '.join([pp.get_phoneme_map(word, phoneme_dict, "mm") for word in word_list])

    mapped_ipa_phonemes = ' '.join([pp.get_phoneme_map(word, phoneme_dict, "ipa") for word in word_list])

    # Note: Python doesn't have a direct equivalent of `setState` from Flutter.
    # The output variables are assigned here. You would then use them as needed.

    input_code_point = f"[{', '.join([f'U+{ord(c):04X}' for c in processed_text])}]"

    # For capitalization, use the `title()` or `capitalize()` method.
    # output_text = mapped_names.title()
    output_text_mm_phoneme = f"/{mapped_mm_phonemes}/"
    output_text_ipa_phoneme = f"/{mapped_ipa_phonemes}/"
    # print("------------"+ output_text)
    # print("------------"+ output_text_mm_phoneme)
    # print("------------"+ mapped_ipa_phonemes)
    # You could return the results as a dictionary

    return output_text,output_text_mm_phoneme,output_text_ipa_phoneme
    return {
        "inputCodePoint": input_code_point,
        "outputText": output_text,
        "outputTextMMPhoneme": output_text_mm_phoneme,
        "outputTextIPAPhoneme": output_text_ipa_phoneme,
    }