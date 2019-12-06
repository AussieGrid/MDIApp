""" I have no idea what this program do but I am going to figure this out
    So , help me Machine God"""

import math


class PhaseState:

    def __init__(self, temperature, pressure, mol_flow_initial, mol_frac_initial, pressure_crit, temperature_crit, omega, density, molmass, additional_parameters):

        _gas_molar_flow = 0  # molar flow of gaseous products, mol./h {G}
        _liquid_molar_flow = 0  # molar flow of liquid products, mol./h {L}
        _cut_molar = 0  # mole fraction of distillate {e}
        _cut_smoothing = False  # {sglazh}

        _temperature = temperature  # {T}
        _pressure = pressure  # {P}
        _mol_flow_initial = mol_flow_initial  # molar flow of feed, mol./h {F}

        _num_of_components = len(mol_frac_initial)  # {NComp}
        if _num_of_components != len(pressure_crit) or _num_of_components != len(temperature_crit) or _num_of_components != len(omega):
            pass  # Here must error message raise, but idk how to do it yet

        _mol_frac_initial = mol_frac_initial.copy()  # molar fractions of components in flow of feed, % {zF}
        _mol_frac_liquid = []  # molar fractions of components in flow of liquid products, % {xL}
        _mol_frac_gaseous = []  # molar fractions of components in flow of gaseous products, % {yG}
        """ for i in range(_num_of_components):
                _mol_frac_liquid.append(0)
                _mol_frac_gaseous.append(0) """

        _pressure_crit = pressure_crit.copy()  # critical pressures of each components, Pa {Pc}
        _temperature_crit = temperature_crit.copy()  # critical temperatures of each components, C {Tc}
        _omega = omega.copy()  # some acentric factors of components ???
        _density = density.copy()  # density of components, kg/m3 {ro}
        _molmass = molmass.copy()  # molecular masses of components, g/mol. {Mr}

        _parameters_coef = dict.fromkeys(['aTFP', 'bTFP'])  # {ParamKoef}
        if additional_parameters[0] > -1:  # reloading of parameters {Param}
            _parameters_coef['aTFP'] = additional_parameters[1]
            _parameters_coef['bTFP'] = additional_parameters[2]

    def wilson_constant_calculation(self):
        """
        Wilson equation for the prediction of vapour-liquid equilibrium for multicomponent mixtures
        i.e., calculates constants of equilibrium
        """

        _pressure_bar = self._pressure / 10**5  # convert Pa to bar
        _temperature_kelvin = self._temperature + 273  # convert C to K

        _pressure_partial = []  # partial pressures of components in the mixture {Ps}
        _coefficient_distribution = []  # distribution coefficients of components {Kf}

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

        __s_1 = 0
        __s_2 = 0

        for i in range(self._num_of_components):
            __s_1 += self._mol_frac_initial[i] * self._coefficient_distribution[i]
            if self._coefficient_distribution[i] > 0:
                __s_2 += self._mol_frac_initial[i] / self._coefficient_distribution[i]

        if __s_1 > 1 and __s_2 > 1:
            return 0
        if __s_1 < 1:
            return 1
        if __s_2 < 1:
            return 2
        if __s_1 == 1:
            return 3
        if __s_2 == 1:
            return 4

    def raschford_rice(self, fc):
        """
        Calculation of the mole fraction of distillate using Raschford-Rice equation
        :param fc: the value is gathered from phase_selector
        """

        _fc = fc
        __eps = 10 ** -9

        def _rr_function(__e):
            __s = 0
            for i in range(self._num_of_components):
                if self._coefficient_distribution[i] > 0 and (1 + __e * (self._coefficient_distribution[i] - 1) != 0):
                    __s += self._mol_frac_initial[i] * (self._coefficient_distribution[i] - 1) / (1 + __e * (self._coefficient_distribution[i] - 1))
            return __s

        _a, _b = 0, 1

        if _fc == 3:
            _e = 0
        if _fc == 4:
            _e = 1

        if _rr_function(_a) * _rr_function(_b) < 0:
            while abs(_a + _b) > __eps:
                _e = (_a + _b) / 2
                if _rr_function(_a) * _rr_function(_b) > 0:
                    _a = _e
                else:
                    _b = _e
            _e = (_a + _b) / 2

        for i in range(self._num_of_components):
            self._mol_frac_liquid.append(self._mol_frac_initial[i] / (1 + _e * (self._coefficient_distribution[i] - 1)))
            self._mol_frac_gaseous.append(self._mol_frac_liquid[i] * self._coefficient_distribution[i])

        self._cut_molar = _e

    def calculation(self):
        """

        :return:
        """

        self.wilson_constant_calculation()
        _phase = self.phase_selector()
        _e_old = self._cut_molar

        if _phase == 0 or _phase == 3 or _phase == 4:
            self.raschford_rice(_phase)

            if self._cut_molar >= 1:
                self._cut_molar = 1
                for i in range(self._num_of_components):
                    self._mol_frac_liquid[i] = 0
                    self._mol_frac_gaseous[i] = self._mol_frac_initial[i]

            if self._cut_molar <= 0:
                self._cut_molar = 0
                for i in range(self._num_of_components):
                    self._mol_frac_liquid[i] = self._mol_frac_initial[i]
                    self._mol_frac_gaseous[i] = 0

        if _phase == 1:
            self._cut_molar = 0
            for i in range(self._num_of_components):
                    self._mol_frac_liquid[i] = self._mol_frac_initial[i]
                    self._mol_frac_gaseous[i] = 0

        if _phase == 2:
            self._cut_molar = 1
            for i in range(self._num_of_components):
                    self._mol_frac_liquid[i] = 0
                    self._mol_frac_gaseous[i] = self._mol_frac_initial[i]

        if self._cut_smoothing:
            if _e_old > self._cut_molar:
                self._cut_molar = _e_old - (_e_old - self._cut_molar) / 100
            if _e_old < self._cut_molar:
                self._cut_molar = _e_old + (_e_old - self._cut_molar) / 100

            if self._cut_molar > 1:
                self._cut_molar = 1

            if self._cut_molar < 0:
                self._cut_molar = 0

        self._gas_molar_flow = self._mol_flow_initial * self._cut_molar
        self._liquid_molar_flow = self._mol_flow_initial - self._gas_molar_flow

    def get_cut_value(self, _e):
        """

        :param _e: cut_molar
        :return:
        """

        if (_e == 0) or (_e == 1):
            return _e

        _avg_molmass_initial = 0  # average molecular mass of the components in feed stream {MrsrF}
        _avg_molmass_liquid = 0  # average molecular mass of the components in liquid products stream {MrsrL}
        _avg_molmass_gaseuos = 0  # average molecular mass of the components in gas products stream {MrsrG}

        for i in range(len(self._mol_frac_initial)):
            _avg_molmass_initial += self._mol_frac_initial[i] * self._molmass[i]
            _avg_molmass_liquid += self._mol_frac_liquid[i] * self._molmass[i]
            _avg_molmass_gaseuos += self._mol_frac_gaseuos[i] * self._molmass[i]

        if _avg_molmass_liquid == 0:
            _avg_molmass_liquid = _avg_molmass_initial
        if _avg_molmass_gaseuos == 0:
            _avg_molmass_gaseuos = _avg_molmass_initial

        _density_initial = 0
        _density_liquid = 0
        _density_gaseuos = 0

        for i in range(len(self._mol_frac_initial)):
            _density_initial += self._mol_frac_initial[i] * self._molmass[i] / (self._density[i] * _avg_molmass_initial)
            _density_liquid += self._mol_frac_liquid[i] * self._molmass[i] / (self._density[i] * _avg_molmass_liquid)
            _density_gaseuos += self._mol_frac_gaseuos[i] * self._molmass[i] / (self._density[i] * _avg_molmass_gaseuos)

        _density_initial = 1 / _density_initial
        _density_liquid = 1 / _density_liquid
        _density_gaseuos = 1 / _density_gaseuos

        return _e * _density_initial * _avg_molmass_gaseuos / (_density_gaseuos * _avg_molmass_initial)

    def get_temp_from_procent(self):
        """
        
        :return:
        """
