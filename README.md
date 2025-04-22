# BioNano
![version](https://img.shields.io/badge/version-0.0.1-brightgreen)
[![paper](https://img.shields.io/badge/paper-arXiv-red)]()
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)

We present a machine learning–driven method for rapidly optimizing post-synthesis silver doping in CdSe nanoplatelets (NPLs). Using [Bayesian Optimization with In-Context Learning (BO-ICL)](https://github.com/ur-whitelab/BO-LIFT) on large language models, our approach directly integrates both continuous and categorical synthesis variables -- from dopant concentration to reaction temperature -- to predict and improve target photophysical properties. Specifically, we jointly optimize quantum yield and secondary photoluminescence peak area to capture the trade-off between emissive efficiency and spectral tunability. Compared to a Gaussian Process baseline, the LLM-based optimizer converges on higher-performing experimental protocols with fewer trials. Moreover, we illustrate interpretability via SHAP values, revealing that doping percentage, dopant mass, and NPL dimensions are the most influential factors in controlling the luminescence response. This one-step method underscores the promise of large language models to accelerate materials innovation and guide the rational design of doped NPLs.


Repository with the code base for the BioNano project under development at the University of Rochester.


## Preprocessing data

## GPRs with [Ax](https://ax.dev)

## SHAP Analysis


## References
