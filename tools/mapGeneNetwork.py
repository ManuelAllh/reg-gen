import sys

from rgt.GeneSet import GeneSet
from rgt.MotifSet import MotifSet

# motif databases

jaspar = '/home/ivan/projects/reg-gen/data/motifs/jaspar_vertebrates.mtf'
uniprobe = '/home/ivan/projects/reg-gen/data/motifs/uniprobe_primary.mtf'
internal = '/home/ivan/projects/reg-gen/data/motifs/internal.mtf'

# files with p-values
enrichment_files = sys.argv[1]
# tfs to include in the network
factor_file = sys.argv[2]
# search mode to map factors to motifs (exact or inexact)
search_mode = sys.argv[3]
# pvalue cuttoff for definition of active factors
pvalue = float(sys.argv[4])
# output file
out = sys.argv[5]
# genes to be used as potential targets 
targets = None
if len(sys.argv) > 6:
    targets_file = sys.argv[6]
    # reading targets
    targets = GeneSet("genes")
    targets.read(targets_file)

# starting motif databases
motif_set = MotifSet()
if len(sys.argv) > 7:
    motif_set.read_mtf([sys.argv[7]])
else:
    motif_set.read_mtf([jaspar, uniprobe, internal])

# reading genes 
factors = GeneSet("genes")
factors.read(factor_file)

motif_set.read_enrichment(enrichment_files, pvalue)
motif_set.write_network(factors, search_mode, out, targets, pvalue)
