# Machine Translation for Middle Egyptian-English

This repo preprocesses various corpora of Middle Egyptian transliterations to an identical format, and then feeds them into an OpenNMT machine translation pipeline.

Supervised and semi-supervised learning techniques will be used to optimize output for this extremely low resource language.

**Supervised case**:  
Corpus size: 12938 aligned sentences  
Current max BLEU score = 42.22

**Semi-supervised case**:  
Corpus size: 50,457 monolingual sentences + 12938 aligned sentences  
Current max BLEU score = ??? (in progress)  

In-progress:  
- [x] Parse pyramid texts from PDF to add additional ~5k aligned sentences  
- [x] Preprocess newly added aligned sentences
- [x] Update machine translation notebook with new BLEU score after corpus expanded
- [ ] Complete back-translation and semi-supervised machine translation pipeline  
