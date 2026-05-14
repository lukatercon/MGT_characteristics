from trankit import Pipeline, trankit2conllu
from tqdm import tqdm

import os
import sys


def process_long_text(pipeline, text, max_tokens=400):
    """
    Split text into sentences, batch them into chunks under max_tokens,
    and process each chunk separately.
    Uses conservative max_tokens to leave room for special tokens.
    """
    # First, use trankit just for sentence splitting
    sentences = pipeline.ssplit(text)['sentences']
    
    chunks = []
    current_chunk_sents = []
    current_len = 0

    for sent in sentences:
        sent_len = len(sent['tokens'])
        
        # If a single sentence is already too long, split it by words
        if sent_len > max_tokens:
            words = sent['text'].split()
            for i in range(0, len(words), max_tokens):
                chunks.append(' '.join(words[i:i+max_tokens]))
            continue
        
        # If adding this sentence exceeds the limit, flush and start new chunk
        if current_len + sent_len > max_tokens:
            chunks.append(' '.join(s['text'] for s in current_chunk_sents))
            current_chunk_sents = []
            current_len = 0
        
        current_chunk_sents.append(sent)
        current_len += sent_len

    # Don't forget the last chunk
    if current_chunk_sents:
        chunks.append(' '.join(s['text'] for s in current_chunk_sents))

    # Now annotate each chunk
    results = []
    for chunk in chunks:
        results.append(pipeline(chunk))
    
    return results


model_path = os.path.join("..", "Models", "save_dir_ssj_sst")

# parse positional arguments. Usage: 
# python annotate_w_trankit.py raw_files_directory output_path language read_mode processing_mode

# language can be any of the languages supported by trankit

# read_mode can be either entire_dir (to annotate all the files in the directory) or 
# relevant (currently only for sl and en - only get the docs that re on a list of relevant docs)

# processing_mode can be default, where the whole file is passed into the pipeline 
# or long_text, where the text of each file is first split up depending on a max_token value 
raw_files_path, output_path, lang, read_mode, proc_mode = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
assert read_mode in ["relevant", "entire_dir"]
assert proc_mode in ["default", "long_text"]


lang = lang.lower()
if read_mode == "relevant":
    assert lang in ["slovenian", "english"]

    if lang == "slovenian":
        relevant_ids_file = os.path.join("..", "Datasets", "Solar", "Solar_relevant_doc_ids.txt")
    elif lang == "english":
        relevant_ids_file = os.path.join("..", "Datasets", "LOCNESS", "LOCNESS_relevant_doc_ids.txt")

# build list of relevant doc ids
if read_mode == "relevant":
    relevant_ids = list()
    with open(relevant_ids_file, "r", encoding="utf-8") as rf_ids:
        for line in rf_ids:
            relevant_ids.append(line.strip())
elif read_mode == "entire_dir":
    relevant_ids = os.listdir(raw_files_path)

# load the Trankit models
if lang == "slovenian":
    p = Pipeline(lang="customized", cache_dir=model_path, embedding='xlm-roberta-large', gpu=False)
else:
    p = Pipeline(lang=lang, gpu=False)

print("Done loading Trankit models!")

# open output file
with open(output_path, "w", encoding="utf-8") as wf:
    for doc_id in tqdm(iter(relevant_ids), total=len(relevant_ids), desc="Progress through docs"):
        file = doc_id + ".txt" if not doc_id.endswith(".txt") else doc_id

        with open(os.path.join(raw_files_path, file), "r", encoding="utf-8") as rf:
            file_text = rf.read()
        
        # annotate
        if proc_mode == "default":
            conllu_output = trankit2conllu(p(file_text))
        elif proc_mode == "long_text":
            chunk_results = process_long_text(p, file_text)
            conllu_output = "".join(trankit2conllu(result) for result in chunk_results)

        conllu_sents = conllu_output.split("\n\n")
        no_of_sents = len(conllu_sents)

        # prepare the final conllu and handle the ids
        final_conllu_text = ""
        for k in range(no_of_sents):  # k represents the sentence index
            if "\t" in conllu_sents[k]:
                final_conllu_text += f"# sent_id = {doc_id}.{str(k + 1)}\n{conllu_sents[k]}\n\n"
        
        # write to output file
        wf.write(final_conllu_text)
