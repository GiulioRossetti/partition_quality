# Partition Quality
Quality scores to evaluate network partitions

Implementation of the scoring functions listed in

```
Yang, Jaewon, and Jure Leskovec. 
"Defining and evaluating network communities based on ground-truth." 
Knowledge and Information Systems 42.1 (2015): 181-213.
```

## Implemented quality functions

### Scoring functions based on internal connectivity
- Internal Density
- Edges inside
- Average Degree
- Fraction over median degree (FOMD)
- Triangle Participation Ratio (TPR)

### Scoring functions based on external connectivity
- Expansion
- Cut Ratio

### Scoring functions that combine internal and external connectivity
- Conductance
- Normalized Cut
- Maximum-ODF (Out Degree Fraction)
- Average-ODF
- Flake-ODF

### Scoring function based on a network model
- Modularity

# Execution
```python
    python PartitionQuality.py nework_filename partition_filename
```

## Input files specification

### Graph file
Text file in edgelist format (one edge per row), semicolon as node separator.

Example:

```bash
node1;node2
node3;node1
node4;node5
node5;node2
```

### Community file
Text file in comlist format (one community per row), comma as node separator. 

Example:

```bash
node1,node2,node3,node4,node5
node6,node7,node8
node9,node10
node11,node12,node13,node14
```

# Dependencies
- Python 2.7
- networkx
- numpy
