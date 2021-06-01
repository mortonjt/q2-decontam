import importlib
import qiime2.plugin
import qiime2.sdk
from qiime2.plugin import (Str, Properties, Int, Float,  Metadata, Bool,
                           MetadataColumn, Categorical, Numeric)
from q2_types.feature_table import FeatureTable, Frequency
from q2_types.feature_data import FeatureData, Differential
from q2_decontam._method import prevalence


plugin = qiime2.plugin.Plugin(
    name='decontam',
    version="0.1.0",
    website="https://github.com/mortonjt/q2-decontam",
    citations=[],
    short_description=('Plugin for contaminant removal. '),
    description=('This is a QIIME 2 plugin for removing contaminants.'),
    package='q2-decontam')


plugin.methods.register_function(
    function=prevalence,
    inputs={'table': FeatureTable[Frequency]},
    parameters={
        'blank': MetadataColumn[Categorical],
        'batch': MetadataColumn[Categorical],
        'min_samples' : Int
    },
    outputs=[('filtered_table', FeatureTable[Frequency])],
    input_descriptions={
        "table": "Input table of counts.",
    },
    output_descriptions={
        'filtered_table': ('Table with contaminants removed.')
    },
    parameter_descriptions={
        'blank': 'Specifies if the sample is a blank or not.',
        'batch': 'Specifies different sequencing batches.',
        'min_samples': 'Minimum number of samples to keep',
    },
    name='Prevalance filter',
    description=("Removes contaminants based on blanks."),
    citations=[]
)
