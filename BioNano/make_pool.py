import bolift
import itertools
import cloudpickle

import os
os.environ['OPENAI_API_KEY'] = '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'

possible_mutations = ['DhyaA', 'DhydA', 'DhyaB', 'DcymA', 'DmtrA', 'DomcA', 'DmtrC']

shewanellas = ['WT']
for k in itertools.combinations(possible_mutations, 2):
  shewanellas.append("".join(k))
for k in itertools.combinations(possible_mutations, 3):
  shewanellas.append("".join(k))


props = {
  'SH_mutation': shewanellas,
  'SH_initial_conc': [0.05],
  'QD_material': ['CdSe'],#['CdS', 'CdSe', 'CdTe'],
  'QD_conc': [0.5, 1],
  'QD_Size': [510, 520, 535],
  'QD_Shape': ['spheres'], #, 'rods', 'palettes'],
  'QD_Surface': ["MPA (3-mercaptopropionic acid)", "GSH (glutathione)", "Cys (cystine)"],
  'MD_medium': ['minimum'],
  'MD_growth': ['anaerobic'],
  'MD_nutrient': ['lactate'],
  'MD_nutrient_conc': [20],
  'MD_shaking': [100], #[50, 100, 150],
  'MD_temperature': [5, 25, 45],
  'MD_pH': [7],
  'MD_light': [530],
  'MD_time': [1],
}


'''
The proposed experimental procedure is illustraded below:

WT Shewanella oneidensis MR-1 (inital OD600 0.05) were cultured with 1.0uM cadmium selenide quantum dots capped with 3-mercaptopropionic acid (MPA) in an
anaerobic minimal medium solution containing 20 mM lactate at 25 C. Cultures were irridated with 530nm LEDs for 1 week to yield 1.0 umol +/- 0.1 umol Hydrogen.
'''


pool_elements = []
for procedure in itertools.product(*props.values()):
  (SH_mutation,
  SH_initial_conc,
  QD_material,
  QD_conc,
  QD_Size,
  QD_Shape,
  QD_Surface,
  MD_medium,
  MD_growth,
  MD_nutrient,
  MD_nutrient_conc,
  MD_shaking,
  MD_temperature,
  MD_pH,
  MD_light,
  MD_time) = procedure
  scaffold = f"{SH_mutation} Shewanella oneidensis MR-1 (initial OD600 {SH_initial_conc}) were cultured with "\
             f"{QD_conc} uM {QD_material} quantum dots capped with {QD_Surface} "\
             f"in an {MD_growth} {MD_medium} medium solution containing {MD_nutrient_conc} mM {MD_nutrient} at {MD_temperature} ºC. " \
             f"Cultures were irradiated with {MD_light} nm LEDs for {MD_time} week."

  pool_elements.append(scaffold)

with open('pool.dat', 'w') as pool_file:
  pool_file.write('Procedure\n')
  pool_file.write('\n'.join(pool_elements))

print(len(pool_elements))

pool = bolift.Pool(pool_elements)

cloudpickle.dump(pool, open("pool.pkl", "wb"))