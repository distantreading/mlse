## Roadmap for the project

1. Select all language collections that have at least 9 different authors represented with 3 different novels from ELTeC (that's currently 8 collections) to create the ELTeC Authorship Attribution Benchmark Dataset. See overview of ELTeC here: https://distantreading.github.io/ELTeC/. (DONE)
2. Copy only the XML-files (preferably level-1) over to the corpus folder here that correpond to these authors, separated by language. Each collection should have at least 24 novels in them. (Decide whether to use more if available? Yes, up to 12? Or even more? pol has 33.) (DONE, using all available novels)
3. Extract the main body text as plain text from these XML files and save into a separate folder; retain original file names. Consider some segmentation of novels into multiple documents (say, 20,000 words each) to increase the number of available instances for sampling (see below). (DONE, segmentation to be done at a later stage, e.g. in step #7) 
4. Extract metadata from these XML files (xml:id, language, author, title, year of first publication, timeSlot, author-gender, author-birth-year, length class, reprint count, others?) into one big metadata table (metadata.tsv). (DONE, but using separate metadata files for the moment.) 
5. Optionally, include additional metadata. With help from the collection editors, add additional metadata like narrative perspective and subgenre information. If possible, use the Kraków-Antwerp pipeline to add information about proportion of direct speech in each novel. (POSTPONED)
6. Perform a comparative analysis of the metadata as an indicator of what level of attribition accuracy we expect (a) for a given language collection as a whole, but also (b) for specific authors within a given language collection. This based on the assumption that better metadata-based separation of authors should be reflected in higher accuracy in the stylometric analyses, and that stronger similarity within the texts of the authors should also be reflected in higher accuracy for these authors. Formulate specific hypotheses based on this. Indicators could be the range and distribution of metadata categories, or even a classification experiment based exclusively on the metadata.  (DONE)
7. Create a script that runs stylo in a multi-language (each language separately), multi-parameter (mfw, classifier), multi-fold (cross-validations) loop with a classification task and records all performance data (classification accuracy, principally) into a big table (TODO Maciej)
8. Visualize the average (median, standard deviation) performance for each language in comparison, to see whether there are differences in performance between collections. 
9. Check the performance results (a) per collection and (b) per author against the hypotheses formulated in step #6 (predicted accuracies). 
10. Visualize the detailed performance for each language as a function of key parameters (2-3 classifiers, mfw, with mean and standard deviation from sampling)
11. Visualize results from the best parametes as a confusion matrix to see which authors are easily mixed up and which are clearly recognized. 
12. With the best mfw parameters for each language, also do a clustering and dendrogram visualization, for visual inspection by experts. 
13. Discuss results with the domain experts, i.e. the creators of each collection, to develop hypotheses to explain the most common classification errors and the composition of the collection. 
14. Write it all up, keep data and code here in the repo, submit to JCLS or DH2022. 

## Notes
1. For the sake of consistency and comparability, the Polish-language collection probably needs to be excluded from the dataset because it is structured quite a bit differently from the other collections, and because metadata pertaining to publication year is missing or not encoded in a standardized way. 

