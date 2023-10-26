# AgML subproject from BioNano

## Filesystem

```bash
AgML
├── Data
│   ├── absorbance_data
│   ├── fluorescence_data
│   ├── processed_data.csv
│   ├── abs_spectra_data.csv
│   ├── fl_spectra_data.csv
│   ├── pool_chunk.{txt, pkl}
│   ├── pool_processed.{csv, txt, pkl}
│   ├── procedures.tsv
├── process_data.ipynb
├── predict.ipynb
```

- Data: Directory with all the raw and processed data
    - absorbance_data and fluorescence_data: raw data from the spectrometer
    - processed_data.csv: processed raw data. File with all the experiments, spectra and properties
    - abs_spectra_data.csv and fl_spectra_data.csv: processed dataset. Each row is a point in the spectra
    - pool_chunk.{txt, pkl}: pool created using the chunk procedure. txt is the prompts, pkl is the pickled pool
    - pool_processed.{csv, txt, pkl}: pool created by Jorge's calculations. csv is the dataframe, txt is the prompts, pkl is the pickled pool
    - procedures.tsv: procedures used to create the pool_processed
- process_data.ipynb: notebook used to process the raw data
- predict.ipynb: notebook used to carry the BO out