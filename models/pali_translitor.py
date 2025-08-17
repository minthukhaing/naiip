import re
singleton ={ "က": "k",
    "ခ": "kh",
    "ဂ": "g",
    "ဃ": "gh",
    "င": "\u1e45",
    "စ": "c",
    "ဆ": "ch",
    "ဇ": "j",
    "ဈ": "jh",
    "ဉ": "\u00f1",
    "ဋ": "\u1e6d",
    "ဌ": "\u1e6dh",
    "ဍ": "\u1e0d",
    "ဎ": "\u1e0dh",
    "ဏ": "\u1e47",
    "တ": "t",
    "ထ": "th",
    "ဒ": "d",
    "ဓ": "dh",
    "န": "n",
    "ပ": "p",
    "ဖ": "ph",
    "ဗ": "b",
    "ဘ": "bh",
    "မ": "m",
    "ယ": "y",
    "ရ": "r",
    "လ": "l",
    "ဝ": "v",
    "သ": "s",
    "ဟ": "h",
    "ဠ": "\u1e37",
    "အ": "",

}
vowelForm = {
    "ာ": "ā",
    "ါ": "ā",
    "ိ": "i",
    "ီ": "ī",
    "ု": "u",
    "ူ": "ū",
    "ေ": "e",
    "ံ": "aṁ",
    "ှ": "h"
  }
specialCharsForm = {
    "အ": "a",
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
    "။": ".",
  }
asatForm = {"်": "a"}
extendedForm = {
    "ာ့": "a",
    "ါ့": "a",
    "ား": "āā",
    "ါး": "āā",
    "ံ့": "ṃ",
    "ုံ": "uṃ", # ုံ
    "ော": "o",
    "ေါ": "o",
    "ီး": "īī",
    "ု": "u",
    "ူ": "ū",
    "ူး": "u",
    "ိုး": "oee",
    "ို": "oe",
    "ှာ": "ā",
    "ှါ": "ā"
}
clusterForm = {"ျ": "y", "ြ": "r", "ွ": "v"}
#------------------------------------------------------
def transliterate(text):
    output = []
    i = 0

    while i < len(text):
        char = text[i]
        next_char = text[i + 1] if i + 1 < len(text) else ""
        after_next = text[i + 2] if i + 2 < len(text) else ""
        third_next = text[i + 3] if i + 3 < len(text) else ""
        the_rest = text[1:]

        # Rule 5.1: Singleton + Singleton + Asat (Fix Order)
        if (char in singleton and 
            next_char in singleton and 
            after_next in asatForm):
            output.append(f"{singleton[char]}a{singleton[next_char]}")
            i += 2
            # print('rule 5.1: Singleton + Singleton + Asat (Fix Order)')

        # Rule 5.0: Singleton + Cluster + Singleton + Asat
        elif (char in singleton and 
              next_char in clusterForm and 
              after_next in singleton and 
              text[i + 3] in asatForm):
            output.append(f"{singleton[char]}{clusterForm[next_char]}a{singleton[after_next]}")
            i += 3
            # print('rule 5.0: Singleton + Cluster + Singleton + Asat')

        # Rule 4.2: Singleton + Extended + Singleton + Asat (Remove Asat in Output)
        elif (char in singleton and 
              next_char in vowelForm and 
              third_next in singleton and 
              text[i + 4] in asatForm):
            extended_two = text[1:3]
            # print(f'ExtendedTwo: {extended_two}')
            output.append(singleton[char] + extendedForm[extended_two] + singleton[third_next])
            i += 4  # Skip asat
            # print('rule 4.2: Singleton + Extended + Singleton + Asat')

        # Rule 4.1: Singleton + Vowel + Singleton + Asat (Remove Asat in Output)
        elif (char in singleton and 
              next_char in vowelForm and 
              after_next in singleton and 
              text[i + 3] in asatForm):
            output.append(singleton[char] + vowelForm[next_char] + singleton[after_next])
            i += 3  # Skip asat
            # print('rule 4.1: Asat Singleton + Vowel + Singleton + Asat')

        # Rule 4.0: Asat Form
        elif char in asatForm:
            if output:
                output[-1] += asatForm[char]
            # print('rule 4.0: Asat Form')

        # Rule 3.0: Singleton + Extended Forms
        elif (char in singleton and 
              the_rest in extendedForm):
            output.append(singleton[char] + extendedForm[the_rest])
            i += 3
            # print('rule 3.0: Singleton + Extended Forms')

        # Rule 2.1: Singleton + Cluster + Vowel
        elif (char in singleton and 
              next_char in clusterForm and 
              after_next in vowelForm):
            output.append(singleton[char] + clusterForm[next_char] + vowelForm[after_next])
            i += 2
            # print('rule 2.1: Singleton + Cluster + Vowel')

        # Rule 2.0: Singleton + Cluster
        elif (char in singleton and 
              next_char in clusterForm):
            output.append(singleton[char] + clusterForm[next_char])
            i += 1
            # print('rule 2.0: Singleton + Cluster')

        # Rule 1.1: Singleton အ / ဧ + Vowel
        elif (char in singleton and 
              char in specialCharsForm):
            if next_char in vowelForm:
                if next_char == 'ှ':
                    output.append(f"{singleton[char]}{vowelForm[next_char]}a")
                else:
                    output.append(vowelForm[next_char])
                i += 1
            else:
                output.append(specialCharsForm[char])
            # print('rule 1.1: Singleton အ / ဧ + Vowel')

        # Rule 1.0: Singleton + Vowel (base)
        elif char in singleton:
            if next_char in vowelForm:
                if next_char == 'ှ':
                    output.append(f"{singleton[char]}{vowelForm[next_char]}a")
                else:
                    output.append(singleton[char] + vowelForm[next_char])
                i += 1
            else:
                output.append(f"{singleton[char]}a")
            # print('rule 1.0: Singleton + Vowel (base)')

        # Rule 0.1: Special Character Form
        elif char in specialCharsForm:
            output.append(specialCharsForm[char])
            # print('rule 0.1: Special Character Form')

        # Rule 0.0: Default - just append
        else:
            output.append(char)
            # print('rule 0.0: Default')

        i += 1

    return "".join(output)

