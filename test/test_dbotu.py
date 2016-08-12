import pytest
from dbotu import *

import numpy as np, pandas as pd, io
import scipy.stats, scipy.optimize
from Bio import SeqIO

@pytest.fixture
def caller():
    fasta_fh = io.StringIO("\n".join(['>seq1', 'AAAAAAA', '>seq2', 'AAATAAA', '>seq3', 'AATTTAA']))
    fasta_fh.seek(0)
    log_fh = io.StringIO()
    records = SeqIO.to_dict(SeqIO.parse(fasta_fh, 'fasta'))
    table = pd.DataFrame(np.array([[0, 10, 20], [0, 1, 2], [10, 0, 0]]), index=['seq1', 'seq2', 'seq3'], columns=['sample1', 'sample2', 'sample3'])
    return DBCaller(table, records, word_size=3, max_dist=15, min_fold=0.0, threshold_pval=0.001, log=log_fh)

def test_seq_abunds(caller):
    assert all(caller.seq_abunds == pd.Series([30, 10, 3], index=['seq1', 'seq3', 'seq2']))

def test_empty_otus(caller):
    assert caller.otus == []

def test_process_one(caller):
    caller._process_record(caller.seq_abunds.index[0])
    assert caller.otus[0] == OTU('seq1', 'AAAAAAA', [0, 10, 20], 3)
    assert caller.otus[0].kmer_dict == {'AAA': 5}

def test_process_two(caller):
    for i in range(2):
        caller._process_record(caller.seq_abunds.index[i])

    assert caller.otus[0] == OTU('seq1', 'AAAAAAA', [0, 10, 20], 3)
    assert caller.otus[1] == OTU('seq3', 'AATTTAA', [10, 0, 0], 3)

def test_process_three(caller):
    for i in range(3):
        caller._process_record(caller.seq_abunds.index[i])

    # seq2 got merged into seq1
    assert caller.otus[0] == OTU('seq1', 'AAAAAAA', [0, 11, 22], 3)
    assert caller.otus[1] == OTU('seq3', 'AATTTAA', [10, 0, 0], 3)

def test_id_check():
    '''fail if there are IDs in the table that are not in the fasta'''
    fasta_fh = io.StringIO("\n".join(['>seq1', 'A', '>seq2', 'T']))
    fasta_fh.seek(0)
    records = SeqIO.to_dict(SeqIO.parse(fasta_fh, 'fasta'))
    table = pd.DataFrame(np.array([[0, 1], [2, 3], [4, 5]]), index=['seq1', 'seq2', 'seq3'], columns=['sample1', 'sample2'])
    with pytest.raises(RuntimeError):
        DBCaller(table, records, word_size=1, max_dist=15, min_fold=0.0, threshold_pval=0.001)
