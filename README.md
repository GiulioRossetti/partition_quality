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
    import pquality
    scores = pquality.pquality_summary()
    print(scores['Indexes'])
    print(scores['Modularity'])
```

# Dependencies
- Python 3.x
- networkx>2.x
- numpy
