import os
from openai import OpenAI

from utils import combine_with_Šolar_template, build_lengths_dict, build_titles_dict

if __name__ == "__main__":
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

    #NOTE: this code was written and used before we set firm criteria for what counts as a relevant text from Šolar.
    # That is why the other script only looks at the relevant ids.
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
