from project import test  # local
import unittest


class Test_Countries(unittest.TestCase):

    # test question 1
    def test_import_data(self):
        c = test.import_data()
        # test some countries. If source file changes, this may fail
        dPortugal = {'Area': 92391, 'Continent': 'Europe', 'GDP': 18000.0,
                     'Literacy': 93.3, 'Phones': 399.21, 'Population': 10605870.0}
        dAfghanistan = {'Area': 647500, 'Continent': 'Asia', 'GDP': 700.0,
                        'Literacy': 36.0, 'Phones': 3.22, 'Population': 31056997.0}
        dZambia = {'Area': 752614, 'Continent': 'Africa', 'GDP': 800.0,
                   'Literacy': 80.6, 'Phones': 8.23, 'Population': 11502010.0}
        self.assertEqual(c["Portugal"], dPortugal)
        self.assertEqual(c["Afghanistan"], dAfghanistan)
        self.assertEqual(c["Zambia"], dZambia)

    # test question 2
    def test_convert_population_to_int(self):
        c = test.import_data()
        cint = test.convert_population_to_int(c)["Afghanistan"]["Population"]
        self.assertIsInstance(cint, int)

    # test question 3
    def test_convert_area_to_sq_km(self):
        c = test.import_data()
        areaSqMiles = round(c["Portugal"]["Area"]*2.58999, 1)
        test.convert_area_to_sq_km(c)
        self.assertEqual(c["Portugal"]["Area"], areaSqMiles)

    # test question 4
    def test_get_europe_countries(self):
        c = test.import_data()
        # test random countries. If source file changes, this may fail
        europeanCountries = ['Albania', 'Denmark', 'Estonia', 'Finland', 'Hungary',
                             'Liechtenstein', 'Lithuania', 'Luxembourg', 'Portugal', 'Spain', 'Sweden']
        self.assertTrue(set(test.get_europe_countries(c)).issuperset(set(europeanCountries)))

    # test question 5
    def test_get_literacy_levels_by_continent(self):
        c = test.import_data()
        literacy = test.get_literacy_levels_by_continent(c, "Africa")
        # test all literacy levels. If source file changes, this may fail
        testList = [('Niger', 17.6, 'VERY_LOW'), ('Mali', 46.4, 'LOW'), ('Togo', 60.9, 'MEDIUM'),
                    ('Zambia', 80.6, 'HIGH'), ('Zimbabwe', 90.7, 'VERY_HIGH')]
        self.assertTrue(set(literacy).issuperset(set(testList)))

    # test question 6
    def test_get_country_codes(self):
        c = test.import_data()
        countryCodes = test.get_country_codes(c)
        # test some codes. If source file changes, this may fail
        testList = ["POR", "ISR", "AUS", "SPA", "ZIM"]  # test some
        self.assertTrue(set(countryCodes).issuperset(set(testList)))

    # test question 7.1
    def test_get_population_in_millions(self):
        ct = test.Country("MyCountry", 10310234, "MyContinent")
        self.assertEqual(ct.get_population_in_millions(), round(10310234/1000000, 2))

    # test question 7.2
    def test_get_country_population(self):
        c = test.import_data()
        self.assertEqual(test.get_country_population(c, "Portugal"), round(c["Portugal"]["Population"]/1000000, 2))
        self.assertEqual(test.get_country_population(c, "MyCountry"), None)


if __name__ == '__main__':
    unittest.main()
