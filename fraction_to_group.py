""" A program to convert fractional composition of oil into group one"""
""" Программа для перевода фракционного состава нефти в групповой"""


class FractionToGroup:

    def __init__(self, d_15_15, t_10, t_50, t_90, t_95,
                 dens_sum_aromatics, dens_paraffins, dens_naftenes, dens_olefines,
                 dens_bt, dens_dbt, dens_thiophenes, dens_sulfides, dens_disulfides,
                 dens_pyrrole, dens_pyridine, dens_carb, dens_indole, dens_xylene,
                 mm_sum_aromatics, mm_paraffins, mm_naftenes, mm_olefines,
                 mm_bt, mm_dbt, mm_thiophenes, mm_sulfides, mm_disulfides,
                 mm_pyrrole, mm_pyridine, mm_carb, mm_indole, mm_xylene,
                 bromine_number, sulfur_mass_fraction, nitrogen_mass_fraction):
        """
        Listing of boiling temperatures for fractions accuired according to ASTM D86-15
        :param d_15_15: float - relative density of oil at 15C to water density at 15C
        :param t_10: float - 10% fraction boiling temperature
        :param t_50: float - 50% fraction boiling temperature
        :param t_90: float - 90% fraction boiling temperature
        :param t_95: float - 95% fraction boiling temperature

        Listing of densities of components in the mix
        :param dens_sum_aromatics: float - density of all aromatics in the mix
        :param dens_paraffins: float - density of paraffins in the mix
        :param dens_naftenes: float - density of naftenes in the mix
        :param dens_olefines: float - density of olefines in the mix
        :param dens_bt: float - ???
        :param dens_dbt: float - ???
        :param dens_thiophenes: float - density of tiophenes in the mix
        :param dens_sulfides: float - density of sulphides in the mix
        :param dens_disulfides: float - density of disulphides in the mix
        :param dens_pyrrole: float - density of pyrrole in the mix
        :param dens_pyridine: float - density of pyridine in the mix
        :param dens_carb: float - density of acids (?) in the mix
        :param dens_indole: float - density of indole in the mix
        :param dens_xylene: float - density of xylene in the mix

        Listing of molecular masses of components in the mix
        :param mm_sum_aromatics: float -
        :param mm_paraffins: float -
        :param mm_naftenes: float -
        :param mm_olefines: float -
        :param mm_bt: float -
        :param mm_dbt: float -
        :param mm_thiophenes: float -
        :param mm_sulfides: float -
        :param mm_disulfides: float -
        :param mm_pyrrole: float -
        :param mm_pyridine: float -
        :param mm_carb: float -
        :param mm_indole: float -
        :param mm_xylene: float -

        Listing of misc parameters
        :param bromine_number: float -
        :param sulfur_mass_fraction: float -
        :param nitrogen_mass_fraction: float -

        :return: None
        """

        _d_15_15 = d_15_15 * 0.994 + 0.0093
        _t_10 = t_10
        _t_50 = t_50
        _t_90 = t_90
        _t_95 = t_95

        _dens_sum_aromatics = dens_sum_aromatics
        _dens_paraffins = dens_paraffins
        _dens_naftenes = dens_naftenes
        _dens_olefines = dens_olefines
        _dens_bt = dens_bt
        _dens_dbt = dens_dbt
        _dens_thiophenes = dens_thiophenes
        _dens_sulfides = dens_sulfides
        _dens_disulfides = dens_disulfides
        _dens_pyrrole = dens_pyrrole
        _dens_pyridine = dens_pyridine
        _dens_carb = dens_carb
        _dens_indole = dens_indole
        _dens_xylene = dens_xylene

        _mm_sum_aromatics = mm_sum_aromatics
        _mm_paraffins = mm_paraffins
        _mm_naftenes = mm_naftenes
        _mm_olefines = mm_olefines
        _mm_bt = mm_bt
        _mm_dbt = mm_dbt
        _mm_thiophenes = mm_thiophenes
        _mm_sulfides = mm_sulfides
        _mm_disulfides = mm_disulfides
        _mm_pyrrole = mm_pyrrole
        _mm_pyridine = mm_pyridine
        _mm_carb = mm_carb
        _mm_indole = mm_indole
        _mm_xylene = mm_xylene

        _bromine_number = bromine_number
        _sulfur_mass_fraction = sulfur_mass_fraction
        _nitrogen_mass_fraction = nitrogen_mass_fraction
