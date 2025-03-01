import unittest
from requests.exceptions import Timeout

from semanticscholar.SemanticScholar import SemanticScholar
from semanticscholar.SemanticScholarException \
    import BadQueryParametersException


class SemanticScholarTest(unittest.TestCase):

    def setUp(self) -> None:
        self.sch = SemanticScholar()

    def test_paper(self):
        data = self.sch.get_paper('10.1093/mind/lix.236.433')
        self.assertEqual(data.title,
                         'Computing Machinery and Intelligence')
        self.assertEqual(data.raw_data['title'],
                         'Computing Machinery and Intelligence')
        self.sch.timeout = 0.01
        self.assertEqual(self.sch.timeout, 0.01)
        self.assertRaises(Timeout,
                          self.sch.get_paper,
                          '10.1093/mind/lix.236.433')

    def test_author(self):
        data = self.sch.get_author(2262347)
        self.assertEqual(data.name, 'A. Turing')
        self.assertEqual(data.raw_data['name'], 'A. Turing')

    def test_not_found(self):
        data = self.sch.get_paper(0).raw_data
        self.assertEqual(len(data), 0)

    def test_bad_query_parameters(self):
        self.assertRaises(BadQueryParametersException,
                          self.sch.get_paper,
                          '10.1093/mind/lix.236.433',
                          fields=['unknown'])

    def test_search_paper(self):
        data = self.sch.search_paper('turing')
        self.assertGreater(data.total, 0)
        self.assertGreater(data.next, 0)
        data.next_page()
        self.assertGreater(len(data), 100)

    def test_search_paper_fields_of_study(self):
        data = self.sch.search_paper('turing', fields_of_study=['Mathematics'])
        self.assertEqual(data[0].s2FieldsOfStudy[0]['category'], 'Mathematics')

    def teste_search_author(self):
        data = self.sch.search_author('turing')
        self.assertGreater(data.total, 0)
        self.assertEqual(data.next, 0)


if __name__ == '__main__':
    unittest.main()
