# q2-decontam

# Installation

Within your qiime2 environment using R, run
```R
if (!requireNamespace("BiocManager", quietly = TRUE))
    install.packages("BiocManager")

BiocManager::install("decontam")
```

Then this plugin can be installed via
`pip install git+https://github.com/mortonjt/q2-decontam.git`

Make sure to refresh your environment via `qiime dev refresh-cache`



# Getting started
See the help menu to get started via
`qiime decontam prevalence --help`
