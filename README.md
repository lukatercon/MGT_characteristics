# MGT_characteristics
Repository for the code used for data generation and data preparation in the "Comparison of Syntactic Characteristics of Machine-Generated Texts in Slovenian and English" PhD study.

## Data Generation

Several models were used with prompts that were designed using metadata from various human-written corpora. The generation procedure used for each corresponding human-written corpus is described below.

The scripts used for data generation are contained in LLM_text_generation/. The hyperparameters used for data generation can be found in LLM_text_generation/generation_hyperparameters.

### Šolar

Prompts used: see LLM_text_generation/text_generation_prompts.txt. This includes the default prompts, as well as the alternative persona-aware and metalinguistically-aware prompts, and others. 

Process summary: 
We employed a human annotator to find existing explicitly mentioned titles within the Šolar corpus and used those to build prompts for generating MGT using LLMs (see below for a list). The default prompt template is stored in LLM_text_generation/text_generation_prompts.md. We generated a corresponding MG essay and ran the analysis only on those texts from Šolar that:

1. are labeled as "esej ali spis" in the corpus metadata
2. are written by 4th year gimnazija students (this is done to single out a subset of Šolar that most corresponds to British A-level student proficiency, as this is what we take as the relevant subset of essays in the LOCNESS corpus)
3. have an explicitly mentioned essay title or explicitly refer to some literary work as the basis for the content. This ensures that the content of the MG essays stays as close to the HW essays as possible, since this information is featured in the prompt.

The IDs of all the relevant Šolar texts are stored in Solar_relevant_doc_ids.txt. 

With GaMS-27B, we additionally excluded texts shorter than 100 words in order to ensure that none of the cases in which the model refused to provide a response made it into the comparison process. We also found that in one specific case "solar28", the model returned only the title repeated over and over in a long loop. Consequently we excluded this case from the comparison as well. The corresponding human-written essays were also excluded from the human-written text corpus during the analysis phase in order to ensure a fair comparison.

After generating the texts using the default prompt, the alternative persona-aware prompt and metalinguistically aware prompt was also used to generate an additional set of texts using the GaMS-27B and gemma-2-27B models (and GPT-5, albeit only with the metalinguistically aware alternative prompt). This was done to assess the degree to which prompt wording affects the generated texts. Several othed alternative prompt wordings were also tested.


Models used:
- GPT-5 - the default ChatGPT model, currently still a very widely used AI text generation platform (specific checkpoint name: gpt-5-2025-08-07)
- GaMS-27B-Instruct - LLM specifically aimed at generating Slovenian texts developed as part of the PoVeJMo project - 27 billion parameter version: [https://huggingface.co/cjvt/GaMS-27B-Instruct](https://huggingface.co/cjvt/GaMS-27B-Instruct)
- gemma-2-27b-it - the LLM that the GaMS-27B model was based on: [https://huggingface.co/google/gemma-2-27b-it](https://huggingface.co/google/gemma-2-27b-it)
*- GaMS-1B-Chat - LLM specifically aimed at generating Slovenian texts developed as part of the PoVeJMo project - 1 billion parameter version: [https://huggingface.co/cjvt/GaMS-1B-Chat](https://huggingface.co/cjvt/GaMS-1B-Chat)*
*- GaMS-27B-Instruct-Nemotron - LLM specifically aimed at generating Slovenian texts developed as part of the PoVeJMo project - 27 billion parameter version finetuned on the Nemotron machine-translated instruction tuning dataset: [https://huggingface.co/GaMS-Beta/GaMS-27B-Instruct-Nemotron](https://huggingface.co/GaMS-Beta/GaMS-27B-Instruct-Nemotron)*


### LOCNESS

Prompts used: see LLM_text_generation/text_generation_prompts.txt. This includes the default prompts, as well as the alternative persona-aware and metalinguistically-aware prompts.

Process summary: 
Since the LOCNESS corpus often lacks overtly expressed essay titles, the essays were first manually inspected and assigned a title. If the essay contained an explicitly expressed title somewhere within the body of the essay or before the body, this was used as the title. If not, a new essay title was inferred from the content. For one essay (dubbed 8-28 in our ID scheme), the title could not be successfully inferred, thus the essay was excluded from the final analysis. The resulting essay titles for each essay ID are contained in LOCNESS_relevant_doc_ids.txt. The essay IDs inside this file were newly constructed, since the original corpus lacks a unified essay ID scheme.

## Data Preprocessing

Grammatical annotation tools used:
- Trankit - using the model retrained on the SSJ UD and SST UD treebanks v2.15: [https://www.clarin.si/repository/xmlui/handle/11356/1997](https://www.clarin.si/repository/xmlui/handle/11356/1997). We chose this model to annotate the Slovenian texts, since it achieves SOTA performance on the UD dependency parsing task, which is crucial for studies of syntax.
