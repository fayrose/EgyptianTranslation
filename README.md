# Machine Translation for Middle Egyptian-English

This repo preprocesses various corpora of Middle Egyptian transliterations to an identical format, then uses supervised and semi-supervised learning techniques with OpenNMT for machine translation. Afterwards, the results are quantified using token-accuracy, perplexity, cross-entropy and BLEU score.

**Supervised case**:  
Corpus size: 12,938 aligned sentences  
Current max BLEU score = 42.22

**Semi-supervised case**:  
Corpus size: 50,457 monolingual sentences + 12,938 aligned sentences  
Current max BLEU score = 41.78

In-progress:  
- [x] Parse pyramid texts from PDF to add additional ~5k aligned sentences  
- [x] Preprocess newly added aligned sentences
- [x] Update machine translation notebook with new BLEU score after corpus expanded
- [x] Semi-supervised machine translation pipeline  
