# Analyze-Generated-Distractors

[RU](README.md)
[<b>EN</b>](README.en.md)

## Repository description 

This repository contains materials and data from the research described in Section 3.2 “Analysis of generated distractors and comparison of various methods” of Nikita Login’s dissertation <b>“Automation of distractor (incorrect option) creation for language testing item banks”</b> for the degree of Candidate of Philological Sciences. 

## Repository structure 

The "synt-complexity" folder contains data and source code for experiments analyzing distractors obtained by different methods in terms of syntactic complexity. 

The "general" folder contains the data and source code for the remaining experiments described in Section 3.2. 

## "general" folder 

### Folder structure 

- The "notebooks" subfolder contains interactive Jupyter notebooks with the source code of the experiments and research carried out 
- The "data_for_comparison" subfolder contains data used in analytical comparisons (correlations, cross-tests) 
- The "data_input" subfolder contains input data for interactive notebooks 
- The "data_output_image" subfolder contains image files created in interactive notebooks 
- The "data_output_table" subfolder contains table files created in interactive notebooks 
- The "tools" subfolder contains Python modules used in interactive notebooks 


### Description of interactive Jupyter notebooks 

| File | Description | 
|------------------|--------------------| 
| attest_chatgpt.ipynb | Retrieving distractors from the ChatGPT model| 
| attest_deepseek.ipynb | Retrieving distractors from the DeepSeek model | 
| calculate_individual_scores.ipynb | Calculating individual sequence matching metric values ​​for each example | 
| combine_cross_tests.ipynb | Combination of cross-test results into one table | 
| corr_all.ipynb | Calculation of correlations between different metrics | 
| cross_test_ege.ipynb | Cross-test of lexical metrics on Unified State Examination data | 
| cross_test_ru_race_tf.ipynb | Cross-test of lexical metrics on Ru-RACE-TF data | 
| get_metrics_table.ipynb | Formation of table with the values ​​of the proposed metrics | 
| group_distractors.ipynb | Collection of distractors from different sources into one file | 
| lexical_metrics.ipynb | Computation of Lexical Complexity Metrics | 
| relevance_metrics.ipynb | Calculation of proposed relevance metrics | 
| score_outputs_gemini.ipynb | Calculation of distractor "incorrectness" metric using the Gemini model | 


## "synt-complexity" folder 

### Folder structure 

- The "notebooks" subfolder contains interactive Jupyter notebooks with the source code of the experiments and research carried out 
- The "data" subfolder contains data files used in notebooks and created during their work 

### Description of interactive Jupyter notebooks 

| File | Description | 
|------------------|--------------------| 
| synt_metrics.ipynb | Calculation of Syntactic Complexity Metrics | 
| synt_metrics_manova.ipynb | MANOVA Test for Syntactic Complexity Metrics |