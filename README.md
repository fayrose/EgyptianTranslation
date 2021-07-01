# Machine Translation for Middle Egyptian-English

This repo preprocesses various corpora of Middle Egyptian transliterations to an identical format, and then feeds them into an OpenNMT machine translation pipeline.

Supervised and semi-supervised learning techniques will be used to optimize output for this extremely low resource language.

**Supervised case**:  
Corpus size: 8176 aligned sentences  
Current max BLEU score = 27.84

**Semi-supervised case**:  
Corpus size: 50,457 monolingual sentences + 8176 aligned sentences  
Current max BLEU score = ??? (in progress)  

In-progress:  
- [x] Parse pyramid texts from PDF to add additional ~5k aligned sentences  
- [ ] Preprocess newly added aligned sentences
- [ ] Complete back-translation and semi-supervised machine translation pipeline  
