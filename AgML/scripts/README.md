## Scripts

Scripts that replicate what is done in the notebooks for preprocessing and analysis of new experimental files.

- correct_spectre.py:  Script used to correct the experimental fluorescent files.
    1) It removes background noise,
    2) It corrects with the corresponding correction factor
    3) Smooths the curves with gaussian approaximation
       
- get_objective_values.py: Script used to get the labels for optimization

- make_bo_prompts.py: Script used to make prompts from the experimental features
