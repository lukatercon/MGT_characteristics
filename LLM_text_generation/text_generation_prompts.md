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
