# MGT_characteristics
Repository for the code used for data generation and data preparation in the "Comparison of Syntactic Characteristics of Machine-Generated Texts in Slovenian and English" PhD study.

## Data Generation

Prompts used: see LLM/text_generation/text_generation_prompts.txt

### Šolar

Process summary: 
We employed a human annotator to find existing explicitly mentioned titles within the Šolar corpus and used those to build prompts for generating MGT using LLMs (see below for a list). The prompt template is stored in LLM_text_generation/text_generation_prompts.md. We generated a corresponding MG essay only for those texts from Šolar that:

1. are labeled as "esej ali spis" in the corpus metadata
2. have an explicitly mentioned essay title or at least explicitly refer to some literary work as the basis for the content. This ensures that the content of the MG essays stays as close to the HW essays as possible.

Models used:
- GPT-5 - the default ChatGPT model, currently still a very widely used AI text generation platform

Grammatical annotation tools used:
- Trankit - using the model retrained on the SSJ UD and SST UD treebanks v2.15: [https://www.clarin.si/repository/xmlui/handle/11356/1997](https://www.clarin.si/repository/xmlui/handle/11356/1997). We chose this model to annotate the Slovenian texts, since it achieves SOTA performance on the UD dependency parsing task, which is crucial for studies of syntax.
