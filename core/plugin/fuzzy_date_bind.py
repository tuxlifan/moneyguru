# Copyright 2017 Georg Drees
# Copyright 2016 Virgil Dupras
#
# This software is licensed under the "GPLv3" License as described in the "LICENSE" file,
# which should be included with this package. The terms are also available at
# http://www.gnu.org/licenses/gpl-3.0.html
#
# Adapted from base_import_bind.py

import datetime
from itertools import product
import logging

from core.plugin import ImportBindPlugin, EntryMatch
from core.plugin.fuzzy_memo_bind import DateExtractor

#
# TODO: possible error source: date range selected for moneyguru.
#
#       Does it influence existing_entries below? Are there older entries that don't appear?
#


class FuzzyDateBind(ImportBindPlugin):
    """Check for each imported txn if there is an existing txn that is within [date - DELTA_T, date + DELTA_T]
    and has at least one matching split amount.
    """
    NAME = "Fuzzy Date Bind Plugin"
    AUTHOR = "Georg Drees"

    BASE_CONFIDENCE = 0.75  # could be increased when implement memo matching / associations...
    CONF_PER_MEMODATE_MATCH = 0.07
    DELTA_T = datetime.timedelta(4)  # 4 days
    # positive key: imported is after existing
    # (e.g. money taken from account (import) after purchase date (manual entry, existing))
    PENALTIES = {-7: .13,
                 -6: .12,
                 -5: .11,
                 -4: .10,
                 -3: .09,
                 -2: .08,
                 -1: .07,
                 0: 0,
                 +1: .01,
                 +2: .02,
                 +3: .03,
                 +4: .04,
                 +5: .05,
                 +6: .06,
                 +7: .07,
                 }

    def match_entries(self,
                      target_account,
                      document,
                      import_document,
                      existing_entries,
                      imported_entries,
                      do_refine_matches=True,
                      lang=None):
        matches = []
        will_import = True

        entry_pairs = [(i, e) for i, e in product(imported_entries, existing_entries)
                       if abs(i.date - e.date) <= self.DELTA_T]

        for imported_entry, existing_entry in entry_pairs:
            if any(isplit.amount == esplit.amount
                   for isplit, esplit in product(imported_entry.splits, existing_entry.splits)):
                confidence = self.BASE_CONFIDENCE - self.PENALTIES[(imported_entry.date - existing_entry.date).days]
                logging.debug("Fuzzy Date date range match (%1.3f): %s %s", confidence, imported_entry, existing_entry)
                if do_refine_matches:
                    num_memo_date_matches = sum(int(idate == edate) for idate, edate
                                                in product(DateExtractor(imported_entry.description, lang=lang)
                                                           .get_tokens(),
                                                           DateExtractor(existing_entry.description, lang=lang)
                                                           .get_tokens()))
                    confidence += num_memo_date_matches * self.CONF_PER_MEMODATE_MATCH
                    logging.debug("Fuzzy Date Descriptions match #: %i", num_memo_date_matches)
                    logging.debug("Fuzzy Date: DateExtractor IMPORTED:")
                    logging.debug(DateExtractor(imported_entry.description, lang=lang).get_tokens())
                    logging.debug("Fuzzy Date: DateExtractor EXISTING:")
                    logging.debug(DateExtractor(existing_entry.description, lang=lang).get_tokens())
                # Use "existing, imported" order according to EntryMatch definition
                logging.debug("Fuzzy Date final confidence: %.3f", min(confidence, 1.00))
                matches.append(EntryMatch(existing_entry, imported_entry, will_import, min(confidence, 1.00)))

        return matches
