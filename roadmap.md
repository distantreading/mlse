## Roadmap for the project

1. Select all language collections that have at least 8 different authors represented with 3 different novels from ELTeC (that's currently 10 collections), see overview here: https://distantreading.github.io/ELTeC/. 
2. Copy only the XML-files (preferably level-1) over to the corpus folder here that correpond to these authors, separated by language. Each collection should have at least 24 novels in them. (Decide whether to use more if available? Yes, up to 12? Or even more? pol has 33.)
3. Extract metadata from these XML files (language, author, title, year, decade, author-gender, author-birth-year, length class, reprint count, others?) into one big metadata table (metadata.tsv). 
4. Optionally, include additional metadata. With help from the collection editors, add additional metadata like narrative perspective and subgenre information. If possible, use the Kraków-Antwerp pipeline to add information about proportion of direct speech in each novel.
4. Perform a comparative analysis of the metadata as an indicator of how difficult or easy a given language collection should be, based on the assumption that better metadata-based separation of authors should be reflected in higher accuracy in the stylometric analyses. Formulate hypotheses based on this. Indicators could be the range and distribution of metadata categories, or even a classification experiment based exclusively on the metadata.  
5. Create a script that runs stylo in a multi-language (each language separately), multi-parameter (mfw, classifier), multi-fold (cross-validations) loop with a classification task and records all performance data (classification accuracy, principally) into a big table
5. Visualize the average (median, standard deviation) performance for each language in comparison, to see whether there are differences in performance between collections. 
6. Check the performance results per collection against the hypotheses formulated above, based on the metadata. 
5. Visualize the detailed performance for each language as a function of key parameters (2-3 classifiers, mfw, with mean and standard deviation from sampling)
6. Visualize results from the best parametes as a confusion matrix to see which authors are easily mixed up and which are clearly recognized. 
5. With the best mfw parameters for each language, also do a clustering and dendrogram visualization, for visual inspection by experts. 
6. Discuss results with the domain experts, i.e. the creators of each collection, to develop hypotheses to explain the most common classification errors and the composition of the collection. 
