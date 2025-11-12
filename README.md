# MGT_characteristics
Repository for the code used for data generation and data preparation in the "Comparison of Syntactic Characteristics of Machine-Generated Texts in Slovenian and English" PhD study.

## Data Generation

Several models were used with prompts that were designed using metadata from various human-written corpora. The generation procedure used for each corresponding human-written corpus is described below.

### Šolar

Prompts used: see LLM/text_generation/text_generation_prompts.txt

Process summary: 
We employed a human annotator to find existing explicitly mentioned titles within the Šolar corpus and used those to build prompts for generating MGT using LLMs (see below for a list). The prompt template is stored in LLM_text_generation/text_generation_prompts.md. We generated a corresponding MG essay and ran the analysis only on those texts from Šolar that:

1. are labeled as "esej ali spis" in the corpus metadata
2. are written by 4th year gimnazija students (this is done to single out a subset of Šolar that most corresponds to British A-level student proficiency, as this is what we take as the relevant subset of essays in the LOCNESS corpus)
3. have an explicitly mentioned essay title or explicitly refer to some literary work as the basis for the content. This ensures that the content of the MG essays stays as close to the HW essays as possible, since this information is featured in the prompt.

The IDs of all the relevant Šolar texts are stored in Solar_relevant_doc_ids.txt. 

Models used:
- GPT-5 - the default ChatGPT model, currently still a very widely used AI text generation platform

## Data Preprocessing

Grammatical annotation tools used:
- Trankit - using the model retrained on the SSJ UD and SST UD treebanks v2.15: [https://www.clarin.si/repository/xmlui/handle/11356/1997](https://www.clarin.si/repository/xmlui/handle/11356/1997). We chose this model to annotate the Slovenian texts, since it achieves SOTA performance on the UD dependency parsing task, which is crucial for studies of syntax.

## Data Analysis

The data analysis phase was carried out using the ComparaTree tool for comparative linguistic analysis of treebanks: [https://github.com/clarinsi/ComparaTree/tree/main](https://github.com/clarinsi/ComparaTree/tree/main).

The experiments were carried out in the following order:
- Šolar vs Šolar_GPT-5: The relevant essays from the Šolar 3.0 corpus were first compared to the corresponding essays from the machine-generated Šolar_GPT-5 corpus (see above for the criteria for selecting relevan essays). The results of this phase are stored in data_analysis/Solar_vs_Solar-GPT-5/. Command used to run ComparaTree:
`python src/run_analysis.py --first_file XXXX.conllu --second_file YYYY.conllu --output_dir OOOO --analysis_levels "full"`
