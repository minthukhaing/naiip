import re

singleton = {
            "က": "k",
            "ခ": "kh",
            "ဂ": "g",
            "ဃ": "gg",
            "င": "ng",
            "စ": "s",
            "ဆ": "hs",
            "ဇ": "z",
            "ဈ": "zz",
            "ဉ": "ny",
            "ည": "ny",
            "ဋ": "tt",
            "ဌ": "htt",
            "ဍ": "dd",
            "ဎ": "dd",
            "ဏ": "nm",
            "တ": "t",
            "ထ": "ht",
            "ဒ": "d",
            "ဓ": "dd",
            "န": "n",
            "ပ": "p",
            "ဖ": "ph",
            "ဗ": "bb",
            "ဘ": "b",
            "မ": "m",
            "ယ": "y",
            "ရ": "r",
            "လ": "l",
            "ဝ": "w",
            "သ": "th",
            "ဟ": "h",
            "ဠ": "ll",
            "အ": "",
            "ဧ": "ayy"

            
        }
vowelForm = {
            "ာ": "ar",
            "ါ": "ar",
            "ိ": "ei",
            "ီ": "e",
            "ု": "u",
            "ူ": "uu",
            "ေ": "ay",
            #"ေ": "e",
            "ံ": "am",
            "ဲ": "ell",
            "ှ": "h"
        }
specialCharsForm = {
            "၁": "1",
            "၂": "2",
            "၃": "3",
            "၄": "4",
            "၅": "5",
            "၆": "6",
            "၇": "7",
            "၈": "8",
            "၉": "9",
            "၀": "0",
            "၊": ",",
            "။": "."
        }

asatExtendedForm = {
    "\u103e\u1031\u102c\u1000\u103a": "auk",  # ငှောက်
    "\u103e\u1031\u102c\u1002\u103a": "auk",  # ကောဂ်
    "\u103e\u1031\u102c\u1004\u103a\u1038": "oung",  # ကောင်း
    "\u103e\u1031\u102c\u1004\u1037\u103a": "ount",  # ကောင့်
    "\u103e\u1031\u102c\u1004\u103a": "aung",  # ကောင်
    "\u103e\u1031\u102c\u1005\u103a": "auk",  # ကောစ်
    "\u103e\u1031\u102c\u1007\u103a": "auk",  # ကောဇ်
    "\u103e\u1031\u102c\u1009\u103a\u1038": "oung",  # ကောဉ်း
    "\u103e\u1031\u102c\u1009\u1037\u103a": "ount",  # ကောဉ့်
    "\u103e\u1031\u102c\u1009\u103a": "aung",  # ကောဉ်
    "\u103e\u1031\u102c\u100a\u103a\u1038": "oung",  # ကောည်း
    "\u103e\u1031\u102c\u100a\u1037\u103a": "ount",  # ကောည့်
    "\u103e\u1031\u102c\u100a\u103a": "aung",  # ကောည်
    "\u103e\u1031\u102c\u100b\u103a": "auk",  # ကောဋ်
    "\u103e\u1031\u102c\u100d\u103a": "auk",  # ကောဍ်
    "\u103e\u1031\u102c\u100f\u103a\u1038": "oung",  # ကောဏ်း
    "\u103e\u1031\u102c\u100f\u1037\u103a": "ount", # ကောဏ့်
    "\u103e\u1031\u102c\u100f\u103a": "aung", # ကောဏ်
    "\u103e\u1031\u102c\u1010\u103a": "auk", # ကောတ်
    "\u103e\u1031\u102c\u1012\u103a": "auk", # ကောဒ်
    "\u103e\u1031\u102c\u1014\u103a\u1038": "oung", # ကောန်း
    "\u103e\u1031\u102c\u1014\u1037\u103a": "ount", # ကောန့်
    "\u103e\u1031\u102c\u1014\u103a": "aung", # ကောန်
    "\u103e\u1031\u102c\u1015\u103a": "auk", # ကောပ်
    "\u103e\u1031\u102c\u1017\u103a": "auk", # ကောဗ်
    "\u103e\u1031\u102c\u1019\u103a\u1038": "oumg", # ကောမ်း
    "\u103e\u1031\u102c\u1019\u1037\u103a": "oumt", # ကောမ့်
    "\u103e\u1031\u102c\u1019\u103a": "aumg", # ကောမ်
    "\u103e\u1031\u102c\u101a\u1037\u103a": "auk", # ကောယ့်
    "\u103e\u1031\u102c\u101a\u103a": "auk", # ကောယ်
    "\u103e\u1031\u102c\u101b\u103a": "au", # ကောရ်
    "\u103e\u1031\u102c\u101c\u103a": "aung", # ကောလ်
    "\u103e\u1031\u102c\u101d\u103a": "auk", # ကောဝ်
    "\u103e\u1031\u102c\u101e\u103a": "auk", # ကောသ်
    "\u103e\u1031\u102c\u101f\u103a": "aun", # ကောဟ်
    "\u1031\u102c\u1000\u103a": "auk", # ကောက်
    "\u1031\u102c\u1002\u103a": "auk", # ကောဂ်
    "\u1031\u102c\u1004\u103a\u1038": "oung", # ကောင်း
    "\u1031\u102c\u1004\u1037\u103a": "ount", # ကောင့်
    "\u1031\u102c\u1004\u103a": "aung", # ကောင်
    "\u1031\u102c\u1005\u103a": "auk", # ကောစ်
    "\u1031\u102c\u1007\u103a": "auk", # ကောဇ်
    "\u1031\u102c\u1009\u103a\u1038": "oung", # ကောဉ်း
    "\u1031\u102c\u1009\u1037\u103a": "ount", # ကောဉ့်
    "\u1031\u102c\u1009\u103a": "aung", # ကောဉ်
    "\u1031\u102c\u100a\u103a\u1038": "oung", # ကောည်း
    "\u1031\u102c\u100a\u1037\u103a": "ount", # ကောည့်
    "\u1031\u102c\u100a\u103a": "aung", # ကောည်
    "\u1031\u102c\u100b\u103a": "auk", # ကောဋ်
    "\u1031\u102c\u100d\u103a": "auk", # ကောဍ်
    "\u1031\u102c\u100f\u103a\u1038": "oung", # ကောဏ်း
    "\u1031\u102c\u100f\u1037\u103a": "ount", # ကောဏ့်
    "\u1031\u102c\u100f\u103a": "aung", # ကောဏ်
    "\u1031\u102c\u1010\u103a": "auk", # ကောတ်
    "\u1031\u102c\u1012\u103a": "auk", # ကောဒ်
    "\u1031\u102c\u1014\u103a\u1038": "oung", # ကောန်း
    "\u1031\u102c\u1014\u1037\u103a": "ount", # ကောန့်
    "\u1031\u102c\u1014\u103a": "aung", # ကောန်
    "\u1031\u102c\u1015\u103a": "auk", # ကောပ်
    "\u1031\u102c\u1017\u103a": "auk", # ကောဗ်
    "\u1031\u102c\u1019\u103a\u1038": "oumg", # ကောမ်း
    "\u1031\u102c\u1019\u1037\u103a": "oumt", # ကောမ့်
    "\u1031\u102c\u1019\u103a": "aumg", # ကောမ်
    "\u1031\u102c\u101a\u1037\u103a": "auk", # ကောယ့်
    "\u1031\u102c\u101a\u103a": "auk", # ကောယ်
    "\u1031\u102c\u101b\u103a": "au", # ကောရ်
    "\u1031\u102c\u101c\u103a": "aung", # ကောလ်
    "\u1031\u102c\u101d\u103a": "auk", # ကောဝ်
    "\u1031\u102c\u101e\u103a": "auk", # ကောသ်
    "\u1031\u102c\u101f\u103a": "aun", # ကောဟ်
     "\u103e\u1031\u102b\u1000\u103a": "auk", # ငှေါက်
    "\u103e\u1031\u102b\u1002\u103a": "auk", # ခေါဂ်
    "\u103e\u1031\u102b\u1004\u103a\u1038": "oung", # ကေါင်း
    "\u103e\u1031\u102b\u1004\u1037\u103a": "ount", # ကေါင့်
    "\u103e\u1031\u102b\u1004\u103a": "aung", # ကေါင်
    "\u103e\u1031\u102b\u1005\u103a": "auk", # ကေါစ်
    "\u103e\u1031\u102b\u1007\u103a": "auk", # ကေါဇ်
    "\u103e\u1031\u102b\u1009\u103a\u1038": "oung", # ကေါဉ်း
    "\u103e\u1031\u102b\u1009\u1037\u103a": "ount", # ကေါဉ့်
    "\u103e\u1031\u102b\u1009\u103a": "aung", # ကေါဉ်
    "\u103e\u1031\u102b\u100a\u103a\u1038": "oung", # ကေါည်း
    "\u103e\u1031\u102b\u100a\u1037\u103a": "ount", # ကေါည့်
    "\u103e\u1031\u102b\u100a\u103a": "aung", # ကေါည်
    "\u103e\u1031\u102b\u100b\u103a": "auk", # ကေါဋ်
    "\u103e\u1031\u102b\u100d\u103a": "auk", # ကေါဍ်
    "\u103e\u1031\u102b\u100f\u103a\u1038": "oung", # ကေါဏ်း
    "\u103e\u1031\u102b\u100f\u1037\u103a": "ount", # ကေါဏ့်
    "\u103e\u1031\u102b\u100f\u103a": "aung", # ကေါဏ်
    "\u103e\u1031\u102b\u1010\u103a": "auk", # ကေါတ်
    "\u103e\u1031\u102b\u1012\u103a": "auk", # ကေါဒ်
    "\u103e\u1031\u102b\u1014\u103a\u1038": "oung", # ကေါန်း
    "\u103e\u1031\u102b\u1014\u1037\u103a": "ount", # ကေါန့်
    "\u103e\u1031\u102b\u1014\u103a": "aung", # ကေါန်
    "\u103e\u1031\u102b\u1015\u103a": "auk", # ကေါပ်
    "\u103e\u1031\u102b\u1017\u103a": "auk", # ကေါဗ်
    "\u103e\u1031\u102b\u1019\u103a\u1038": "oumg", # ကေါမ်း
    "\u103e\u1031\u102b\u1019\u1037\u103a": "oumt", # ကေါမ့်
    "\u103e\u1031\u102b\u1019\u103a": "aumg", # ကေါမ်
    "\u103e\u1031\u102b\u101a\u1037\u103a": "auk", # ကေါယ့်
    "\u103e\u1031\u102b\u101a\u103a": "auk", # ကေါယ်
    "\u103e\u1031\u102b\u101b\u103a": "auk", # ကေါရ်
    "\u103e\u1031\u102b\u101c\u103a": "aung", # ကေါလ်
    "\u103e\u1031\u102b\u101d\u103a": "auk", # ကေါဝ်
    "\u103e\u1031\u102b\u101e\u103a": "auk", # ကေါသ်
    "\u103e\u1031\u102b\u101f\u103a": "aun", # ကေါဟ်
    "\u1031\u102b\u1000\u103a": "auk", # ခေါက်
    "\u1031\u102b\u1002\u103a": "auk", # ခေါဂ်
    "\u1031\u102b\u1004\u103a\u1038": "oung", # ကေါင်း
    "\u1031\u102b\u1004\u1037\u103a": "ount", # ကေါင့်
    "\u1031\u102b\u1004\u103a": "aung", # ကေါင်
    "\u1031\u102b\u1005\u103a": "auk", # ကေါစ်
    "\u1031\u102b\u1007\u103a": "auk", # ကေါဇ်
    "\u1031\u102b\u1009\u103a\u1038": "oung", # ကေါဉ်း
    "\u1031\u102b\u1009\u1037\u103a": "ount", # ကေါဉ့်
    "\u1031\u102b\u1009\u103a": "aung", # ကေါဉ်
    "\u1031\u102b\u100a\u103a\u1038": "oung", # ကေါည်း
    "\u1031\u102b\u100a\u1037\u103a": "ount", # ကေါည့်
    "\u1031\u102b\u100a\u103a": "aung", # ကေါည်
    "\u1031\u102b\u100b\u103a": "auk", # ကေါဋ်
    "\u1031\u102b\u100d\u103a": "auk", # ကေါဍ်
    "\u1031\u102b\u100f\u103a\u1038": "oung", # ကေါဏ်း
    "\u1031\u102b\u100f\u1037\u103a": "ount", # ကေါဏ့်
    "\u1031\u102b\u100f\u103a": "aung", # ကေါဏ်
    "\u1031\u102b\u1010\u103a": "auk", # ကေါတ်
    "\u1031\u102b\u1012\u103a": "auk", # ကေါဒ်
    "\u1031\u102b\u1014\u103a\u1038": "oung", # ကေါန်း
    "\u1031\u102b\u1014\u1037\u103a": "ount", # ကေါန့်
    "\u1031\u102b\u1014\u103a": "aung", # ကေါန်
    "\u1031\u102b\u1015\u103a": "auk", # ကေါပ်
    "\u1031\u102b\u1017\u103a": "auk", # ကေါဗ်
    "\u1031\u102b\u1019\u103a\u1038": "oumg", # ကေါမ်း
    "\u1031\u102b\u1019\u1037\u103a": "oumt", # ကေါမ့်
    "\u1031\u102b\u1019\u103a": "aumg", # ကေါမ်
    "\u1031\u102b\u101a\u1037\u103a": "auk", # ကေါယ့်
    "\u1031\u102b\u101a\u103a": "auk", # ကေါယ်
    "\u1031\u102b\u101b\u103a": "auk", # ကေါရ်
    "\u1031\u102b\u101c\u103a": "aung", # ကေါလ်
    "\u1031\u102b\u101d\u103a": "auk", # ကေါဝ်
    "\u1031\u102b\u101e\u103a": "auk", # ကေါသ်
    "\u1031\u102b\u101f\u103a": "aun", # ကေါဟ်
    "\u1031\u101e\u103a": "it", 
    "\u103e\u1031\u1010\u103a": "it",
    "\u1031\u1010\u103a": "it", 
    "\u1031\u100a\u1037\u103a": "ei", 
    "\u1031\u100a\u103a": "i",
    "က်ျာ": "atyar", 
    "ှိုက်": "aik",
    "ှိုဂ်": "aik",
    "ှိုင်း": "ine",
    "ှိုင့်": "aint",
    "ှိုင်": "aing",
    "ှိုစ်": "aik",
    "ှိုဇ်": "aik",
    "ှိုဉ်း": "ainn",
    "ှိုဉ့်": "ainnt",
    "ှိုဉ်": "aiin",
    "ှိုည်း": "aine",
    "ှိုည့်": "aint",
    "ှိုည်": "aing",
    "ှိုဋ်": "aik",
    "ှိုဍ်": "aik",
    "ှိုဏ်း": "inme",
    "ှိုဏ့်": "inmt",
    "ှိုဏ်": "inmg",
    "ှိုတ်": "aik",
    "ှိုဒ်": "aik",
    "ှိုန်း": "aine",
    "ှိုန့်": "aint",
    "ှိုန်": "aing",
    "ှိုပ်": "aik",
    "ှိုဗ်": "aik",
    "ှိုမ်း": "aime",
    "ှိုမ့်": "aimt",
    "ှိုမ်": "aimg",
    "ှိုယ့်": "oh",
    "ှိုယ်": "o",
    "ှိုရ်": "o",
    "ှိုလ်": "o",
    "ှိုဝ်": "o",
    "ှိုသ်": "aik",
    "ှိုဟ်": "ain",
    "ိုက်": "aik",
    "ိုဂ်": "aik",
    "ိုင်း": "ine",
    "ိုင့်": "aint",
    "ိုင်": "aing",
    "ိုစ်": "aik",
    "ိုဇ်": "aik",
    "ိုဉ်း": "ainn",
    "ိုဉ့်": "ainnt",
    "ိုဉ်": "aiing",
    "ိုည်း": "aine",
    "ိုည့်": "aint",
    "ိုည်": "aing",
    "ိုဋ်": "aik",
    "ိုဍ်": "aik",
    "ိုဏ်း": "ainme",
    "ိုဏ့်": "ainmt",
    "ိုဏ်": "ainmg",
    "ိုတ်": "aik",
    "ိုဒ်": "aik",
    "ိုန်း": "aine",
    "ိုန့်": "aint",
    "ိုန်": "aing",
    "ိုပ်": "aik",
    "ိုဗ်": "aik",
    "ိုမ်း": "aime",
    "ိုမ့်": "aimt",
    "ိုမ်": "aimg",
    "ိုယ့်": "oh",
    "ိုယ်": "o",
    "ိုရ်": "o",
    "ိုလ်": "o",
    "ိုဝ့်": "oh",
    "ိုဝ်": "o",
    "ိုသ်": "aik",
    "ိုဟ်": "o",
    "ှာက်": "et",
    "ှာဂ်": "et",
    "ှာင်း": "inn",
    "ှာင့်": "int",
    "ှာင်": "in",
    "ှာစ်": "it",
    "ှာဇ်": "it",
    "ှာဉ်း": "inn",
    "ှာဉ့်": "innt",
    "ှာဉ်": "in",
    "ှာည်း": "ee",
    "ှာည့်": "ei",
    "ှာည်": "i",
    "ှာဋ်": "at",
    "ှာဍ်": "at",
    "ှာဏ်း": "anm",
    "ှာဏ့်": "anmt",
    "ှာဏ်": "anm",
    "ှာတ်": "at",
    "ှာဒ်": "at",
    "ှာန်း": "ann",
    "ှာန့်": "ant",
    "ှာန်": "an",
    "ှာပ်": "ap",
    "ှာဗ်": "ap",
    "ှာမ်း": "amm",
    "ှာမ့်": "amt",
    "ှာမ်": "am",
    "ှာယ့်": "ellt",
    "ှာယ်": "el",
    "ှာရ်": "an",
    "ှာလ်": "an",
    "ှာဝ်": "ap",
    "ှာသ်": "at",
    "ှာဟ်": "an",
    "ာက်": "et",
    "ာဂ်": "et",
    "ာင်း": "inn",
    "ာင့်": "int",
    "ာင်": "in",
    "ာစ်": "it",
    "ာဇ်": "it",
    "ာဉ်း": "inn",
    "ာဉ့်": "innt",
    "ာဉ်": "in",
    "ာည်း": "ee",
    "ာည့်": "ei",
    "ာည်": "i",
    "ာဋ်": "at",
    "ာဍ်": "at",
    "ာဏ်း": "anmm",
    "ာဏ့်": "anmt",
    "ာဏ်": "anm",
    "ာတ်": "at",
    "ာဒ်": "at",
    "ာန်း": "ann",
    "ာန့်": "ant",
    "ာန်": "an",
    "ာပ်": "ap",
    "ာဗ်": "ap",
    "ာမ်း": "amm",
    "ာမ့်": "amt",
    "ာမ်": "am",
    "ာယ့်": "ellt",
    "ာယ်": "el",
    "ာရ်": "an",
    "ာလ်": "an",
    "ာဝ်": "ap",
    "ာသ်": "at",
    "ာဟ်": "an",
    "ါက်": "et",
    "ါဂ်": "et",
    "ါင်း": "inn",
    "ါင့်": "int",
    "ါင်": "in",
    "ါစ်": "it",
    "ါဇ်": "it",
    "ါဉ်း": "inn",
    "ါဉ့်": "innt",
    "ါဉ်": "iin",
    "ါည်း": "ee",
    "ါည့်": "ei",
    "ါည်": "i",
    "ါဋ်": "at",
    "ါဍ်": "at",
    "ါဏ်း": "anmm",
    "ါဏ့်": "anmt",
    "ါဏ်": "anm",
    "ါတ်": "at",
    "ါဒ်": "at",
    "ါန်း": "ann",
    "ါန့်": "ant",
    "ါန်": "an",
    "ါပ်": "ap",
    "ါဗ်": "ap",
    "ါမ်း": "amm",
    "ါမ့်": "amt",
    "ါမ်": "am",
    "ါယ့်": "ellt",
    "ါယ်": "el",
    "ါရ်": "an",
    "ါလ်": "an",
    "ါဝ်": "ap",
    "ါသ်": "at",
    "ါဟ်": "an",
    "ှိက်": "eik",
    "ှိဂ်": "eik",
    "ှိင်း": "einn",
    "ှိင့်": "eint",
    "ှိင်": "ein",
    "ှိစ်": "eik",
    "ှိဇ်": "eik",
    "ှိဉ်း": "einn",
    "ှိဉ့်": "einnt",
    "ှိဉ်": "eiin",
    "ှိည်း": "einn",
    "ှိည့်": "eint",
    "ှိည်": "ein",
    "ှိဋ်": "eik",
    "ှိဍ်": "eik",
    "ှိဏ်း": "einmm",
    "ှိဏ့်": "einmt",
    "ှိဏ်": "einm",
    "ှိတ်": "eik",
    "ှိဒ်": "eik",
    "ှိန်း": "einn",
    "ှိန့်": "eint",
    "ှိန်": "ein",
    "ှိပ်": "eik",
    "ှိဗ်": "eik",
    "ှိမ်း": "eimm",
    "ှိမ့်": "eimt",
    "ှိမ်": "eim",
    "ှိယ့်": "eik",
    "ှိယ်": "eik",
    "ှိရ်": "eik",
    "ှိလ်": "ein",
    "ှိဝ်": "eik",
    "ှိသ်": "eik",
    "ှိဟ်": "ein",
    "ိက်": "eik",
    "ိဂ်": "eik",
    "ိင်း": "einn",
    "ိင့်": "eint",
    "ိင်": "ein",
    "ိစ်": "eik",
    "ိဇ်": "eik",
    "ိဉ်း": "einn",
    "ိဉ့်": "einnt",
    "ိဉ်": "eiin",
    "ိည်း": "einn",
    "ိည့်": "eint",
    "ိည်": "ein",
    "ိဋ်": "eik",
    "ိဍ်": "eik",
    "ိဏ်း": "einmm",
    "ိဏ့်": "einmt",
    "ိဏ်": "einm",
    "ိတ်": "eik",
    "ိဒ်": "eik",
    "ိန်း": "einn",
    "ိန့်": "eint",
    "ိန်": "ein",
    "ိပ်": "ake",
    "ိဗ်": "ake",
    "ိမ်း": "eimm",
    "ိမ့်": "eimt",
    "ိမ်": "eim",
    "ိယ့်": "eik",
    "ိယ်": "eik",
    "ိရ်": "eik",
    "ိလ်": "ein",
    "ိဝ်": "eik",
    "ိသ်": "eik",
    "ိဟ်": "ein",
    "ိံ": "ein",
    "ှုက်": "oak",
    "ှုဂ်": "oak",
    "ှုင်း": "one",
    "ှုင့်": "ont",
    "ှုင်": "oun",
    "ှုစ်": "oat",
    "ှုဇ်": "oat",
    "ှုဉ်း": "one",
    "ှုဉ့်": "ont",
    "ှုဉ်": "oun",
    "ှုည်း": "one",
    "ှုည့်": "ont",
    "ှုည်": "oun",
    "ှုဋ်": "oat",
    "ှုဍ်": "oat",
    "ှုဏ်း": "onme",
    "ှုဏ့်": "onmt",
    "ှုဏ်": "ounm",
    "ှုတ်": "oak",
    "ှုဒ်": "oak",
    "ှုန်း": "one",
    "ှုန့်": "ont",
    "ှုန်": "oun",
    "ှုပ်": "oke",
    "ှုဗ်": "oke",
    "ှုမ်း": "ome",
    "ှုမ့်": "omt",
    "ှုမ်": "oum",
    "ှုယ့်": "omt",
    "ှုယ်": "oun",
    "ှုရ်": "oun",
    "ှုလ်": "oun",
    "ှုဝ်": "oat",
    "ှုသ်": "oat",
    "ှုဟ်": "oan",
    "ုက်": "oak",
    "ုဂ်": "oak",
    "ုင်း": "one",
    "ုင့်": "ont",
    "ုင်": "oun",
    "ုစ်": "oat",
    "ုဇ်": "oat",
    "ုဉ်း": "one",
    "ုဉ့်": "ont",
    "ုဉ်": "oun",
    "ုည်း": "one",
    "ုည့်": "ont",
    "ုည်": "oun",
    "ုဋ်": "oat",
    "ုဍ်": "oat",
    "ုဏ်း": "onme",
    "ု့ဏ်": "onmt",
    "ုဏ်": "ounm",
    "ုတ်": "oat",
    "ုဒ်": "oak",
    "ုန်း": "one",
    "ုန့်": "ont",
    "ုန်": "oun",
    "ုပ်": "oke",
    "ုဗ်": "oke",
    "ုမ်း": "ome",
    "ုမ့်": "omt",
    "ုမ်": "oum",
    "ုယ့်": "omt",
    "ုယ်": "oun",
    "ုရ်": "oun",
    "ုလ်": "oun",
    "ုဝ်": "oat",
    "ုသ်": "oat",
    "ုဟ်": "oan",
    "ှက်": "et",
    "ှဂ်": "et",
    "ှင်း": "inn",
    "ှင့်": "int",
    "ှင်": "in",
    "ှစ်": "it",
    "ှဇ်": "it",
    "ှဉ်း": "inn",
    "ှဉ့်": "innt",
    "ှဉ်": "iin",
    "ှည်း": "ee",
    "ှည့်": "ei",
    "ှည်": "i",
    "ှဋ်": "at",
    "ှဍ်": "at",
    "ှဏ်း": "anmm",
    "ှဏ့်": "anmt",
    "ှဏ်": "anm",
    "ှတ်": "at",
    "ှဒ်": "at",
    "ှန်း": "ann",
    "ှန့်": "ant",
    "ှန်": "an",
    "ှပ်": "ap",
    "ှဗ်": "ap",
    "ှမ်း": "amm",
    "ှမ့်": "amt",
    "ှမ်": "am",
    "ှယ့်": "ellt",
    "ှယ်": "el",
    "ှရ်": "el",
    "ှလ်": "an",
    "ှဝ်": "ap",
    "ှသ်": "at",
    "ှဟ်": "an",
    
    "က်": "et",
    "ဂ်": "et",
    "င်း": "inn",
    "င့်": "int",
    "င်": "in",
    "စ်": "it",
    "ဇ်": "it",
    "ဉ်း": "iinn",
    "ဉ့်": "iint",
    "ဉ်": "iin",
    "ည်း": "ii",
    "ည့်": "ei",
    "ည်": "i",
    "ဋ်": "at",
    "ဍ်": "at",
    "ဏ်း": "anmm",
    "ဏ့်": "anmt",
    "ဏ်": "anm",
    "တ်": "at",
    "ဒ်": "at",
    "န်း": "ann",
    "န့်": "ant",
    "န်": "an",
    "ပ်": "ap",
    "ဗ်": "ap",
    "မ်း": "amm",
    "မ့်": "amt",
    "မ်": "am",
    "ယ့်": "ellt",
    "ယ်": "el",
    "ရ်": "el",
    "လ်": "an",
    "ဝ်": "ap",
    "သ်": "at",
    "ဟ်": "an",
    "\u1031ရ်": "ay",
    "ွှိူက်": "waik",
    "ွှိုဂ်": "waik",
    "ွှိုင်း": "wine",
    "ွှိုင့်": "waint",
    "ွှိုင်": "waing",
    "ွှိုစ်": "waik",
    "ွှိုဇ်": "waik",
    "ွှိုဉ်း": "wainn",
    "ွှိုဉ့်": "wainnt",
    "ွှိုဉ်": "waiing",
    "ွှိုည်း": "waine",
    "ွှိုည့်": "waint",
    "ွှိုည်": "waing",
    "ွှိုဋ်": "waik",
    "ွှိုဍ်": "waik",
    "ွှိုဏ်း": "wainme",
    "ွှိုဏ့်": "wainmt",
    "ွှိုဏ်": "wainmg",
    "ွှိူတ်": "waik",
    "ွှိုဒ်": "waik",
    "ွှိုန်း": "waine",
    "ွှိုန့်": "waint",
    "ွှိုန်": "waing",
    "ွှိုပ်": "waik",
    "ွှိုဗ်": "waik",
    "ွှိုမ်း": "waime",
    "ွှိုမ့်": "waimt",
    "ွှိုမ်": "waimg",
    "ွှိုယ့်": "woh",
    "ွှိုယ်": "wo",
    "ွှိုရ်": "wo",
    "ွှိုလ်": "wo",
    "ွှိုဝ်": "wo",
    "ွှိုသ်": "waik",
    "ွှိုဟ်": "wain",
    "ွိုက်": "waik",
    "ွိုဂ်": "waik",
    "ွိုင်း": "wine",
    "ွိုင့်": "waint",
    "ွိုင်": "waing",
    "ွိုစ်": "waik",
    "ွိုဇ်": "waik",
    "ွိုဉ်း": "wainn",
    "ွိုဉ့်": "wainnt",
    "ွိုဉ်": "waiin",
    "ွိုည်း": "waine",
    "ွိုည့်": "waint",
    "ွိုည်": "waing",
    "ွိုဋ်": "waik",
    "ွိုဍ်": "waik",
    "ွိုဏ်း": "wainme",
    "ွိုဏ့်": "wainmt",
    "ွိုဏ်": "wainmg",
    "ွိုတ်": "waik",
    "ွိုဒ်": "waik",
    "ွိုန်း": "waine",
    "ွိုန့်": "waint",
    "ွိုန်": "waing",
    "ွိုပ်": "waik",
    "ွိုဗ်": "waik",
    "ွိုမ်း": "waime",
    "ွိုမ့်": "waimt",
    "ွိုမ်": "waimg",
    "ွိုယ့်": "woh",
    "ွိုယ်": "wo",
    "ွိုရ်": "wo",
    "ွိုလ်": "wo",
    "ွိုဝ်": "wo",
    "ွိုသ်": "waik",
    "ွိုဟ်": "wain",
    "ွှိက်": "weik",
    "ွှိဂ်": "weik",
    "ွှိင်း": "weinn",
    "ွှိင့်": "weint",
    "ွှိင်": "wein",
    "ွှိစ်": "weik",
    "ွှိဇ်": "weik",
    "ွှိဉ်း": "weinn",
    "ွှိဉ့်": "weinnt",
    "ွှိဉ်": "weiin",
    "ွှိည်း": "weinn",
    "ွှိည့်": "weint",
    "ွှိည်": "wein",
    "ွှိဋ်": "weik",
    "ွှိဍ်": "weik",
    "ွှိဏ်း": "weinmm",
    "ွှိဏ့်": "weinmt",
    "ွှိဏ်": "weinm",
    "ွှိတ်": "weik",
    "ွှိဒ်": "weik",
    "ွှိန်း": "weinn",
    "ွှိန့်": "weint",
    "ွှိန်": "wein",
    "ွှိပ်": "wake",
    "ွှိဗ်": "wake",
    "ွှိမ်း": "weimm",
    "ွှိမ့်": "weimt",
    "ွှိမ်": "weim",
    "ွှိယ့်": "weik",
    "ွှိယ်": "weik",
    "ွှိရ်": "weik",
    "ွှိလ်": "wein",
    "ွှိဝ်": "weik",
    "ွှိသ်": "weik",
    "ွှိဟ်": "wein",
    "ွိက်": "weik",
    "ွိဂ်": "weik",
    "ွိင်း": "weinn",
    "ွိင့်": "weint",
    "ွိင်": "wein",
    "ွိစ်": "weik",
    "ွိဇ်": "weik",
    "ွိဉ်း": "weinn",
    "ွိဉ့်": "weinnt",
    "ွိဉ်": "weiin",
    "ွိည်း": "weinn",
    "ွိည့်": "weint",
    "ွိည်": "wein",
    "ွိဋ်": "weik",
    "ွိဍ်": "weik",
    "ွိဏ်း": "weinmm",
    "ွိဏ့်": "weinmt",
    "ွိဏ်": "weinm",
    "ွိတ်": "weik",
    "ွိဒ်": "weik",
    "ွိန်း": "weinn",
    "ွိန့်": "weint",
    "ွိန်": "wein",
    "ွိပ်": "wake",
    "ွိဗ်": "wake",
    "ွိမ်း": "weimm",
    "ွိမ့်": "weimt",
    "ွိမ်": "weim",
    "ွိယ့်": "weik",
    "ွိယ်": "weik",
    "ွိရ်": "weik",
    "ွိလ်": "wein",
    "ွိဝ်": "weik",
    "ွိသ်": "weik",
    "ွိဟ်": "wein",
    "ွှက်": "wet",
    "ွှဂ်": "wet",
    "ွှင်း": "winn",
    "ွှင့်": "wint",
    "ွှင်": "win",
    "ွှစ်": "wit",
    "ွှဇ်": "wit",
    "ွှဉ်း": "winn",
    "ွှဉ့်": "winnt",
    "ွှဉ်": "wiin",
    "ွှည်း": "wee",
    "ွှည့်": "wei",
    "ွှည်": "wi",
    "ွှဋ်": "ut",
    "ွှဍ်": "ut",
    "ွှဏ်း": "unmm",
    "ွှဏ့်": "unmt",
    "ွှဏ်": "unm",
    "ွှတ်": "ut",
    "ွှဒ်": "ut",
    "ွှန်း": "unn",
    "ွှန့်": "unt",
    "ွှန်": "un",
    "ွှပ်": "up",
    "ွှဗ်": "up",
    "ွှမ်း": "wamm",
    "ွှမ့်": "wamt",
    "ွှမ်": "wam",
    "ွှယ့်": "wellt",
    "ွှယ်": "wel",
    "ွှရ်": "wel",
    "ွှလ်": "wan",
    "ွှဝ်": "wap",
    "ွှသ်": "wat",
    "ွှဟ်": "wan",
    "ွက်": "wet",
    "ွဂ်": "wet",
    "ွင်း": "winn",
    "ွင့်": "wint",
    "ွင်": "win",
    "ွစ်": "wit",
    "ွဇ်": "wit",
    "ွဉ်း": "winn",
    "ွဉ့်": "winnt",
    "ွဉ်": "wiin",
    "ွည်း": "wee",
    "ွည့်": "wei",
    "ွည်": "wi",
    "ွဋ်": "utt",
    "ွဍ်": "ut",
    "ွဏ်း": "unmm",
    "ွဏ့်": "unmt",
    "ွဏ်": "unm",
    "ွတ်": "ut",
    "ွဒ်": "ut",
    "ွန်း": "unn",
    "ွန့်": "unt",
    "ွန်": "un",
    "ွပ်": "oup",
    "ွဗ်": "oup",
    "ွမ်း": "umm",
    "ွမ့်": "umt",
    "ွမ်": "um",
    "ွယ့်": "wellt",
    "ွယ်": "wel",
    "ွရ်": "wel",
    "ွလ်": "wan",
    "ွဝ်": "wap",
    "ွသ်": "wat",
    "ွဟ်": "wan",
}

vowelExtendedForm = {
    "ှဲ": "el",  # အ
    "ို့": "oh",  # အို့
    "ှို့": "oh",  # အှို့
    "ိုး": "oe",
    "ှိုး": "oe", #
    "\u1031\u102c\u103a": "aw",  # ကော်
    "\u103e\u1031\u102c\u103a": "aw",  # ကှော်
    "\u1031\u102b\u103a": "aw",  # ခေါ်
    "\u103e\u1031\u102b\u103a": "aw",  # ခှေါ်
    "\u1031\u102c\u1037": "awt",  # ကော့
    "\u103e\u1031\u102c\u1037": "awt",  # ကှော့
    "\u1031\u102b\u1037": "awt",  # ခေါ့
    "\u103e\u1031\u102b\u1037": "awt",  # ခှေါ့
    "ာ့": "a",
    "ှာ့": "a",
    "ါ့": "a",
    "ှါ့": "a",
    "ဲ့": "elt",
    "ှဲ့": "elt",
    "ှာ": "ar",
    "ှါ": "ar",
    "ား": "arr",
    "ှား": "arr",
    "ါး": "arr",
    "ှါး": "arr",
    "ံ့": "amt",
    "ှံ": "am",
    "ှံ့": "amt",
    "ုံး": "ome",
    "ှုံး": "ome",
    "ုံ့": "omt",
    "ှုံ့": "omt",
    "ုံ": "oum",
    "ှုံ": "oum",
    "ှု": "u",
    "ှူ": "uu",
    "\u103e\u1031": "ay", # အှေ
    "\u1031\u1037": "ae", # အေ့
    "\u103e\u1031\u1037": "ae", # အှေ့
    "\u1031\u1038": "aye", # အေး
    "\u103e\u1031\u1038": "aye", # အှေး
    "\u1031\u102c": "aww", # မော
    "\u103e\u1031\u102c": "aww", # မှော
    "\u1031\u102b": "aww", # ခေါ
    "\u103e\u1031\u102b": "aww", # ခှေါ
    "ီး": "ee",
    "ှီး": "ee",
    "ှီ": "e",
    "ှိ": "ei",
    "ူး": "oo",
    "ှူး": "ue",
    "\u102d\u102f": "o", # အို
    "\u103e\u102d\u102f": "o",

}

clusterForm = {"ျ": "y", "ြ": "y", "ွ": "w"}
modifyForm = {"ခ": "ch", "ရ": "sh", "သ": "sh"}
def transcript(text):
    output = []
    i = 0
    n = len(text)
    DEBUG = False

    # Assuming these dictionaries are already defined:
    # singleton, clusterForm, asatExtendedForm, vowelForm, modifyForm, vowelExtendedForm, specialCharsForm

    while i < n:
        char = text[i]
        next_char = text[i + 1] if i + 1 < n else ""
        after_next = text[i + 2] if i + 2 < n else ""
        third_next = text[i + 3] if i + 3 < n else ""

        all_but_s = text[i+1:] if i + 1 < n else ""
        all_but_sc = text[i+2:] if i + 2 < n else ""
        all_but_scc = text[i+3:] if i + 3 < n else ""

        # Rule 4.2: Singleton + Cluster + Cluster + AsatExtendedForm
        if (
            char in singleton
            and next_char in clusterForm
            and after_next in clusterForm
            and all_but_scc in asatExtendedForm
        ):
            if third_next == 'ှ':
                if (next_char in ['ျ', 'ြ'] or any(c in next_char for c in ['ျ', 'ြ'])) and char in modifyForm:
                    if 'ွ' in after_next:
                        output.append(
                            vowelForm.get(third_next, "") +
                            modifyForm[char] +
                            asatExtendedForm[all_but_sc]
                        )
                    else:
                        output.append(
                            vowelForm.get(third_next, "") +
                            modifyForm[char] +
                            clusterForm[after_next] +
                            asatExtendedForm[all_but_scc]
                        )
                else:
                    if 'ွ' in after_next:
                        output.append(
                            vowelForm.get(third_next, "") +
                            singleton[char] +
                            clusterForm[next_char] +
                            asatExtendedForm[all_but_sc]
                        )
                    else:
                        output.append(
                            vowelForm.get(third_next, "") +
                            singleton[char] +
                            clusterForm[next_char] +
                            clusterForm[after_next] +
                            asatExtendedForm[all_but_scc]
                        )
            else:
                if (next_char in ['ျ', 'ြ'] or any(c in next_char for c in ['ျ', 'ြ'])) and char in modifyForm:
                    if 'ွ' in after_next:
                        output.append(
                            modifyForm[char] + asatExtendedForm[all_but_sc]
                        )
                    else:
                        output.append(
                            singleton[char] +
                            clusterForm[next_char] +
                            clusterForm[after_next] +
                            asatExtendedForm[all_but_scc]
                        )
                else:
                    if 'ွ' in after_next:
                        output.append(
                            singleton[char] +
                            clusterForm[next_char] +
                            asatExtendedForm[all_but_sc]
                        )
                    else:
                        output.append(
                            singleton[char] +
                            clusterForm[next_char] +
                            clusterForm[after_next] +
                            asatExtendedForm[all_but_scc]
                        )
            i += 3 + len(all_but_scc)
        
        # Rule 4.1: Singleton + Cluster + AsatExtendedForm
        elif (
            char in singleton
            and next_char in clusterForm
            and all_but_sc in asatExtendedForm
        ):
            if after_next == 'ှ':
                if 'ွ' in next_char:
                    if 'ရ' in char:
                        output.append(f"sh{asatExtendedForm[all_but_s]}")
                    else:
                        output.append(
                            vowelForm.get(after_next, "") +
                            singleton[char] +
                            asatExtendedForm[all_but_s]
                        )
                elif (next_char in ['ျ', 'ြ'] or any(c in next_char for c in ['ျ', 'ြ'])) and char in modifyForm:
                    output.append(
                        f"{vowelForm.get(after_next, '')}{modifyForm[char]}{asatExtendedForm[all_but_sc]}"
                    )
                else:
                    output.append(
                        vowelForm.get(after_next, "") +
                        singleton[char] +
                        clusterForm[next_char] +
                        asatExtendedForm[all_but_sc]
                    )
                i += 3 + len(all_but_sc)
            else:
                if 'ွ' in next_char:
                    output.append(singleton[char] + asatExtendedForm[all_but_s])
                elif (next_char in ['ျ', 'ြ'] or any(c in next_char for c in ['ျ', 'ြ'])) and char in modifyForm:
                    output.append(f"{modifyForm[char]}{asatExtendedForm[all_but_sc]}")
                else:
                    output.append(
                        singleton[char] +
                        clusterForm[next_char] +
                        asatExtendedForm[all_but_sc]
                    )
                i += 2 + len(all_but_sc)

        # Rule 4.0: Singleton + AsatExtendedForm
        elif char in singleton and all_but_s in asatExtendedForm:
            if next_char == 'ှ':
                if 'ရ' in char:
                    output.append(f"sh{asatExtendedForm[all_but_s]}")
                else:
                    output.append(
                        vowelForm.get(next_char, "") +
                        singleton[char] +
                        asatExtendedForm[all_but_s]
                    )
                i += 2 + len(all_but_s)
            else:
                output.append(f"{singleton[char]}{asatExtendedForm[all_but_s]}")
                i += 1 + len(all_but_s)

        # Rule 3.1: Singleton + Cluster + Cluster + Vowel Extended
        elif (
            char in singleton
            and next_char in clusterForm
            and after_next in clusterForm
            and all_but_scc in vowelExtendedForm
        ):
            if third_next == 'ှ':
                if (next_char in ['ျ', 'ြ'] or any(c in next_char for c in ['ျ', 'ြ'])) and char in modifyForm:
                    output.append(
                        f"{vowelForm.get(third_next, '')}{modifyForm[char]}{clusterForm[after_next]}{vowelExtendedForm[all_but_scc]}"
                    )
                else:
                    output.append(
                        f"{vowelForm.get(third_next, '')}{singleton[char]}{clusterForm[next_char]}{clusterForm[after_next]}{vowelExtendedForm[all_but_scc]}"
                    )
                i += 3 + len(all_but_scc)
            else:
                if (next_char in ['ျ', 'ြ'] or any(c in next_char for c in ['ျ', 'ြ'])) and char in modifyForm:
                    output.append(modifyForm[char] + clusterForm[after_next] + vowelExtendedForm[all_but_scc])
                else:
                    output.append(
                        singleton[char] +
                        clusterForm[next_char] +
                        clusterForm[after_next] +
                        vowelExtendedForm[all_but_scc]
                    )
                i += 3 + len(all_but_scc)

        # Rule 3.0: Singleton + Cluster + Cluster + Vowel
        elif (
            char in singleton
            and next_char in clusterForm
            and after_next in clusterForm
        ):
            if third_next in vowelForm:
                if third_next == 'ှ':
                    if (next_char in ['ျ', 'ြ'] or any(c in next_char for c in ['ျ', 'ြ'])) and char in modifyForm:
                        output.append(
                            f"{vowelForm.get(third_next, '')}{modifyForm[char]}{clusterForm[after_next]}a"
                        )
                    else:
                        output.append(
                            f"{vowelForm.get(third_next, '')}{singleton[char]}{clusterForm[next_char]}{clusterForm[after_next]}a"
                        )
                else:
                    if (next_char in ['ျ', 'ြ'] or any(c in next_char for c in ['ျ', 'ြ'])) and char in modifyForm:
                        output.append(modifyForm[char] + clusterForm[after_next] + vowelForm[third_next])
                    else:
                        output.append(
                            singleton[char] +
                            clusterForm[next_char] +
                            clusterForm[after_next] +
                            vowelForm[third_next]
                        )
                i += 4
            else:
                if (next_char in ['ျ', 'ြ'] or any(c in next_char for c in ['ျ', 'ြ'])) and char in modifyForm:
                    output.append(f"{modifyForm[char]}{clusterForm[after_next]}a")
                else:
                    output.append(f"{singleton[char]}{clusterForm[next_char]}{clusterForm[after_next]}a")
                i += 3

        # Rule 2.1: Singleton + Cluster + Vowel Extended
        elif (
            char in singleton
            and next_char in clusterForm
            and all_but_sc in vowelExtendedForm
        ):
            if after_next == 'ှ':
                if (next_char in ['ျ', 'ြ'] or any(c in next_char for c in ['ျ', 'ြ'])) and char in modifyForm:
                    output.append(vowelForm.get(after_next, "") + modifyForm[char] + vowelExtendedForm[all_but_sc])
                else:
                    if 'ရ' in char:
                        output.append(f"sh{clusterForm[next_char]}{vowelExtendedForm[all_but_sc]}")
                    else:
                        output.append(
                            vowelForm.get(after_next, "") +
                            singleton[char] +
                            clusterForm[next_char] +
                            vowelExtendedForm[all_but_sc]
                        )
                i += 2 + len(all_but_sc)
            else:
                if (next_char in ['ျ', 'ြ'] or any(c in next_char for c in ['ျ', 'ြ'])) and char in modifyForm:
                    output.append(modifyForm[char] + vowelExtendedForm[all_but_sc])
                else:
                    output.append(singleton[char] + clusterForm[next_char] + vowelExtendedForm[all_but_sc])
                i += 2 + len(all_but_sc)

        # Rule 2.0: Singleton + Cluster + Vowel
        elif char in singleton and next_char in clusterForm:
            if after_next in vowelForm:
                if after_next == 'ှ':
                    if (next_char in ['ျ', 'ြ'] or any(c in next_char for c in ['ျ', 'ြ'])) and char in modifyForm:
                        output.append(f"{vowelForm.get(after_next, '')}{modifyForm[char]}a")
                    else:
                        if 'ရ' in char:
                            output.append(f"sh{clusterForm[next_char]}a")
                        else:
                            output.append(f"{vowelForm.get(after_next, '')}{singleton[char]}{clusterForm[next_char]}a")
                else:
                    if (next_char in ['ျ', 'ြ'] or any(c in next_char for c in ['ျ', 'ြ'])) and char in modifyForm:
                        output.append(modifyForm[char] + vowelForm[after_next])
                    else:
                        output.append(singleton[char] + clusterForm[next_char] + vowelForm[after_next])
                i += 3
            else:
                if (next_char in ['ျ', 'ြ'] or any(c in next_char for c in ['ျ', 'ြ'])) and char in modifyForm:
                    output.append(f"{modifyForm[char]}a")
                else:
                    output.append(f"{singleton[char]}{clusterForm[next_char]}a")
                i += 2

        # Rule 1.1: Singleton + Vowel Extended Forms
        elif char in singleton and all_but_s in vowelExtendedForm:
            if next_char == 'ှ':
                if 'ရ' in char:
                    output.append(f"sh{vowelExtendedForm[all_but_s]}")
                else:
                    output.append(vowelForm.get(next_char, "") + singleton[char] + vowelExtendedForm[all_but_s])
            else:
                output.append(singleton[char] + vowelExtendedForm[all_but_s])
            i += 1 + len(all_but_s)

        # Rule 1.0: Singleton + Vowel (base)
        elif char in singleton:
            if next_char in vowelForm:
                if next_char == 'ှ':
                    if 'ရ' in char:
                        output.append("sha")
                    else:
                        output.append(f"{vowelForm[next_char]}{singleton[char]}a")
                else:
                    output.append(singleton[char] + vowelForm[next_char])
                i += 2
            else:
                if 'အ' in char:
                    output.append("ah")
                elif 'ဧ' in char:
                    output.append(f"{singleton[char]}")
                else:
                    output.append(f"{singleton[char]}a")
                i += 1

        # Rule 0.1: Special Character Form
        elif char in specialCharsForm:
            output.append(specialCharsForm[char])
            i += 1

        # Rule 0.0: Default - just append
        else:
            output.append(char)
            i += 1

    return ''.join(output)