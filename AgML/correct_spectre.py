import os
import time
import numpy as np
import pandas as pd
from scipy.io import loadmat
from scipy.optimize import curve_fit
from tqdm import tqdm  # for the progress bar

def gauss1(x, a, b, c):
    return a / ((2 * np.pi * c) ** 0.5) * np.exp(-((x - b) ** 2) / (2 * c))

def gauss2(x, a1, b1, c1, a2, b2, c2):
    return (a1 * np.exp(-((x - b1) ** 2) / (2 * c1 ** 2)) +
            a2 * np.exp(-((x - b2) ** 2) / (2 * c2 ** 2)))

def main():
    mat = loadmat('./Data/NormFLEff.mat')
    FLEff = mat['FLEff']
    dirs = ["./Data/proposed_trials/NLP2"]
    fitS, fitE = 441, 800

    for directory in dirs:
        files = sorted(os.listdir(directory))
        files = [file for file in files if "M4" in file and "corrected" not in file]
        GPk = np.ones(len(files))  # All assume two peaks; change if needed

        print(f"Processing {len(files)} files in '{directory}'...")

        for ind in tqdm(range(len(files)), desc="Correcting spectra"):
            file = files[ind]
            path = os.path.join(directory, file)
            tmp = pd.read_csv(path, sep='\t').to_numpy()
            WLS = tmp[:, 0]
            bkg = np.mean(tmp[:35, 1])
            S = tmp[:, 1] - bkg

            EffS = np.where(FLEff[:, 0] == tmp[0, 0])[0][0]
            EffE = np.where(FLEff[:, 0] == tmp[-1, 0])[0][0]
            Eff = FLEff[EffS:EffE+1, 1]

            tmpC = S / Eff
            i1 = np.where(WLS == fitS)[0][0]
            i2 = np.where(WLS == fitE)[0][0]
            tmpCF = tmpC[i1:i2]
            tmpWLF = WLS[i1:i2]

            flag = 0
            try:
                if GPk[ind] != 1:
                    popt, _ = curve_fit(gauss1, tmpWLF, tmpCF, p0=[10000, 680, 3000])
                    yFit = gauss1(np.arange(fitS, 1001), *popt)
                    flag = 1
                else:
                    popt, _ = curve_fit(gauss2, tmpWLF, tmpCF, p0=[10000, 511, 1.5, 100000, 680, 100])
                    if popt[3] < 0:
                        raise ValueError("Negative amplitude")
                    yFit = gauss2(np.arange(fitS, 1001), *popt)
            except:
                popt, _ = curve_fit(gauss1, tmpWLF, tmpCF, p0=[10000, 511, 1.5])
                yFit = gauss1(np.arange(fitS, 1001), *popt)
                flag = 1

            WLFinal = np.arange(WLS[0], 1001)
            SFinal = tmpC

            filename_wo_ext = '.'.join(file.split('.')[:-1])
            corrected_txt_path = os.path.join(directory, filename_wo_ext + '_corrected.txt')
            np.savetxt(corrected_txt_path, np.column_stack((WLFinal, yFit)), delimiter='\t')

            if flag == 1:
                np.save(os.path.join(directory, file.split('.')[0] + '_corrected'), SFinal[i1:len(WLFinal)])

if __name__ == "__main__":
    main()
