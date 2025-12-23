# Prompt Templates

## Šolar 3.0 MGT (Slovenian)

### Default Prompt

```
Napiši esej z naslovom {essay_title} in podnaslovom {essay_subtitle}, ki se nanaša na literarno delo {referenced_literary_work}, s približno {length_of_corresponding_HWT} besedami. Odgovori samo z esejem brez spremnega besedila.
```

The three bracketed elements are included in the prompt depending on the availability of the relevant data (title, subtitle, referenced literary work). For the system prompt, the simple English prompt "You are a helpful assistant." is used (for getting the Slovenian data as well), as this reflects the system prompt that the average user will have when using the in-browser ChatGPT interface.

### Persona-Aware Prompt

```
Napiši esej z naslovom {essay_title} in podnaslovom {essay_subtitle}, ki se nanaša na literarno delo {referenced_literary_work}, s približno {length_of_corresponding_HWT} besedami. Esej napiši, kot bi ga napisal dijak 4. letnika gimnazije iz kraja: {region} pri predmetu: {subject}. Odgovori samo z esejem brez spremnega besedila.
```

This prompt additionally incorporates information about the school grade, school type, region of Slovenia that the student is from and the school subject. It therefore constructs a type of persona for the LLM to assume when generating the text.

### Persona-Aware Prompt with Writer Age

```
Napiši esej z naslovom {essay_title} in podnaslovom {essay_subtitle}, ki se nanaša na literarno delo {referenced_literary_work}, s približno {length_of_corresponding_HWT} besedami. Esej napiši, kot bi ga napisal {age} let star pisec. Odgovori samo z esejem brez spremnega besedila.
```

This prompt additionally incorporates information about the age of the writer.

### Persona-Aware Prompt with Writer Grade

```
Napiši esej z naslovom {essay_title} in podnaslovom {essay_subtitle}, ki se nanaša na literarno delo {referenced_literary_work}, s približno {length_of_corresponding_HWT} besedami. Esej napiši, kot bi ga napisal pisec, ki hodi v {grade} {school}. Odgovori samo z esejem brez spremnega besedila.
```

This prompt additionally incorporates information about the school grade of the writer.

### Alternative Prompt for Longer Responses

```
Napiši esej z naslovom {essay_title} in podnaslovom {essay_subtitle}, ki se nanaša na literarno delo {referenced_literary_work}, s približno {length_of_corresponding_HWT*2} besedami. Odgovori samo z esejem brez spremnega besedila.
```
Due to GaMS-27B producing unexpectedly short responses (e.g. generating an essay with 50 words, when prompted to produce an essay with 700 words), the above prompt was also used to see if GaMS would produce longer responses.

### Metalinguistically-Aware Prompt

**Option 1**

```
Napiši esej z naslovom {essay_title} in podnaslovom {essay_subtitle}, ki se nanaša na literarno delo {referenced_literary_work}, s približno {length_of_corresponding_HWT} besedami. Esej napiši, kot bi ga napisal dijak 4. letnika gimnazije iz kraja: {region} pri predmetu: {subject}. Bodi pozoren, da bo jezik v eseju čim bolj podoben jeziku, ki bi ga sproduciral omenjeni dijak, pri čemer posebej pazi na primerno dolžino eseja, dolžino povedi, leksikalno raznolikost, raznolikost n-gramov, raznolikost skladenjskih dreves, skladenjsko kompleksnost (povprečno dolžino skladenjskih relacij) in porazdelitev besednovrstnih oznak in tipov skladenjskih relacij. Odgovori samo z esejem brez spremnega besedila.
```

**Option 2 (incorporating the exact differences between Šolar-human and Šolar-GaMS-27B)**
```
Napiši esej z naslovom {essay_title} in podnaslovom {essay_subtitle}, ki se nanaša na literarno delo {referenced_literary_work}, s približno {length_of_corresponding_HWT} besedami. Esej napiši, kot bi ga napisal dijak 4. letnika gimnazije iz kraja: {region} pri predmetu: {subject}. Bodi pozoren, da bo jezik v eseju čim bolj podoben jeziku, ki bi ga sproduciral omenjeni dijak, pri čemer posebej pazi, da bodo dolžine esejev daljše kot običajno, dolžine povedi krajše, leksikalna raznolikost višja, raznolikost n-gramov višja, raznolikost skladenjskih dreves višja in skladenjska kompleksnost (povprečna dolžina skladenjskih relacij) nižja. Med besednovrstnimi oznakami morajo biti bolj pogosti pomožni glagoli, glagoli in zaimki, manj pa mora biti samostalnikov, pridevnikov in predlogov. Med tipi skladenjskih relacij morajo biti bolj pogosti prislovni modifikatorji, pomožni glagoli in predmeti, manj pa mora biti pridevniških modifikatorjev, samostalniških modifikatorjev in prirednih zvez. Odgovori samo z esejem brez spremnega besedila.
```

In addition to including information about the writer of the essay, this prompt also additionally instructs the model to produce language that is linguistically as close as possible to the profile of the writer. The first option only lists the linguistic characteristics that the model should try to adjust, while the second option also describes how these characteristics should be adjusted, considering the differences that arise from the Solar-human_vs_Solar-GaMS-27B comparison. 
