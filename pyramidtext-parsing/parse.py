"""
Purpose of this file is to try and extract aligned sentences and sentence fragments
from this PDF (https://library.oapen.org/bitstream/id/467ce946-d62f-431b-bd85-9c8f039d4598/421591.pdf)
to expand corpora necessary for MT.
"""
from pdfminer.high_level import extract_pages, extract_text
from pdfminer.layout import LAParams, LTLine
import re
import pandas as pd
from tqdm import trange, tqdm
# ================ HELPERS ======================
def get_column(objs, col_no, page_no, page_width):
    if col_no == 1:
        ans = sorted([item for item in objs if ((item.bbox[0] + item.bbox[2]) / 2) < (page_width / 2) and item.bbox[1] < 753], key=lambda x: -x.bbox[1])
    elif col_no == 2:
        ans = sorted([item for item in objs if ((item.bbox[0] + item.bbox[2]) / 2) >= (page_width / 2) and item.bbox[1] < 753], key=lambda x: -x.bbox[1])
    else:
        ans = []

    if page_no == 357:
        return [item for item in ans if item.bbox[1] < 428]
    return ans

def get_columned_page(element, page, keyset):
    page_width = element.width
    col_1 = get_column(element._objs, 1, page, page_width)
    col_2 = get_column(element._objs, 2, page, page_width)
    elements = col_1
    elements.extend(col_2)

    current, split_up = [], []
    for element in elements:
        if type(element) == LTLine:
            if len(current):
                split_up.append(current)
                current = []
        else:
            for item in element:
                txt = item.get_text().strip('\n')
                current.append(txt)
                if ':' in txt:
                    keyset.add(txt[:txt.index(':')])
    if len(current):
        split_up.append(current)
    return split_up

def remove_header_footer(objs):
    vertically_sorted = sorted(objs, key=lambda x: -((x.bbox[1] + x.bbox[3]) / 2))
    no_header = [item for item in vertically_sorted if item.bbox[1] < 753]
    
    footer_line = None
    for i in range(len(no_header)):
        if type(no_header[i]) == LTLine:
            footer_line = i
            break
    no_footer = no_header[:i]
    not_header = [item for item in no_footer if item._objs[0]._objs[0].size < 11 and item._objs[0]._objs[0].fontname != 'ZADVIK+BaskervilleMT-Italic' and 'motif' not in item.get_text()]
    
    lines = []
    for item in not_header:
        for obj in item._objs:
            if obj.get_text().split()[0] in CH_PREFIXES:
                lines.append(obj.get_text())
            else:
                lines[-1] += " " + obj.get_text()
    return lines

def standardize_unicode(df):
    #df = df.Transliteration.str.replace('z', 's')
    df = df.replace('\uf084','H', regex=True)
    df = df.replace('\uf0a3','X', regex=True)
    df = df.replace('\uf0a2','x', regex=True)
    df = df.replace('\uf02b','S', regex=True)
    df = df.replace('\uf0b3','T', regex=True)
    df = df.replace('\uf09d','D', regex=True)
    df = df.replace('\r\n', ' ')
    df = df.replace('\n', ' ')
    df = df.replace(r'\s{2,}', ' ', regex=True)
    df = df.replace(r'\(i\s\)', '(i)', regex=True)
    df = df.replace(r'\*', '', regex=True)
    df = df.replace('â€™', "'", regex=True)
    return df

# ================ SCRIPT =======================
CH_PREFIXES = ['aPT', 'BD', 'PT', 'fPT', 'hPT', 'sPT', 'CT', 'aCT', 'N']

def get_chapter1(path):
    START_PAGE = 357
    END_PAGE = 494

    full_list = []
    keyset = set()
    layout = extract_pages(path, page_numbers=list(range(START_PAGE, END_PAGE+1)), laparams=LAParams(line_margin=0.2, boxes_flow=1))
    page = START_PAGE
    for element in layout:   
        split_up = get_columned_page(element, page, keyset)

        # Fix partial entries
        right_prefix = False
        for prefix in CH_PREFIXES:
            if split_up[0][0].startswith(prefix):
                right_prefix = True
        
        if right_prefix:
            full_list.extend(split_up)
        else:
            full_list[-1].extend(split_up[0])
            full_list.extend(split_up[1:])

        print('Page {} processing complete!'.format(page))
        page += 1
    print("Done with all page processing!")

    aligned = []
    for utterance in tqdm(full_list):
        joined = ' '.join(utterance)
        translit_regex = r"\):\s?(.+?)\s?“"
        translate_regex = r'“\s?(.+?)\s?”'
        translit_matches = re.findall(translit_regex, joined, re.UNICODE | re.DOTALL)
        translate_matches = re.findall(translate_regex, joined, re.UNICODE | re.DOTALL)
        if len(translit_matches) == len(translate_matches):
            for i in range(len(translit_matches)):
                aligned.append((translit_matches[i], translate_matches[i]))
        else:
            print('investigate failure')
            
    df = pd.DataFrame(aligned, columns=['Transliteration','Translation'])
    df = standardize_unicode(df)

    print(df.shape)
    return df

def get_chapter2(path):
    START_PAGE = 530
    END_PAGE = 679

    full_list = []
    layout = extract_pages(path, page_numbers=list(range(START_PAGE, END_PAGE + 1)), laparams=LAParams(line_margin=0.2))
    
    for element in tqdm(layout):
        elements = remove_header_footer(element._objs)
        full_list.extend(elements)

    aligned = []
    for utterance in tqdm(full_list):
        if ':' not in utterance:
            pass
        else:
            translit_regex = r":\s?(.+?)\s?“"
            translate_regex = r'“\s?(.+?)\s?[”|$]'
            translit_matches = re.findall(translit_regex, utterance, re.UNICODE | re.DOTALL)
            translate_matches = re.findall(translate_regex, utterance, re.UNICODE | re.DOTALL)
            if len(translit_matches) == len(translate_matches):
                for i in range(len(translit_matches)):
                    aligned.append((translit_matches[i], translate_matches[i]))
            else:
                aug = utterance.replace("“O Osiris NN”", "")
                translit_regex = r":\s?(.+?)\s?“"
                translate_regex = r'“\s?(.+?)\s?[”|$|\n]'
                translit_matches = re.findall(translit_regex, aug, re.UNICODE | re.DOTALL)
                translate_matches = re.findall(translate_regex, aug, re.UNICODE | re.DOTALL)
                if len(translit_matches) == len(translate_matches):
                    for i in range(len(translit_matches)):
                        aligned.append((translit_matches[i], translate_matches[i]))
                else:
                    print('investigate failure')

    df = pd.DataFrame(aligned, columns=['Transliteration','Translation'])
    df = standardize_unicode(df)

    print(df.shape)
    return df

def run_save_all():
    path = 'PT.pdf'

    ch1 = get_chapter1(path)
    ch1.to_csv('chapter1.csv')

    ch2 = get_chapter2(path)
    ch2.to_csv('chapter2.csv')
    
    df = pd.concat([ch1,ch2])
    df.to_csv('combined.csv')

run_save_all()