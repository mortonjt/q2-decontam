#!/usr/bin/env Rscript
cat(R.version$version.string, "\n")

library(decontam)


args <- commandArgs(TRUE)
biom.name <- args[[1]]
map.name <- args[[2]]
blank.column <- args[[3]]
batch.column <- args[[3]]
output <- args[[4]]

table <-read.table(biom.name, check.names=FALSE, row.names=1)
map <- read.csv(map.name, sep='\t', row.names=1)

# True if a negative control sample
neg2 <- MAP2$`blank.column`
batch <- as.factor(MAP2$`batch.column`)
ocp <- isContaminant(as.matrix(table), neg=neg2, threshold=0.1, batch=batch,
                     detailed=TRUE, normalize=TRUE, method='prevalence')
write.table(ocp, output)
