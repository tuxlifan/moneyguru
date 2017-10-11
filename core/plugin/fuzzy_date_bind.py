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
    DELTA_T = datetime.timedelta(4)  # 4 days
    # positive key: imported is after existing
    # (e.g. money taken from account (import) after purchase date (manual entry, existing))
    PENALTIES = {-4: .08,
                 -3: .07,
                 -2: .06,
                 -1: .05,
                 0: 0,
                 +1: .01,
                 +2: .02,
                 +3: .03,
                 +4: .04, }

    def match_entries(self,
                      target_account,
                      document,
                      import_document,
                      existing_entries,
                      imported_entries):
        matches = []
        will_import = True

        entry_pairs = [(i, e) for i, e in product(imported_entries, existing_entries)
                       if abs(i.date - e.date) <= self.DELTA_T]

        for imported_entry, existing_entry in entry_pairs:
            if any(isplit.amount == esplit.amount
                   for isplit, esplit in product(imported_entry.splits, existing_entry.splits)):
                confidence = self.BASE_CONFIDENCE - self.PENALTIES[(imported_entry.date - existing_entry.date).days]
                logging.debug("Fuzzy Date Bind match (%1.2f): %s %s", confidence, imported_entry, existing_entry)
                # Use "existing, imported" order according to EntryMatch definition
                matches.append(EntryMatch(existing_entry, imported_entry, will_import, confidence))

        return matches
