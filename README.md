# miRTarget
Prognosticate on the target of microRNA.

A bridge for automate psRNATarget and MirTarSite. Combine the sequencing data and deep-learning method to predict microRNA target using Selenium.

## Inroduction
MicroRNAs are non-coding RNA with 20-24 nucleotides in which found in animals, plants, and some virus. By base pairing with complementary sequencing, miRNAs cleave their target genes and inhibit gene expression. Therefore, predicting microRNA target gene is a cardinal importance of regulation. 

Previous studies had shown that bulges prevail among binding sites, making the prediction to be abstruse. Screening the transcriptome data might sustain fallacies. Researchers provided psRNATarget and MirTarSite to resolve the problem by scoring schema and deep-learning method, respectively. The results, however, could not done in the same platform.

miRTarget apply Selenium to aid combination between psRNATarget and MirTarSite in Python.

### Predict microRNA Target
#### Requirements
* Python 3.7+
* argparse
* MirTarSite (https://github.com/Samuel1043/mirtarsite)
* pandas
* Selenium (Chromedriver)

#### Input 
* microRNA fasta file
```
>osa-miR398b_MIMAT0000983
UGUGUUCUCAGGUCGCCCCUG
>osa-miR166i-5p_MIMAT0022883
AAUGCAGUUUGAUCCAAGAUC
```
* transcriptome fasta file (Os-Nipponbare-Reference-IRGSP-1.0)
```
>LOC_Os01g01010.1 cDNA|TBC domain containing protein, expressed
AGATGAGCTGGTGGGGATGCTCTAAGAGAACGAGAGAAGCACAGAGCAGATAAACCACAC
CCACAGGCACCACCGTCCTTGTTGGTAATGAAGAAGACGAGACGACGACTTCCCCACTAG
GAAACACGACGGAGGCGGAGATGATCGACGGCGGAGAGAGCTACAGAAACATCGATGCCT
CCTGTCCAATCCCCCCATCCCATTCGGTAGTTGGATTGAAGACTACCGAATAAGAGAAGC
AGGCAGGCAGACAAACCCTTGAACCAAGGAGTCCTCGCTGAGGAAGCTTTGGATCCACGA
CGCAGCTATGGCCTCCCCGCCCACCAGGCCGCCAGCCACAACCAGCTGACTAGGTAGGCT
TCCTAGGTCGCATGCATCATCAGATTTCAATCTCCCTTCGTTCCCTGTCCCTAATCCAAT
```

#### Usage
Please make sure MirTarSite folder is under the mirTarget
```
python mirTarget.py [-h] FULL-PATH-TO-microRNA-FASTA-FILE FULL-PATH-TO-TRANSCRIPTOME-FASTA-FILE

miRTarget
Tools to combine psRNAtarget and MirTarSite
Please type in the full path of miRNA and transcriptome data for analyzing!

positional arguments:
miRNA                 microRNA fasta file 5'->3' sequence
transcritome          transcriptome fasta file 5'->3' sequence

optional arguments:
  -h, --help  show this help message and exit
```