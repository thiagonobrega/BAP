# Blind Attribute Pairing (BAP)

Welcome to the BAP GitHub. This GitHub contains the proof-of-concept of "Schema Matching" solution to scenarios where privacy is required. This solution was presented as a conference paper in ACM-SAC 2018 (https://doi.org/10.1145/3167132.3167193), and in my master degree dissertation. In this page contains all elements (source code, scripts, and datasets) needed to ensure de repeatability of the BAP results. 

## About BAP

In many scenarios, it is necessary to identify records referring to the same real-world object across different data sources (Record Linkage). Yet, such need is often in contrast with privacy requirements concerning (e.g., identify patients with the same diseases, genome matching, and fraud detection). Thus, in the cases where the parties interested in the Record Linkage process need to preserve the privacy of their data, Privacy-Preserving Record Linkage (PPRL) approaches are applied to address the privacy problem. In this sense, the first step of PPRL is the agreement of the parties about the data (attributes) that will be used during the record linkage process. Thus, to reach an agreement, the parties must share information about their data schema, which in turn can be utilized to break the data privacy. To overcome the (vulnerability) problem caused by the schema information sharing, we propose a novel privacy- preserving approach for attribute pairing to aid PPRL applications. Empirical experiments demonstrate that our privacy-preserving approach improves considerably the efficiency and effectiveness in comparison to a state-of-the-art baseline.

For more information https://www.sigapp.org/sac/sac2018 .


## Installation 

    $ git clone 
    $ cd bap/
    $ pip install -r requirements.txt

## Re-run the experiments

- The datasets need to be extracted  (see [execution/README.md](data/README.md) )
- Run the execution scripts (see [execution/README.md](scripts/README.md) )

## Presentations and text

 - [ACM SAC18 Presentation](https://1drv.ms/p/s!AiduPqZxUF_qi4Mb3Q2gGVeZ6K8hJA)  
 - ACM SAC18 Paper
 - [MS.c Presentation (Portuguese) ](https://1drv.ms/p/s!AiduPqZxUF_qjZonchHU41EYKUPXKA)
 - MS.c Dissertation
