# Partition Quality
Quality scores to evaluate network partitions

(Partial) Implementation of the measures listed in

```
Yang, Jaewon, and Jure Leskovec. "Defining and evaluating network communities based on ground-truth." Knowledge and Information Systems 42.1 (2015): 181-213.
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

# Dependencies
- Python 2.7
- networkx
- numpy
