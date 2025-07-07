import os
import pandas as pd
from tqdm import tqdm

# You must define these functions elsewhere or import them
from utill_functions import smooth_spectrum, get_area_under_peaks, process_spectrum

# Paths
fluorescence_dir = "../Data/proposed_trials/NLP"
absorbance_dir = "../Data/proposed_trials/NLP"

# Get list of fluorescence and absorbance files
fluo_files = sorted([f for f in os.listdir(fluorescence_dir) if f.endswith(".txt") and "corrected" in f])
abs_files = sorted([f for f in os.listdir(absorbance_dir) if f.endswith(".csv")])


# Iterate with progress bar
for i, (txt, csv) in enumerate(tqdm(zip(fluo_files, abs_files), total=len(fluo_files), desc="Processing files")):
    try:
        # Process fluorescence data
        with open(os.path.join(fluorescence_dir, txt), 'r', encoding='utf-8-sig') as f:
            lines = f.readlines()
            x = [float(line.split()[0]) for line in lines]
            y = [float(line.split()[1]) for line in lines]
            y = [yi - min(y) for yi in y]
            f_x, f_y = smooth_spectrum(x, y)
            fl_int_norm = [yi / max(f_y) for yi in f_y]
            fl_auc_total = get_area_under_peaks(f_x, f_y)
            peaks, areas = process_spectrum(f_x, f_y, norm_area=fl_auc_total)

        # Process absorbance data
        abs_path = os.path.join(absorbance_dir, csv)
        if os.path.exists(abs_path):
            df = pd.read_csv(abs_path)
            df.sort_values(by=['nm'], inplace=True)
            x, y = df['nm'].astype(float).tolist(), df[' A'].astype(float).tolist()
            x, y = smooth_spectrum(x, y)
            abs_int_norm = [yi / max(y) for yi in y]
            abs_s = df[df['nm'] == 430][' A'].values[0]

            # Reference constants
            fl_r, abs_r, n_r = 8272505, 0.129734, 1.3611
            if "M5" in txt or "M6" in txt:
                fl_r, abs_r, n_r = 9453221.02, 0.039083, 1.3611
            elif "M7" in txt:
                fl_r, abs_r, n_r = 8930003.417, 0.044838, 1.3611

            # Sample constants
            fl_s, n_s = fl_auc_total, 1.375
            qy = 0.53 * (fl_s / fl_r) * (abs_r / abs_s) * (n_s / n_r) ** 2

            # # Optional plotting
            # sd = get_sd_object(f_x, f_y)
            _title = f"Trial: {i + 1} \nQY={qy:.2f}  AUC2= {areas[1]:.2f}  F={qy * areas[1]:.2f}"
            # plot_spectra(sd, title=_title)

            print(txt, "QY:", round(qy, 2), "AUC2:", round(areas[1], 2), "f:", round(qy * areas[1], 2))

    except Exception as e:
        print(f"Exception at {txt} and {csv}: {e}")
        continue


#now the same but with Data/proposed_trials/BO

# Get list of fluorescence and absorbance files
fluorescence_dir = "../Data/proposed_trials/BO"
absorbance_dir = "../Data/proposed_trials/BO"
# Get list of fluorescence and absorbance files
fluo_files = sorted([f for f in os.listdir(fluorescence_dir) if f.endswith(".txt") and "corrected" in f])
abs_files = sorted([f for f in os.listdir(absorbance_dir) if f.endswith(".csv")])


print("Fluorescence files:", fluo_files)
print("Absorbance files:", abs_files)
# Iterate with progress bar
for i, (txt, csv) in enumerate(tqdm(zip(fluo_files, abs_files), total=len(fluo_files), desc="Processing files")):
    try:
        # Process fluorescence data
        with open(os.path.join(fluorescence_dir, txt), 'r', encoding='utf-8-sig') as f:
            lines = f.readlines()
            x = [float(line.split()[0]) for line in lines]
            y = [float(line.split()[1]) for line in lines]
            y = [yi - min(y) for yi in y]
            f_x, f_y = smooth_spectrum(x, y)
            fl_int_norm = [yi / max(f_y) for yi in f_y]
            fl_auc_total = get_area_under_peaks(f_x, f_y)
            peaks, areas = process_spectrum(f_x, f_y, norm_area=fl_auc_total)

        # Process absorbance data
        abs_path = os.path.join(absorbance_dir, csv)
        if os.path.exists(abs_path):
            df = pd.read_csv(abs_path)
            df.sort_values(by=['nm'], inplace=True)
            x, y = df['nm'].astype(float).tolist(), df[' A'].astype(float).tolist()
            x, y = smooth_spectrum(x, y)
            abs_int_norm = [yi / max(y) for yi in y]
            abs_s = df[df['nm'] == 430][' A'].values[0]

            # Reference constants
            fl_r, abs_r, n_r = 8272505, 0.129734, 1.3611
            if "M5" in txt or "M6" in txt:
                fl_r, abs_r, n_r = 9453221.02, 0.039083, 1.3611
            elif "M7" in txt:
                fl_r, abs_r, n_r = 8930003.417, 0.044838, 1.3611

            # Sample constants
            fl_s, n_s = fl_auc_total, 1.375
            qy = 0.53 * (fl_s / fl_r) * (abs_r / abs_s) * (n_s / n_r) ** 2

            # # Optional plotting
            # sd = get_sd_object(f_x, f_y)
            _title = f"Trial: {i + 1} \nQY={qy:.2f}  AUC2= {areas[1]:.2f}  F={qy * areas[1]:.2f}"
            # plot_spectra(sd, title=_title)

            print(txt, "QY:", round(qy, 2), "AUC2:", round(areas[1], 2), "f:", round(qy * areas[1], 2))

    except Exception as e:
        print(f"Exception at {txt} and {csv}: {e}")
        continue
