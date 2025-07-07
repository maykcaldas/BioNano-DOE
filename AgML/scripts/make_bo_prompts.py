import argparse
import numpy as np
import pandas as pd
from tqdm import tqdm
from itertools import product

# Constantes físicas
Length = [25.59635, 27.39105, 23.54675, 27.3818]     #Fill with current experimental values 
Width = [5.9023, 7.48505, 12.7644, 8.75165]   #Fill with current experimental values 
Thickness = 1.22
Unit_volume = 0.221445125
epsilon = 31947800
Cd_atoms_per_unit_volume = 4
Ag_acet_concentration = [0.006, 0.0007]
Dilution_factor_for_OD = 100
Ag_percentage_doping = np.arange(0.01,10,0.05)
Optical_density_at_dilution_factor_100 = [0.15, 0.3]
Aliquote = [0.25, 0.5]
Mass_Ag_acet = [3.5, 7.8, 14]
Ag_Acet_mw = 166.91
Temperature = [0, 25, 50]
Time = [10, 60, 180]

def make_prompt_from_features(features,version=0):    
    if version == 0:
        prompt_template = "Stock nanoplatelets have dimensions {Dimension1_nm} nm by {Dimension2_nm} nm and the optical density of 100x hexanes dilution of stock is {Dilution_pct}% " \
                        "recorded at 512nm. {Nano_stock_vol_mL} mL nanoplatelets stock is diluted 7x by hexanes using {Diluted_vol_mL} mL for each trial of doping. " \
                        "Silver acetate solution of {AgConc_M} M is made with {AgMass_mg} mg of silver acetate in {MeOH_vol_mL} mL of MeOH and {H2O_vol_mL} mL of water. " \
                        "{Doping_pct} % Ag doping requires {AgSol_uL} uL of silver doping solution, respectively. " \
                        "The reaction was performed at 1000 rpm for {Time_min} minutes at {Temperature_C} oC. " \
                        "Fluorescence of each doped sample was collected as a 30x dilution with hexanes."
    elif version == 1:
        prompt_template = "Stock nanoplatelets have dimensions {Dimension1_nm} nm by {Dimension2_nm} nm and the optical density of 100x hexanes dilution of stock is {Dilution_pct}% "\
                        "recorded at 512nm. {Nano_stock_vol_mL} mL nanoplatelets stock is diluted 7x by hexanes using {Diluted_vol_mL} mL for each trial of doping. "\
                        "Silver acetate solution of {AgConc_M} M is made with {AgMass_mg} mg of silver acetate in {MeOH_vol_mL} mL of MeOH and {H2O_vol_mL} mL of water. "\
                        "{Doping_pct} % Ag doping requires {AgSol_uL} uL of silver doping solution, respectively. "\
                        "The reaction was performed at 1000 rpm for {Time_min} minutes at {Temperature_C} oC. "\
                        "Fluorescence of each doped sample was collected as a 30x dilution with hexanes." \
                        "Knowing that: 1) an increase in silver doping will increase the fluorescence SECONDARY PEAK AREA, "\
                        "and 2) QUANTUM YIELD decreases as Ag doping increases, although some reports indicate that theres a slight increase before decreasing."
    elif version == 2:
        prompt_template = "Stock nanoplatelets have dimensions {Dimension1_nm} nm by {Dimension2_nm} nm and the optical density of 100x hexanes dilution of stock is {Dilution_pct}% "\
                        "recorded at 512nm. {Nano_stock_vol_mL} mL nanoplatelets stock is diluted 7x by hexanes using {Diluted_vol_mL} mL for each trial of doping. "\
                        "Silver acetate solution of {AgConc_M} M is made with {AgMass_mg} mg of silver acetate in {MeOH_vol_mL} mL of MeOH and {H2O_vol_mL} mL of water. "\
                        "{Doping_pct} % Ag doping requires {AgSol_uL} uL of silver doping solution, respectively. "\
                        "The reaction was performed at 1000 rpm for {Time_min} minutes at {Temperature_C} oC. "\
                        "Fluorescence of each doped sample was collected as a 30x dilution with hexanes." \
                        "Knowing that: 1) an increase in silver doping will increase the fluorescence SECONDARY PEAK AREA, "\
                        "and 2) QUANTUM YIELD decreases as Ag doping increases, although some reports indicate that theres a slight increase before decreasing."
    elif version == 3:
        counts = float(features["Dimension1_nm"]) * float(features["Dimension2_nm"]) * 8.8968 * 4 / 0.221448125
        Dimension1_nm = features["Dimension1_nm"]
        Dimension2_nm = features["Dimension2_nm"]
        Dilution_pct = float(features["Dilution_pct"])
        prompt_template = f"Stock nanoplatelets (NPL) have dimensions {Dimension1_nm} nm by {Dimension2_nm}, which gives a total Cd count per NPL as {counts} "\
                        f"nm and the optical density of 100x hexanes dilution of stock is {Dilution_pct}% recorded at 512nm, resulting in a theoretical NPL concentration of {31900000/Dilution_pct} M. "\
                        "{Nano_stock_vol_mL} mL nanoplatelets stock is  diluted 7x by hexanes using {Diluted_vol_mL} mL for each trial of doping. "\
                        "Silver acetate solution of {AgConc_M} M is made with {AgMass_mg} mg of silver acetate in {MeOH_vol_mL} mL of MeOH and {H2O_vol_mL} mL of water. "\
                        "{Doping_pct} % Ag doping requires {AgSol_uL} uL of silver doping solution, respectively. "\
                        "The reaction was performed at 1000 rpm for {Time_min} minutes at {Temperature_C} oC. Fluorescence of "\
                        "each doped sample was collected as a 30x dilution with hexanes."
        
    elif version == 4:
        counts = float(features["Dimension1_nm"]) * float(features["Dimension2_nm"]) * 8.8968 * 4 / 0.221448125
        Dilution_pct = float(features["Dilution_pct"])
        prompt_template = "Experiment Overview: Stock nanoplatelets (NPL) have dimensions {Dimension1_nm} nm by {Dimension2_nm} nm, resulting "\
                        f"in an estimated Cd count per NPL of {counts}. "\
                        f"The optical density of a 100x hexanes dilution of stock is {Dilution_pct}% at 512 nm, yielding a theoretical NPL concentration of {31900000/Dilution_pct} M. "\
                        "{Nano_stock_vol_mL} mL nanoplatelets stock is diluted 7x in hexanes to reach {Diluted_vol_mL} mL for each doping trial. Silver acetate solution ({AgConc_M} M) "\
                        "is prepared using {AgMass_mg} mg of silver acetate in {MeOH_vol_mL} mL MeOH and {H2O_vol_mL} mL water."\
                        "Objective: This experiment investigates the relationship between Ag doping and fluorescence characteristics. Specifically: "\
                        "An increase in silver doping typically elevates the secondary peak area of fluorescence. "\
                        "Quantum yield generally decreases with Ag doping, though slight initial increases are reported."
    elif version == 5:
        prompt_template = "Stock nanoplatelets have dimensions {Dimension1_nm} nm by {Dimension2_nm} nm and the optical density of 100x hexanes dilution of stock is {Dilution_pct}% "\
                        "recorded at 512nm. {Nano_stock_vol_mL} mL nanoplatelets stock is diluted 7x by hexanes using {Diluted_vol_mL} mL for each trial of doping. "\
                        "Silver acetate solution of {AgConc_M} M is made with {AgMass_mg} mg of silver acetate in {MeOH_vol_mL} mL of MeOH and {H2O_vol_mL} mL of water. "\
                        "{Doping_pct} % Ag doping requires {AgSol_uL} uL of silver doping solution, respectively. "\
                        "The reaction was performed at 1000 rpm for {Time_min} minutes at {Temperature_C} oC. "\
                        "Fluorescence of each doped sample was collected as a 30x dilution with hexanes." \
                        "Knowing that: 1) an increase in silver doping will increase the fluorescence SECONDARY PEAK AREA, "\
                        "2) QUANTUM YIELD decreases as Ag doping increases, although some reports indicate that theres a slight increase before decreasing, "\
                        "and 3) increasing the MeOH and Water quantities, which are incompatible solvents for the NPLs in hexanes, increases the solubility of Ag but also negatively impacts the QY of NPLs"
        
        
    #check if features are as dataframe, change to kwargs
    if isinstance(features, np.ndarray):
        features = features.tolist()
        return prompt_template.format(**features)
    features = features.to_dict()
    return prompt_template.format(**features)

def generate_feature_combinations():
    depurated_L_w_combs = []
    areas = []
    for L, W in zip(Length, Width):
        if L * W not in areas:
            areas.append(L * W)
            depurated_L_w_combs.append((L, W))

    data = { 'Dimension1_nm': [], 'Dimension2_nm': [],  'Dilution_pct': [], 'Nano_stock_vol_mL': [], 
            'Diluted_vol_mL': [], 'AgConc_M': [], 'AgMass_mg': [], 'MeOH_vol_mL': [], 
            'H2O_vol_mL': [], 'Doping_pct': [], 'AgSol_uL': [], 'Temperature_C': [], 'Time_min': [] }

    total_iterations = len(depurated_L_w_combs) * len(Optical_density_at_dilution_factor_100) * len(Aliquote) * len(Ag_acet_concentration) * len(Mass_Ag_acet) * len(Ag_percentage_doping)

    with tqdm(total=total_iterations) as pbar:
        for OD in Optical_density_at_dilution_factor_100:
            for NSV in Aliquote:
                for AAC in Ag_acet_concentration:
                    for AM in Mass_Ag_acet:
                        for DP in Ag_percentage_doping:
                            for L, W in depurated_L_w_combs:
                                pbar.update(1)
                                Unique_unit_areas = L * W
                                Unique_unit_volumes = Unique_unit_areas * Thickness
                                Unique_number_qd = Unique_unit_volumes / Unit_volume
                                Concentration = (OD / epsilon) * Dilution_factor_for_OD
                                Cd_mols = Concentration * Unique_number_qd * Cd_atoms_per_unit_volume * NSV / 1000
                                Ag_mols_needed = Cd_mols * DP / 100
                                Vol_Ag_acet_needed = Ag_mols_needed / AAC * 1e6
                                Ag_total_sol_volume = (AM / Ag_Acet_mw) / AAC
                                Me_OH_vol = Ag_total_sol_volume * 5 / 7
                                Water_vol = Ag_total_sol_volume * 2 / 7

                                for T in Temperature:
                                    for t in Time:
                                        data['Dimension1_nm'].append(L)
                                        data['Dimension2_nm'].append(W)
                                        data['Dilution_pct'].append(OD)
                                        data['Nano_stock_vol_mL'].append(NSV)
                                        data['Diluted_vol_mL'].append(NSV * 7)
                                        data['AgConc_M'].append(AAC)
                                        data['AgMass_mg'].append(AM)
                                        data['MeOH_vol_mL'].append(Me_OH_vol)
                                        data['H2O_vol_mL'].append(Water_vol)
                                        data['Doping_pct'].append(DP)
                                        data['AgSol_uL'].append(Vol_Ag_acet_needed)
                                        data['Temperature_C'].append(T)
                                        data['Time_min'].append(t)
    return pd.DataFrame(data)

def main():
    parser = argparse.ArgumentParser(description='Generate a pool of prompts for Bayesian optimization.')
    parser.add_argument('--num_samples', type=int, default=100, help='Number of prompts to generate.')
    parser.add_argument('--prompt_version', type=int, default=0, help='Prompt template version to use.')
    parser.add_argument('--output_file', type=str, default='pool.txt', help='Output .txt file to save prompts.')
    parser.add_argument('--input_features', type=str, help='Optional CSV file with precomputed features.')

    args = parser.parse_args()

    if args.input_features:
        df = pd.read_csv(args.input_features)
    else:
        df = generate_feature_combinations()
    print(len(df))
    df = df.sample(n=min(args.num_samples, len(df)), random_state=42).reset_index(drop=True)
    prompts = [make_prompt_from_features(df.iloc[i], args.prompt_version) for i in range(len(df))]

    with open(args.output_file, 'w') as f:
        for prompt in prompts:
            f.write(prompt + '\n')

    print(f"Generated {len(prompts)} prompts saved to {args.output_file}")

if __name__ == '__main__':
    main()
