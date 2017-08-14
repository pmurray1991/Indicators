import yaml

from indicator_factory import IndicatorBase, IndicatorFactory, CodedIndicator, NumberIndicator


yaml_indicators = \
"""
indicators:
  - name: chem.cfam.aux.system.chemistry.index
    display_name: CH Aux Sys Chem Index
    source: "A paragraph describing how the data is collected"
    description: "A paragraph defining the meaning of the indicator"
    range:
      - '1'
      - '2'
      - '3'
      - red
      - green
      - yellow
      - null
      - NA
    map:
      - green: '1'
      - yellow: '2'
      - red: '3'
      - null: None
      - NA: None
  - name: chem.cfam.cei.condition.1..action.levels..monthly
    display_name: CH CEI Cond 1 Actions
    source: "A paragraph describing how the indicator is collected"
    description: "A paragraph defining the meaning of the indicator"
    range:
      inclusive_floor: 0
      inclusive_ceiling: 1
      mean: .452
      std: .024
      precision : '{:.1%}'
    map:
      - null: None
      - NA: None
"""
lh_config = yaml.load(yaml_indicators)
infact = IndicatorFactory()
for x in lh_config['indicators']:
    infact.add(x)

# infact.add("test")
print(infact.indicatorDictionary['chem.cfam.cei.condition.1..action.levels..monthly'])
print()
print(infact.indicatorDictionary['chem.cfam.aux.system.chemistry.index'])
