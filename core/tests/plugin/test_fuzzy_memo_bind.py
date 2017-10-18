# Copyright 2017 Virgil Dupras, Georg Drees
#
# This software is licensed under the "GPLv3" License as described in the "LICENSE" file,
# which should be included with this package. The terms are also available at
# http://www.gnu.org/licenses/gpl-3.0.html

import logging
from hscommon.testutil import eq_sorted

from ...plugin.fuzzy_memo_bind import DateExtractor

logging.basicConfig(level=logging.DEBUG)


class TestDateExtractor:

    def test_numeric_date_extraction(self):
        # Verify that DateExtractor extracts numeric dates but not other numbers
        test_memo = ''.join(["This string 28.9.6275 demonstrates multiple 2015-10-15 numeric date 22/3/3186 formats",
                             "1/1 that 12/30 should all 5.3.5102 be 42 parsed 17/08/3483 without 404 other 08/12/20",
                             "numbers being 30.12. considered. They were 11.22 random generated. And could",
                             "occur15.11.without whitespace12/12surrounding6/18/68them3.14159."])
        test_dates = ['28.9.6275', '2015-10-15', '22/3/3186',
                      '1/1', '12/30', '5.3.5102', '17/08/3483', '08/12/20',
                      '30.12.',
                      '15.11.', '12/12', '6/18/68']
        result = DateExtractor(test_memo).get_tokens()
        eq_sorted(result, test_dates)

    def test_known_bug_n_of_m(self):
        # Demonstrate that e.g. 'page 1/42' would trigger extraction.
        # This test is expected to fail once the bug would be fixed.
        test_memo = "This is page 1/2, see also other p. 1/42"
        test_dates = ['1/2', '1/42']
        result = DateExtractor(test_memo).get_tokens()
        eq_sorted(result, test_dates)

    def test_language_dicts_loading(self):
        memo = 'November from 11/1'
        expected_numeric = ['11/1']
        expected_numeric_and_tokens = ['November', 'Nov', '11/1']
        # Using lang=False to disable language specific matching until user preferences are implemented
        # c.f. fuzzy_memo_bind.py: DateExtractor.__init__
        eq_sorted(DateExtractor(memo, lang=False).get_tokens(), expected_numeric)
        eq_sorted(DateExtractor(memo, lang="some_unknown_language").get_tokens(), expected_numeric)
        eq_sorted(DateExtractor(memo, lang="en").get_tokens(), expected_numeric_and_tokens)

    def test_language_ignorecase(self):
        memo = 'november'
        expected_casesense = []
        expected_ignorecase = ['November', 'Nov']
        eq_sorted(DateExtractor(memo, lang="en", ignorecase=False).get_tokens(), expected_casesense)
        eq_sorted(DateExtractor(memo, lang="en", ignorecase=True).get_tokens(), expected_ignorecase)
