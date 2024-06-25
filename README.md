# Fairness in a real social network
This is a project for measuring fairness in ranking algorithms results. It was developed for the course "D6 - Online Social Networks and Media" of my MSc degree under the supervision of [E. Pitoura](https://www.cs.uoi.gr/~pitoura/) and [P. Tsaparas](https://www.cs.uoi.gr/~tsap/). A full description of the process followed and results can be found in [REPORT.pdf](/REPORT.pdf) file. 

## Notes
- [requirements.txt](/requirements.txt) file can be used to re-create anaconda environment with the necessary dependencies.

## Contents
- [src/fairness_funcs.py](src/fairness_funcs.py): Fairness-related metrics calculations such as GINI coefficient or homophily
- [src/helper_funcs.py](src/helper_funcs.py): Graph preprocessing and I/O functions
- [gplus_analysis.ipynb](gplus_analysis.ipynb): Fairness analysis of Google+ ego-networks

## References
1. Tóth, G., Wachs, J., Di Clemente, R. et al. Inequality is rising where social network segregation interacts with urban topology. Nat Commun 12, 1143 (2021). https://doi.org/10.1038/s41467-021-21465-0
2. J. McAuley and J. Leskovec. Learning to Discover Social Circles in Ego Networks. NIPS, 2012. https://snap.stanford.edu/data/ego-Gplus.html
