# MGT_characteristics
Repository for the code used for data generation and data preparation in the "Comparison of Syntactic Characteristics of Machine-Generated Texts in Slovenian and English" PhD study.

## Data Generation

Several models were used with prompts that were designed using metadata from various human-written corpora. The generation procedure used for each corresponding human-written corpus is described below.

### Šolar

Prompts used: see LLM_text_generation/text_generation_prompts.txt. This includes the default prompts, as well as the alternative persona-aware and metalinguistically-aware prompts. 

Process summary: 
We employed a human annotator to find existing explicitly mentioned titles within the Šolar corpus and used those to build prompts for generating MGT using LLMs (see below for a list). The default prompt template is stored in LLM_text_generation/text_generation_prompts.md. We generated a corresponding MG essay and ran the analysis only on those texts from Šolar that:

1. are labeled as "esej ali spis" in the corpus metadata
2. are written by 4th year gimnazija students (this is done to single out a subset of Šolar that most corresponds to British A-level student proficiency, as this is what we take as the relevant subset of essays in the LOCNESS corpus)
3. have an explicitly mentioned essay title or explicitly refer to some literary work as the basis for the content. This ensures that the content of the MG essays stays as close to the HW essays as possible, since this information is featured in the prompt.

The IDs of all the relevant Šolar texts are stored in Solar_relevant_doc_ids.txt. 

With GaMS-27B, we additionally excluded texts shorter than 100 words in order to ensure that none of the cases in which the model refused to provide a response made it into the comparison process. We also found that in one specific case "solar28", the model returned only the title repeated over and over in a long loop. Consequently we excluded this case from the comparison as well. The corresponding human-written essays were also excluded from the human-written text corpus during the analysis phase in order to ensure a fair comparison.

After generating the texts using the default prompt, the alternative persona-aware prompt and metalinguistically aware prompt was also used to generate an additional set of texts using the GaMS-27B and gemma-2-27B models (and GPT-5, albeit only with the metalinguistically aware alternative prompt). This was done to assess the degree to which prompt wording affects the generated texts. All alternative prompts were found to produce very similar results to the default prompt (???????????). 
#### ==TODO: Check if these differences are statistically significant or not. We need to know whether we can make any claims at all about the alternative prompts.==


Models used:
- GPT-5 - the default ChatGPT model, currently still a very widely used AI text generation platform (specific checkpoint name: gpt-5-2025-08-07)
- GaMS-27B-Instruct - LLM specifically aimed at generating Slovenian texts developed as part of the PoVeJMo project - 27 billion parameter version: [https://huggingface.co/cjvt/GaMS-27B-Instruct](https://huggingface.co/cjvt/GaMS-27B-Instruct)
- gemma-2-27b-it - the LLM that the GaMS-27B model was based on: [https://huggingface.co/google/gemma-2-27b-it](https://huggingface.co/google/gemma-2-27b-it)
*- GaMS-1B-Chat - LLM specifically aimed at generating Slovenian texts developed as part of the PoVeJMo project - 1 billion parameter version: [https://huggingface.co/cjvt/GaMS-1B-Chat](https://huggingface.co/cjvt/GaMS-1B-Chat)*
*- GaMS-27B-Instruct-Nemotron - LLM specifically aimed at generating Slovenian texts developed as part of the PoVeJMo project - 27 billion parameter version finetuned on the Nemotron machine-translated instruction tuning dataset: [https://huggingface.co/GaMS-Beta/GaMS-27B-Instruct-Nemotron](https://huggingface.co/GaMS-Beta/GaMS-27B-Instruct-Nemotron)*


## Data Preprocessing

Grammatical annotation tools used:
- Trankit - using the model retrained on the SSJ UD and SST UD treebanks v2.15: [https://www.clarin.si/repository/xmlui/handle/11356/1997](https://www.clarin.si/repository/xmlui/handle/11356/1997). We chose this model to annotate the Slovenian texts, since it achieves SOTA performance on the UD dependency parsing task, which is crucial for studies of syntax.

## Data Analysis

The data analysis phase was carried out using the ComparaTree tool for comparative linguistic analysis of treebanks: [https://github.com/clarinsi/ComparaTree/tree/main](https://github.com/clarinsi/ComparaTree/tree/main).

As several measures included in ComparaTree are based on a special segment-based averaging method, the optimal value for the segment length had to be estableished first. We plotted the rank-frequency distributions for texts produced by GaMS-27B and humans for the following segment lengths: [100, 500, 1000, 5000, 10000, 20000]. It was found that, for the segmental type-token ratio and the tree diversity score, an approximate Zipfian distribution forms around n=1000. This was not found to be the case for the 3-gram diversity score, as we do not get an approximate Zipfian distribution even for n=20000. As a fallback method, we checked whether the tendencies for the 3-gram diversity scores were the same for all the aforementioned values of n (in which dataset the values were higher, etc.).   
#### ==TODO: Describe also how you checked the rank frequency distributions for different values of n and checked whether the trends hold==

The experiments were carried out in the following order:
- Šolar vs Šolar_GPT-5: The relevant essays from the Šolar 3.0 corpus were first compared to the corresponding essays from the machine-generated Šolar_GPT-5 corpus (see above for the criteria for selecting relevant essays). The results of this phase are stored in data_analysis/Solar_vs_Solar-GPT-5/. Command used to run ComparaTree:
`python src/run_analysis.py --first_file XXXX.conllu --second_file YYYY.conllu --output_dir OOOO --analysis_levels "full"`
Afterwards, the following three additional comparisons were run:
- Šolar vs Šolar-GaMS-1B:
- Šolar vs Šolar-GaMS-27B:
- Šolar vs Šolar-gemma-2-27B:
