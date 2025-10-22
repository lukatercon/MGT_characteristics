from openai import OpenAI

import os


def combine_with_template(title_info, length):
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
            subtitle_string = f" z naslovom {title_info[1]}"

    template = f"Napiši esej{title_string}{subtitle_string}{ref_lit_work_string} s približno {str(length)} besedami. Odgovori samo z esejem brez spremnega besedila."

    return template


client = OpenAI()
# define the model to be used
model_to_use = ""

# define the files that contain lengths and titles
lengths_file = os.path.join("..", "Datasets", "Solar", "Solar_lengths.tsv")
titles_file = os.path.join("..", "Datasets", "Solar", "Annotated_titles.tsv")

# define the output dir
output_dir = os.path.join("..", "Datasets", "Solar", "Solar_GPT-5", "raw")


# build metadata dictionary
with open(lengths_file, "r", encoding="utf-8") as rf_len:
    raw_len = rf_len.read()
len_dict = dict()

for line in raw_len.splitlines()[1:]:
    doc_id, length = line.strip().split("\t")
    len_dict[doc_id] = int(length)

# build titles dictionary
with open(titles_file, "r", encoding="utf-8") as rf_titles:
    titles_dict = dict()
    for line in rf_titles:
        if not line.startswith("DOC_ID\t"):
            doc_id, title, ref_work, subtitle = line.strip().split("\t")
            title = title if title != "N/A" else None
            ref_work = ref_work if ref_work != "N/A" else None
            subtitle = subtitle if subtitle != "N/A" else None
            titles_dict[doc_id] = (title, subtitle, ref_work)

# go through every document in Šolar and generate a machine generated essay
i = 0
for doc_id in titles_dict.keys():
    prompt = combine_with_template(titles_dict[doc_id], len_dict[doc_id])

    completion = client.chat.completions.create(
        model=model_to_use,
        temperature=1,
        top_p=1,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},  # use a default system prompt in English
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

