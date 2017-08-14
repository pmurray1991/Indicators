"""
An Indicator is one of hundreds of manual measurements tabulated monthly at a power plant.

This module provides classes for two types of indicator objects: CodedIndicator and NumberIndicator.
The goal is to bind behaviors (validation, display, etc) with the value of the indicator.

Your task is to design the factory data structure and implement the skeleton methods in the Indicator
classes. The application will load hundreds of indicators into the factory. These are the concrete
indicator types. As monthly timeseries data is processed by the application, thousands of indicator
objects will be created and managed.

The file tests/unittests/test_lh_Indicator.py contains sample data and skeleton's of the first unittests.
The sample data has two instances of concrete indicator types (from the hundreds references above).

The deliverable for this task will be demonstrating behavior through unittests. You should deliver
pull requests against the indicator branch of the PyLight repository. Robin Wang will be your POC for
GitHub logistics.

As the project evolves, I expect we will expand unittests. You should propose variations. We will add new
ones as new features emerge.
"""


class IndicatorBase:
    """
    Base class for indicator types
    """
    def __init__(self, value):
        self._value = value

    @property
    def name(self):
        return self._name

    @property
    def display_name(self):
        return self._display_name

    @property
    def source(self):
        return self._source

    @property
    def description(self):
        return self._description

    def __hash__(self):
        """ hash on name"""
        return hash(self.name)

    def __eq__(self, other):
        """ eq when name is equal, sort in alphabetical order"""
        return self.name == other.name



class CodedIndicator(IndicatorBase):
    """
    Indicator with a coded value.

    A coded value is a member of a list. The list is
    defined in the range attribute of the yml. For example:
    range:
      - red
      - green
      - yellow

    """
    def __init__(self, *args):
        super().__init__(*args)
        self._display_name = args[0]['display_name']
        self._name = args[0]['name']
        self._source = args[0]['source']
        self._range = args[0]['range']
        self._map = args[0]['map']
        self._description = args[0]['description']

    @property
    def range(self):
        """present list of codes"""
        return self._range

    @property
    def map(self):
        """present map as list of dicts"""
        return self._map

    def in_range(self, value):
        """
        value in inclusive range
        :return bool:
        """

        if value in self.range:
            return True
        else:
            return False

    #@property
    def value(self,value):
        """ get mapped value """
        for x in self.map:
            if x[value]:
                return x[value]

    def __str__(self):
        return "Name: %s\nDisplay Name: %s\nSource: %s\nDescription: %s\nrange: %s\nmap: %s" \
               % (self.name, self.display_name, self.source, self.description,self.range,self.map)



    def __repr__(self):
        return "<{0}:name={1}, display_name={2},source={3}, description={4}, range={5},map={6}>".format(self.__class__.__name__,self.name, self.display_name, self.source, self.description,self.range,self.map)


class NumberIndicator(IndicatorBase):
    """
    Indicator is numeric value

    The value under the range key of the yml is a dictionary.
    """

    def __init__(self, *args):
        super().__init__(*args)
        self._display_name = args[0]['display_name']
        self._name = args[0]['name']
        self._source = args[0]['source']
        self._range = args[0]['range']
        self._map = args[0]['map']
        self._description = args[0]['description']

    @property
    def range(self):
        """
        indicator in inclusive range
        :return bool:
        """
        return self._range

    @property
    def map(self):
        """ list of mappings as dicts"""
        return self._map

    def in_range(self, value):
        """
        indicator value in inclusive range
        :return bool:
        """
        if value in range(self.range['inclusive_floor'], self.range['inclusive_ceiling']):
            return True
        else:
            return False

    def is_normal(self,value):
        """
        indicator value inside statistical variance
        :return bool:
        """
        if (float(self.range['mean'])-float(self.range['std'])) <= value \
                <= (float(self.range['mean'])+float(self.range['std'])):
            return True
        else:
            return False

    def __str__(self):
        return "Name: %s\nDisplay Name: %s\nSource: %s\nDescription: %s\nrange: %s\nmap: %s" \
               % (self.name, self.display_name, self.source, self.description, self.range, self.map)

    def __repr__(self):
        return "<{0}:name={1}, display_name={2},source={3}, description={4}, range={5},map={6}>".format(self.__class__.__name__,self.name, self.display_name, self.source, self.description,self.range,self.map)


class IndicatorFactory:
    """
    Factory capable of manufacturing any Indicator configured.

    The factory is completely described under the indicators key in lighthouse.yml.
    """
    def __init__(self):
        """ Establish a factory to produce CodeIndicator and NumberIndicator objects """
        self.indicator_dictionary = {}

    def add(self, indicator_config):
        """
        Register an indicator configuration

        This method interrogates indicator_config to decide type, either
        CodeIndicator or NumberIndicator.
            CodeIndicator has a list under range
            NumberIndicator has a dict under range

        This method must be robust at checking for all attributes.
        Also, be sure to overwrite duplicates.

        Raise IndicatorConfigError if indicator_config cannot be added for any reason.

        :return: 201 on success

        """
        try:
            if isinstance(indicator_config['range'],list):
                cI = CodedIndicator(indicator_config)
                self.indicator_dictionary[cI.name] = cI
            elif isinstance(indicator_config['range'],dict):
                numInd = NumberIndicator(indicator_config)
                self.indicator_dictionary[numInd.name] = numInd
            else:
                raise Exception("IndicatorConfigError")
        except:
            raise Exception("IndicatorConfigError")

        if indicator_config:
            return 201

    def indicator(self, indicator_name, indicator_value):
        """ Fabricate a concrete indicator from an indicator spec """
        if indicator_name and indicator_value:
            if indicator_name in self.indicator_dictionary.keys():
                return self.indicator_dictionary[indicator_name]
