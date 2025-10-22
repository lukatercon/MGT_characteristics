# MGT_characteristics
Repository for the code used for data generation and data preparation in the "Comparison of Syntactic Characteristics of Machine-Generated Texts in Slovenian and English" PhD study.

## Data Generation

Prompts used: see LLM/text_generation/text_generation_prompts.txt

### Šolar

Models used:
- GPT-5 - the default ChatGPT model, currently still a very widely used AI text generation platform

Grammatical annotation tools used:
- Trankit - using the model retrained on the SSJ UD and SST UD treebanks v2.15: [https://www.clarin.si/repository/xmlui/handle/11356/1997](https://www.clarin.si/repository/xmlui/handle/11356/1997). We chose this model, since it achieves SOTA performance on the UD dependency parsing task, which is crucial for studies of syntax.
