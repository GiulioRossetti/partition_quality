# Partition Quality
Quality scores to evaluate network partitions

(Partial) Implementation of the measures listed in

```
Yang, Jaewon, and Jure Leskovec. 
"Defining and evaluating network communities based on ground-truth." 
Knowledge and Information Systems 42.1 (2015): 181-213.
```

## Implemented quality functions
- Modularity
- Conductance
- Normalized Cut
- Cut Ratio
- Internal Edge Density
- Average Internal Degree
- Fraction over median degree (FOAM)
- Expansion

# Execution
```python
    python PartitionQuality.py nework_filename partition_filename
```

## Input files specification

### Graph file
Text file in edgelist format (one edge per row), semicolon as node separator.

Example:

> node1;node2
> node3;node1
> node4;node5
> node5;node2

### Community file
Text file in comlist format (one community per row), comma as node separator. 

Example:

> node1,node2,node3,node4,node5
> node6,node7,node8
> node9,node10
> node11,node12,node13,node14

# Dependencies
- Python 2.7
- networkx
- numpy
