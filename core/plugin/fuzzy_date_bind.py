# Copyright 2017 Georg Drees
# Copyright 2016 Virgil Dupras
#
# This software is licensed under the "GPLv3" License as described in the "LICENSE" file,
# which should be included with this package. The terms are also available at
# http://www.gnu.org/licenses/gpl-3.0.html
#
# Adapted from base_import_bind.py

import datetime

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

    DELTA_T = datetime.timedelta(4)  # 4 days
    CONFIDENCE = 0.75  # could be increased when implement memo matching / associations...

    def match_entries(self,
                      target_account,
                      document,
                      import_document,
                      existing_entries,
                      imported_entries):
        matches = []
        will_import = True

        for imported_entry in imported_entries:
            lo = imported_entry.date - DELTA_T
            hi = imported_entry.date + DELTA_T
            for existing_entry in existing_entries:
                if lo <= existing_entry.date and hi >= existing_entry.date:
                    for isplit in imported_entry.splits:
                        for esplit in existing_entry.splits:
                            if isplit.amount == esplit.amount:
                                matches.append(EntryMatch(existing_entry, imported_entry, will_import, CONFIDENCE))
                                break
                        #-------|
                        else:
                            continue
                        break  # break on inner break to get to next existing_entry
            #.......#---|
        return matches

