def combine_with_Šolar_default_template(title_info, length):
    title_string = ""
    subtitle_string = ""
    ref_lit_work_string = ""
    
    # account for cases in which some of the information about the title is missing
    if title_info[0]:
        title_string = f" z naslovom {title_info[0]}"
    
    if title_info[2]:
        ref_lit_work_string = f", ki se nanaša na literarno delo {title_info[2]},"
    
    if title_info[1]:
        if title_info[0]:
            subtitle_string = f" in podnaslovom {title_info[1]}"
        else:
            subtitle_string = f" s podnaslovom {title_info[1]}"

    template = f"Napiši esej{title_string}{subtitle_string}{ref_lit_work_string} s približno {str(length)} besedami. Odgovori samo z esejem brez spremnega besedila."

    return template


def combine_with_Šolar_persona_aware_template(title_info, length, region, subject, age=0, grade=None, mode="default"):
    title_string = ""
    subtitle_string = ""
    ref_lit_work_string = ""
    
    # account for cases in which some of the information about the title is missing
    if title_info[0]:
        title_string = f" z naslovom {title_info[0]}"
    
    if title_info[2]:
        ref_lit_work_string = f", ki se nanaša na literarno delo {title_info[2]},"
    
    if title_info[1]:
        if title_info[0]:
            subtitle_string = f" in podnaslovom {title_info[1]}"
        else:
            subtitle_string = f" s podnaslovom {title_info[1]}"

    if mode == "default":
        template = f"Napiši esej{title_string}{subtitle_string}{ref_lit_work_string} s približno {str(length)} besedami. Esej napiši, kot bi ga napisal dijak 4. letnika gimnazije iz kraja: {region} pri predmetu: {subject}. Odgovori samo z esejem brez spremnega besedila."
    elif mode == "age":
        template = f"Napiši esej{title_string}{subtitle_string}{ref_lit_work_string} s približno {str(length)} besedami. Esej napiši, kot bi ga napisal {str(age)} let star pisec. Odgovori samo z esejem brez spremnega besedila."
    elif mode == "grade" and grade:
        if "letnik" in grade:
            school = "srednje šole"
            template = f"Napiši esej{title_string}{subtitle_string}{ref_lit_work_string} s približno {str(length)} besedami. Esej napiši, kot bi ga napisal pisec, ki hodi v {grade} {school}. Odgovori samo z esejem brez spremnega besedila."
        else:
            school = "osnovne šole"
            template = f"Napiši esej{title_string}{subtitle_string}{ref_lit_work_string} s približno {str(length)} besedami. Esej napiši, kot bi ga napisal pisec, ki hodi v {grade} {school}. Odgovori samo z esejem brez spremnega besedila."
    else:
        raise Exception(f"Invalid prompt mode: {mode}")

    return template


def combine_with_Šolar_linguistically_aware_template(title_info, length, region, subject, mode="general"):
    # mode can be "general" or "specific"
    title_string = ""
    subtitle_string = ""
    ref_lit_work_string = ""
    
    # account for cases in which some of the information about the title is missing
    if title_info[0]:
        title_string = f" z naslovom {title_info[0]}"
    
    if title_info[2]:
        ref_lit_work_string = f", ki se nanaša na literarno delo {title_info[2]},"
    
    if title_info[1]:
        if title_info[0]:
            subtitle_string = f" in podnaslovom {title_info[1]}"
        else:
            subtitle_string = f" s podnaslovom {title_info[1]}"

    if mode == "general":
        template = f"Napiši esej{title_string}{subtitle_string}{ref_lit_work_string} s približno {str(length)} besedami. Esej napiši, kot bi ga napisal dijak 4. letnika gimnazije iz kraja: {region} pri predmetu: {subject}. Bodi pozoren, da bo jezik v eseju čim bolj podoben jeziku, ki bi ga sproduciral omenjeni dijak, pri čemer posebej pazi na primerno dolžino eseja, dolžino povedi, leksikalno raznolikost, raznolikost n-gramov, raznolikost skladenjskih dreves, skladenjsko kompleksnost (povprečno dolžino skladenjskih relacij) in porazdelitev besednovrstnih oznak in tipov skladenjskih relacij. Odgovori samo z esejem brez spremnega besedila."
    elif mode == "specific":
        template = f"Napiši esej{title_string}{subtitle_string}{ref_lit_work_string} s približno {str(length)} besedami. Esej napiši, kot bi ga napisal dijak 4. letnika gimnazije iz kraja: {region} pri predmetu: {subject}. Bodi pozoren, da bo jezik v eseju čim bolj podoben jeziku, ki bi ga sproduciral omenjeni dijak, pri čemer posebej pazi, da bodo dolžine esejev daljše kot običajno, dolžine povedi krajše, leksikalna raznolikost višja, raznolikost n-gramov višja, raznolikost skladenjskih dreves višja in skladenjska kompleksnost (povprečna dolžina skladenjskih relacij) nižja. Med besednovrstnimi oznakami morajo biti bolj pogosti pomožni glagoli, glagoli in zaimki, manj pa mora biti samostalnikov, pridevnikov in predlogov. Med tipi skladenjskih relacij morajo biti bolj pogosti prislovni modifikatorji, pomožni glagoli in predmeti, manj pa mora biti pridevniških modifikatorjev, samostalniških modifikatorjev in prirednih zvez. Odgovori samo z esejem brez spremnega besedila."
    else:
        raise Exception(f"Invalid prompt mode: {mode}")

    return template


def combine_with_locness_default_template(topic, length):
    template = f"Write an essay using approximately {length} words addressing the following topic: {topic}\nProvide only the essay without any additional accompanying text."

    return template


def combine_with_locness_linguistically_aware_template(topic, length):
    template = f"Write an essay using approximately {length} words addressing the following topic: {topic}\nWrite the essay as if it were written by a British A-level student. Make sure that the language used matches the profile of the writer, paying special attention to the length of the essay, the length of sentences, lexical diversity, n-gram diversity, diversity of syntactic trees, syntactic complexity (average length of dependency relations), and the distribution of parts-of-speech and syntactic relation types. Provide only the essay without any additional accompanying text."

    return template

def build_lengths_dict(lengths_file):
    len_dict = dict()
    with open(lengths_file, "r", encoding="utf-8") as rf_len:
        for line in rf_len.readlines()[1:]:
            doc_id, length = line.strip().split("\t")
            len_dict[doc_id] = int(length)

    return len_dict


def build_titles_dict(titles_file):
    titles_dict = dict()
    with open(titles_file, "r", encoding="utf-8") as rf_titles:
        for line in rf_titles.readlines()[1:]:
            doc_id, title, ref_work, subtitle = line.strip().split("\t")
            
            title = title if title != "N/A" else None
            ref_work = ref_work if ref_work != "N/A" else None
            subtitle = subtitle if subtitle != "N/A" else None
            titles_dict[doc_id] = (title, subtitle, ref_work)
    
    return titles_dict


def build_metadata_dict(meta_file, mode):
    meta_dict = dict()
    with open(meta_file, "r", encoding="utf-8") as rf_meta:
        for line in rf_meta.readlines()[1:]:
            if mode == "Šolar":
                _, solar_id, _, date, school_type, subject, grade, text_type, region = line.strip().split("\t")

                solar_id = solar_id[:-1]
                meta_dict[solar_id] = (date, school_type, subject, grade, text_type, region)
            
            elif mode == "LOCNESS":
                _,	locness_id,	topic_from_text, topic_proposed, essay_length = line.strip().split("\t")
                final_topic = topic_from_text if topic_from_text != "_" else topic_proposed

                meta_dict[locness_id] = (final_topic, int(essay_length)) 

    return meta_dict
