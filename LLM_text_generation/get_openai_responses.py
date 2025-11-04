import os
from openai import OpenAI


def combine_with_Šolar_template(title_info, length):
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

# define the client and the model to be used
client = OpenAI()
model_to_use = "gpt-5-2025-08-07"     # this is the model used by default in the ChatGPT browser interface at time of generation "gpt-5-2025-08-07"

# define the files that contain lengths and titles
lengths_file = os.path.join("..", "Datasets", "Solar", "Solar_lengths.tsv")
titles_file = os.path.join("..", "Datasets", "Solar", "Solar_annotated_titles.tsv")

# define the output dir
output_dir = os.path.join("..", "Datasets", "Solar", "Solar_GPT-5", "raw")


# build text lengths dictionary and titles dictionary
len_dict = build_lengths_dict(lengths_file)
titles_dict = build_titles_dict(titles_file)

# go through every document in human-written and generate a corresponding machine generated essay, 
# but only if at least the title or the referenced literary work of the essay is known
i = 1
for doc_id in titles_dict.keys():
    title_info = titles_dict[doc_id]

    if title_info[0] or title_info[2]:

        prompt = combine_with_Šolar_template(title_info, len_dict[doc_id])

        completion = client.chat.completions.create(
            model=model_to_use,
            temperature=1,
            top_p=1,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},  # use a default system prompt in English, since this reflects the default usage of most users
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        with open(os.path.join(output_dir, f"{doc_id}.txt"), "w", encoding="utf-8") as wf:
            wf.write(completion.choices[0].message.content)

        if i % 100 == 0:
            print(f"Document {i}/{len(titles_dict.keys())}")

        i += 1
