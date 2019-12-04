""" I have no idea what this program do but I am going to figure this out
    So , help me Machine God"""

import math


class PhaseState:

    def __init__(self, temperature, pressure, mol_flow_initial, mol_frac_initial, pressure_crit, temperature_crit, omega, ro, mr, additional_parameters):

        _gas_molar_flow = 0 # molar flow of gaseous products, mol./h
        _liquid_molar_flow = 0 # molar flow of liquid products, mol./h
        _cut_molar = 0 # mole fraction of distillate
        _cut_smoothing = False

        _temperature = temperature
        _pressure = pressure
        _mol_flow_initial = mol_flow_initial  # molar flow of feed, mol./h

        _num_of_components = len(mol_frac_initial)
        if _num_of_components != len(pressure_crit) or _num_of_components != len(temperature_crit) or _num_of_components != len(omega):
            pass  # Here must error message raise, but idk how to do it yet

        _mol_frac_initial = mol_frac_initial.copy()  # molar fractions of components in flow of feed, %
        _mol_frac_liquid = []  # molar fractions of components in flow of liquid products, %
        _mol_frac_gaseous = []  # molar fractions of components in flow of gaseous products, %
        for i in range(_num_of_components):
            _mol_frac_liquid.append(0)
            _mol_frac_gaseous.append(0)

        _pressure_crit = pressure_crit.copy()  # critical pressures of each components, C
        _temperature_crit = temperature_crit.copy()  # critical temperatures of each components, Pa
        _omega = omega.copy()  # some acentric factors of components ???
        _ro = ro.copy()  # some acentric factors of components ???
        _mr = mr.copy()  # some acentric factors of components ???

        _parameters_coef = dict.fromkeys(['aTFP', 'bTFP'])
        if additional_parameters[0] > -1:  # reloading of parameters
            _parameters_coef['aTFP'] = additional_parameters[1]
            _parameters_coef['bTFP'] = additional_parameters[2]

    def wilson_constant_calculation(self):
        """
        Wilson equation for the prediction of vapour-liquid equilibrium for multicomponent mixtures
        i.e., calculates constants of equilibrium
        """

        _pressure_bar = self._pressure / 10**5  # convert Pa to bar
        _temperature_kelvin = self._temperature + 273  # convert C to K

        _pressure_partial = []  # partial pressures of components in the mixture
        _coefficient_distribution = []  # distribution coefficients of components

        for i in range(self._num_of_components):
            _pressure_partial.append(self._pressure_crit[i] * math.exp(5.372697 * (1 + self._omega[i]) * (1 - self._temperature_crit[i] * self._parameters_coef['bTFP'] / self._temperature)))
            _coefficient_distribution.append(_pressure_partial[i] / _pressure_bar)

    def phase_selector(self):
        """
        Determines in which condition the mixture is:
        0 - there are 2 phases;
        1 - there is only one phase and its liquid;
        2 - there is only one phase and its gaseous;
        3 - the mixture is in its boiling point
        4 - the mixture is in its dew point
        :return: int
        """
