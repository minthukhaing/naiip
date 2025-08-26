import models.mm_preprocess as p
import json
import asyncio
from aiofile import async_open

async def load_mappings():
    async with async_open('./mm_eng_mapping.json', 'r') as f:
        response_mm = await f.read()
    async with async_open('./pali_roman_mapping.json', 'r') as f:
        response_pali = await f.read()

    mapping_mm = json.loads(response_mm)
    mapping_pali = json.loads(response_pali)
    return  mapping_mm,mapping_pali


async def main():
    mapped_names = ''
    input_text="မင်းသူခိုင်"
    mapping_mm,mapping_pli= await load_mappings()   
    word_dict=mapping_mm
    word_dict1=mapping_pli

    # Step 1: Preprocess
    normalized_text = p.normalize_text(input_text)
    processed_text = p.preprocess(normalized_text)
  
    word_list = processed_text.split(' ')
    mapped_names = ' '.join(p.get_map(word, word_dict) for word in word_list)
   
    input_code_point = ''.join(hex(ord(char)) for char in processed_text)
    output_text= ' '.join(word.capitalize() for word in mapped_names.split())
    #output_text = p.capitalize(mapped_names)
   # print("result str : "+ output_text)

#     ###############################

asyncio.run(main())


