import pprint
import yaml
from unittest import TestCase, skip

from indicator_factory import IndicatorBase, IndicatorFactory, CodedIndicator, NumberIndicator

class LighthouseIndicatorTestCase(TestCase):
    def setUp(self):

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
      upper_quartile: '1100'
      lower_quartile: '500'
      median: '800'
    map:
      - null: None
      - NA: None
"""
        self.lh_config = yaml.load(yaml_indicators)

    def tearDown(self):
        pass

    def test_load_factory(self):
        indicator_factory = IndicatorFactory()
        for indicator_config in self.lh_config['indicators']:
            pprint.pprint(indicator_config)
            response = indicator_factory.add(indicator_config)
            self.assertEqual(response, 201)

    #@skip('todo')
    def test_create_indicator(self):
        indicator_factory = IndicatorFactory()
        for indicator_config in self.lh_config['indicators']:
            pprint.pprint(indicator_config)
            indicator_factory.add(indicator_config)

        indicator = indicator_factory.indicator('chem.cfam.cei.condition.1..action.levels..monthly', .45)
        self.assertIn(indicator.name,indicator_factory.indicator_dictionary.keys())
        self.assertIsInstance(indicator, IndicatorBase)
        self.assertIsInstance(indicator, NumberIndicator)
        self.assertEquals(indicator.is_normal(.45),True)
        self.assertFalse(indicator.is_normal(.427))

        indicator = indicator_factory.indicator('chem.cfam.aux.system.chemistry.index', 'green')
        self.assertIn(indicator.name, indicator_factory.indicator_dictionary.keys())
        self.assertIsInstance(indicator, IndicatorBase)
        self.assertIsInstance(indicator, CodedIndicator)
        self.assertTrue(indicator.in_range('green'))
        self.assertEquals(indicator.value('green'), '1')
