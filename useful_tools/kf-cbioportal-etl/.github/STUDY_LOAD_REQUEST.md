---
name: cbioportal study load request
about: Use this issue template to create a request for a study to be loaded into the Kids First PedcBioportal
title: 'Load PedcBioportal study: '
labels: pedcbioportal
assignees: migbro, zhangb1

---

<!--Hi there! Please take a moment to fill out the template below.-->
## Description
This template is used to start a request to load, whether new or an update, a study onto the Kids First PedcBioPortal
## Common - any new study REQUIRED

1. If this is the first time being loaded, please fill out the cbio meta_study info, for instance:
    ```
    type_of_cancer: brain
    cancer_study_identifier: pbta_all
    name: Pediatric Brain Tumor Atlas (PBTA, Provisional)
    description: Genomic characterization of Pediatric Brain Tumor Atlas samples provided by the <a href="http://CBTTC.org">Children's Brain Tumor Tissue Consortium</a>, the <a href="http://www.pnoc.us/">Pacific Neuroncology Consortium (PNOC)</a>, and its partners via the <a href="http://kidsfirstdrc.org">Gabriella Miller Kids First Data Resource Center</a>. Updated Februrary 2020 from last load, July 2019.
    short_name: pbta_all
    ```
    - `type_of_cancer` can be found here: https://github.com/kids-first/kf-cbioportal-etl/blob/master/REFS/type_of_cancer
    - `cancer_study_identifier` should be in the form of `<type_of_cancer>_<study_id>_year`
    - `name` should be like a study title with a couple key words
    - `description` should be a like a short abstract with links, but **mind the 1024 character limit!**

1. Provide an example of a sample ID that can be used to tie together DNA and RNA (if applicable), aka a "somatic event ID":

1. Load/access control:
   - [ ] Load in QA Only
   - [ ] Load in Prod
   - [ ] **DO NOT LOAD AS PUBLIC**. USE GROUP NAME: 

## Kids First/PBTA
 - [ ] Check if this is a Kids First or PBTA (D3b) study
 - [ ] If creating a subset cohort, please provide a list of `BS_ID`:

## Publication/Collaboration
Publication is obvious, as `Collaboration` study would be something like OpenPBTA, OpenTargets, or other custom request
 - [ ] Check if publication
 - [ ] Check if collaboration

### Please provide the following:
1. A link to the paper (if applicable):
1. Link(s) or a description of where to find the genomic data to load. Acceptable types of data to load are
    - [Somatic variant calls in maf format](https://docs.cbioportal.org/5.1-data-loading/data-loading/file-formats#mutation-data)
    - Copy number calls as one or more of the following: [discrete copy number data](https://docs.cbioportal.org/5.1-data-loading/data-loading/file-formats#discrete-copy-number-data), [continuous copy number data](https://docs.cbioportal.org/5.1-data-loading/data-loading/file-formats#continuous-copy-number-data), [segmented data](https://docs.cbioportal.org/5.1-data-loading/data-loading/file-formats#segmented-data)
    - [RNAseq expression](https://docs.cbioportal.org/5.1-data-loading/data-loading/file-formats#expression-data) 
    - [RNAseq fusion](https://docs.cbioportal.org/file-formats/#structural-variant-data)
    - [Protein level data](https://docs.cbioportal.org/5.1-data-loading/data-loading/file-formats#protein-level-data)



1. [Patient metadata](https://docs.cbioportal.org/5.1-data-loading/data-loading/file-formats#clinical-patient-columns) that is available



1. [Sample metadata](https://docs.cbioportal.org/5.1-data-loading/data-loading/file-formats#clinical-sample-columns) that is available