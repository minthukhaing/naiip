import models.pali_preprocess as P1
import models.pali_translitor as pp
import json
import asyncio

# ✅ Sync-style file loading moved to background thread
def load_mappings_sync():
    with open('./models/pali_roman_mapping.json', 'r', encoding='utf-8') as f:
        return json.load(f)


# async def load_mappings():
 
#     async with async_open('./models/pali_roman_mapping.json', 'r') as f:
#         response_pali = await f.read()

    
#     mapping_pali = json.loads(response_pali)
#     return  mapping_pali

# ✅ Async wrapper around the sync loader
async def load_mappings():
    return await asyncio.to_thread(load_mappings_sync)

async def parli(text):
    mapped_names = ''
    input_text=text
    mapping_pali= await load_mappings()   
    word_dict=mapping_pali
    #print(word_dict)

    # Step 1: Preprocess
    normalized_text = P1.normalize_text(input_text)
    processed_text1 = P1.preprocess(normalized_text)
    #print("result process text : "+ processed_text1)
    word_list = processed_text1.split(' ')
    
    #print("--------- " + processed_text1)
    #print(word_list)
    mapped_string = ' '.join(P1.get_map(word, word_dict) for word in word_list)
    
    input_code_point = ''.join(hex(ord(char)) for char in processed_text1)
    #output_text= ' '.join(word.capitalize() for word in mapped_string.split())
    output_text = P1.capitalize(mapped_string)
    #print("result str : "+ mapped_string)
    return mapped_string




