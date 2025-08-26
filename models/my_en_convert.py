import models.mm_preprocess as p
import models.mm_transpitor as mm
import json
import asyncio

# ✅ Sync-style file loading moved to background thread
def load_mappings_sync():
    with open('./models/mm_eng_mapping.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# ✅ Async wrapper around the sync loader
async def load_mappings():
    return await asyncio.to_thread(load_mappings_sync)

# ✅ Main function
async def myan(txt):
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
