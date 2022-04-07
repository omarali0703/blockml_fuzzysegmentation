# Python micro logic

> lets one create small scripts internally that can be run separately. These don't have to be stored here, but it keeps everything together you know?

## SLSeg parsing with the micro logic script
```bash
python3 micro_logic.py slseg '../dependencies/phd_datasets/slseg_outputs/gum/' True '../dependencies/phd_datasets/slseg_outputs/gum/binary'
```
## RS3 parsing with the micro logic script
> We need to use this code to parse the outputs of GUM. Whilst we have already done this, we may want more GUM data later so its good to have this here. This is also the wrong paths so we need to alter it.
```bash
python3 micro_logic.py rs3parse 'dependencies/phd_datasets/gum_dataset/small_sample/academic' True 'dependencies/phd_datasets/gum_outputs/original_gum_text_bin/academic'

python3 micro_logic.py rs3parse 'dependencies/phd_datasets/gum_dataset/small_sample/fiction' True 'dependencies/phd_datasets/gum_outputs/original_gum_text_bin/fiction'

# Large Sample
python3 micro_logic.py rs3parse 'dependencies/phd_datasets/gum_dataset/large_sample' True 'dependencies/phd_datasets/gum_outputs/original_gum_text_bin/large_sample'
```

## Sentence-clause parsing a set of text
> We Sentence-clause parse to produce a simple benchmark to compare the rest of the results with.

```bash
python3 micro_logic.py clauseparse 'dependencies/phd_datasets/gum_outputs/original_gum_text' 'dependencies/phd_datasets/clause_outputs/'
```

### Converting some RS3 data to original text
> Small and Large sample logic

```bash
python3 micro_logic.py rs3originaltext 'dependencies/phd_datasets/gum_dataset/small_sample' 'dependencies/phd_datasets/gum_outputs/original_gum_text'

python3 micro_logic.py rs3originaltext 'dependencies/phd_datasets/gum_dataset/large_sample' 'dependencies/phd_datasets/gum_outputs/original_gum_text/large_sample'
```

### Validate a set of refs and computed boundaries
The inputs are taken as binaries here. First directory is the ref boundary locations, the second is the computed.
```bash
# Code for SLSeg
python3 micro_logic.py validateboundaries 'dependencies/phd_datasets/gum_outputs/original_gum_text_bin' 'dependencies/phd_datasets/slseg_outputs/gum/binary'

# Code for SEGBOT
python3 micro_logic.py validateboundaries 'dependencies/phd_datasets/segbot_outputs/SEGBOT_TEST' 'dependencies/phd_datasets/gum_outputs/original_gum_text_SEGBOT_TEST' 

# Code for SENTENCE-CLAUSE
python3 micro_logic.py validateboundaries 'dependencies/phd_datasets/clause_outputs' 'dependencies/phd_datasets/gum_outputs/original_gum_text_bin' 

```


## RST Workflow (Testing and validating SLSeg)
1. Convert RS3 data to text data --> Run **Converting some RS3 data to original text** first, to generate our test data in TEXT form
2. Get GUM reference using **RST parsing with micro logic script**
3. Run SLSeg on that data to get its segmentation.
4. run ```bash python3 run_all.py ../phd_datasets/gum_outputs/original_gum_text ../phd_datasets/slseg_outputs/gum ./parser05Aug16 -T50```
5. Delete everything BUT the contents of folder_5. such that the "gum" folder only contains the .rs3 files.
6. Parse these outputs using **SLSeg Parsing with the micro logic script** command.
7. Run the **Validate a set of refs and computed boundaries** command to produce your results
8. Dance and sing, for you have compared a given method to the ground truth.


## Convering RS3 data to training data for use in our FIS.
> To train/generate our FIS needed for FuzzySeg, we need to generate 50% training data needed from GUM. To do so we call the below function.
> Run the below command from ROOT, the first command is the large ds version for larger memory comps. The second is a small test test that runs a little faster and on low memory comps
> Final number is the amount of docs to parse into training data.
> If running in DEP mode. Make sure to run the CoreNLP server on port9000. https://stanfordnlp.github.io/CoreNLP/download.html

```bash
# For DEP mode, first run:
java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000
# inside the CoreNLP Dependency folder.
```

```bash
# Syntax/Stanford Mode
python3 micro_logic.py rs3trainingdata "dependencies/phd_datasets/gum_dataset/rst/rstweb/" "dependencies/phd_datasets/fuzzyseg_outputs/fis_training/" 1 5 'syntax'

python3 micro_logic.py rs3trainingdata "dependencies/phd_datasets/gum_dataset/small_sample/" "dependencies/phd_datasets/fuzzyseg_outputs/fis_training/" 1 3 'syntax'

# Generated Sample
python3 micro_logic.py rs3trainingdata "dependencies/phd_datasets/gum_dataset/small_sample/generated" "dependencies/phd_datasets/fuzzyseg_outputs/fis_training/generated" 20 3 'syntax'

# Large Sample
python3 micro_logic.py rs3trainingdata "dependencies/phd_datasets/gum_dataset/large_sample/" "dependencies/phd_datasets/fuzzyseg_outputs/fis_training/large_sample" 1 3 'syntax'

# Example with the subdirs for fiction and academic etc.
python3 micro_logic.py rs3trainingdata "dependencies/phd_datasets/gum_dataset/small_sample/academic" "dependencies/phd_datasets/fuzzyseg_outputs/fis_training/academic" 5 3 'syntax'

# Charniak syntax
python3 micro_logic.py rs3trainingdata "dependencies/phd_datasets/gum_dataset/small_sample/" "dependencies/phd_datasets/fuzzyseg_outputs/fis_training/" 1 5 'char'

# DEP mode.
python3 micro_logic.py rs3trainingdata "dependencies/phd_datasets/gum_dataset/small_sample/" "dependencies/phd_datasets/fuzzyseg_outputs/fis_training/" 1 5 'dep'

```

## Generating small RST samples from big sets

```bash
python3 micro_logic.py generatedsmall "dependencies/phd_datasets/gum_dataset/large_sample" "dependencies/phd_datasets/gum_dataset/small_sample/generated" 30
```

## Sentiment Analysis Workflow

> run for the review-musical-instruments data, the 5/10 means wbat the sentiment score is out of. 5 = 5* rating, and 10 is a rating out of 10 (obviously)
> The Pang-lee set is out of 10, whilst the other is out of 5.
```bash
python3 micro_logic.py sentimentcasestudy "dependencies/phd_datasets/sentiment_data" 5 False
```

> Run for pang-lee data
```bash
python3 micro_logic.py sentimentcasestudy "dependencies/phd_datasets/sentiment_data" 10 False
```


> Run for pang-lee data with RST weights
```bash
python3 micro_logic.py sentimentcasestudy "dependencies/phd_datasets/sentiment_data" 10 True
```

## HILDA Workflow (TODO)

1. Convert fuzzyseg outputs into hilda inputs.
2. Run hilda with new command that takes the fuzzyseg inputs and uses them instead of the segmenter.