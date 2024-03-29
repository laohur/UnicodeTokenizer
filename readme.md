# UnicodeTokenizer

UnicodeTokenizer: tokenize all Unicode text 

## 切词规则 Tokenize Rules
* break line
* Punctuation
* UnicodeScripts
* Split(" ?[^(\\s|[.,!?…。，、।۔،])]+"
* break word

## use
> pip install UnicodeTokenizer

```python
from UnicodeTokenizer import UnicodeTokenizer
tokenizer=UnicodeTokenizer()

line = """ 
        首先8.88设置 st。art_new_word=True 和 output=[açaí]，output 就是最终 no such name"
        的输出คุณจะจัดพิธีแต่งงานเมื่อไรคะ탑승 수속해야pneumonoultramicroscopicsilicovolcanoconiosis"
        하는데 카운터가 어디에 있어요ꆃꎭꆈꌠꊨꏦꏲꅉꆅꉚꅉꋍꂷꂶꌠلأحياء تمارين تتطلب من [MASK] [PAD] [CLS][SEP]
        est 𗴂𗹭𘜶𗴲𗂧, ou "phiow-bjij-lhjij-lhjij", ce que l'on peut traduire par « pays-grand-blanc-élevé » (白高大夏國). 
    """.strip()
print(tokenizer.tokenize(line))
print(tokenizer.split_lines(line))

```
or 
```bash
git clone https://github.com/laohur/UnicodeTokenizer
cd UnicodeTokenizer # modify 
pip install -e .
```


## reference
* PyICU https://gitlab.pyicu.org/main/pyicu
* tokenizers https://github.com/huggingface/tokenizers
* ICU-tokenizer https://github.com/mingruimingrui/ICU-tokenizer/tree/master


## License
[Anti-996 License](https://github.com/996icu/996.ICU/blob/master/LICENSE)
