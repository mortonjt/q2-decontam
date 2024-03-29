import os
import qiime2
import pandas as pd
import numpy as np
import subprocess
import biom
import tempfile


def run_commands(cmds, verbose=True):
    if verbose:
        print("Running external command line application(s). This may print "
              "messages to stdout and/or stderr.")
        print("The command(s) being run are below. These commands cannot "
              "be manually re-run as they will depend on temporary files that "
              "no longer exist.")
    for cmd in cmds:
        if verbose:
            print("\nCommand:", end=' ')
            print(" ".join(cmd), end='\n\n')
        proc = subprocess.run(cmd, check=True)


def prevalence(table : biom.Table,
               blank : qiime2.CategoricalMetadataColumn,
               batch : qiime2.CategoricalMetadataColumn=None,
               min_samples : int=2) -> pd.DataFrame:

    filter_f = lambda v, i, m: np.sum(v>0) >= min_samples
    table.filter(filter_f, axis='observation')
    table = pd.DataFrame(np.array(table.matrix_data.todense()).T,
                         index=table.ids(),
                         columns=table.ids(axis='observation'))
    blank = blank.to_series()
    if batch is None:
        batch = pd.Series([0] * len(blank), index=blank.index)
    batch = batch.to_series()
    metadata = pd.DataFrame({'blank': blank, 'batch': batch})
    with tempfile.TemporaryDirectory() as temp_dir_name:
        # temp_dir_name = '.'
        biom_fp = os.path.join(temp_dir_name, 'input.tsv.biom')
        map_fp = os.path.join(temp_dir_name, 'input.map.txt')
        summary_fp = os.path.join(temp_dir_name, 'output.summary.txt')

        # Need to manually specify header=True for Series (i.e. "meta"). It's
        # already the default for DataFrames (i.e. "table"), but we manually
        # specify it here anyway to alleviate any potential confusion.
        table.to_csv(biom_fp, sep='\t', header=True)
        metadata.to_csv(map_fp, sep='\t', header=True)

        cmd = ['decontam_prevalence.R', biom_fp, map_fp,
               'blank', 'batch', summary_fp]
        cmd = list(map(str, cmd))
        try:
            run_commands([cmd])
        except subprocess.CalledProcessError as e:
            raise Exception("An error was encountered while running decontam"
                            " in R (return code %d), please inspect stdout"
                            " and stderr to learn more." % e.returncode)
        pvals = pd.read_table(summary_fp)
        idx = pvals['p.prev'] > 0.1
        filtered_table = table.loc[:, idx]
        # filtered_table = biom.Table(
        #     table.values.T,
        #     list(table.columns),
        #     list(table.index)
        # )
        return filtered_table
