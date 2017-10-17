# Copyright 2016 Virgil Dupras
# Copyright 2017 Georg Drees
#
# This software is licensed under the "GPLv3" License as described in the "LICENSE" file,
# which should be included with this package. The terms are also available at
# http://www.gnu.org/licenses/gpl-3.0.html
#
# Adapted from base_import_bind.py

import re
import importlib
import logging

from core.plugin import ImportBindPlugin

# Which language to use for language dependent fuzzy matching
# until plugin preferences are implemented
FUZZY_MEMO_BIND_DEFAULT_LANGUAGE = 'en'


class FuzzyMemoBind(ImportBindPlugin):
    """Try to find matches between descriptions using different extractors.
    """
    NAME = "Fuzzy Memo Bind Plugin"
    AUTHOR = "Georg Drees"

    def match_entries(self,
                      target_account,
                      document,
                      import_document,
                      existing_entries,
                      imported_entries):
        matches = []
        # TODO
        return matches


class BaseExtractor():
    """Base class for extractors"""
    def get_tokens(self):
        raise NotImplementedError


class DateExtractor(BaseExtractor):
    """Extract dates in various formats from a text.

    Limitations:
        * only single-line texts were tested so far.
    Bugs:
        * parts of a text like "page 1/2" and even "p. 1/42" would be matched as date;
          however, since we are ultimately interested in determining the degree to which
          two texts are similar this is deemed acceptable.
    """

    DATE_PATTERNS = [re.compile(r'(\d{1,2}\.\d{1,2}\.(\d{2,4})*)'),  # EU
                     re.compile(r'(\d{4}-\d{2}-\d{2})'),             # ISO
                     re.compile(r'(\d{1,2}/\d{1,2}(/\d{2,4})*)')]    # US

    def __init__(self, memo, lang=None, ignorecase=False):
        self.tokens = []

        for pattern in self.DATE_PATTERNS:
            for m in pattern.finditer(memo):
                self.tokens.append(m.groups()[0])

        # FIXME: TODO implement plugin preferences for user to be able to set a language
        #             or disable language specific matching;
        # For testing use lang=False to disable language specific matching
        if lang is None:
            lang = FUZZY_MEMO_BIND_DEFAULT_LANGUAGE

        if lang:
            try:
                langdict = importlib.import_module('.fuzzy_memo_bind_langdicts.' + lang, 'core.plugin')
            except ImportError:
                logging.info("Failed to load Fuzzy Memo Bind LangDict for language '%s'", lang)
            else:
                try:
                    months = langdict.date_extractor['months']
                except KeyError:
                    logging.warning("No 'months' data found in Fuzzy Memo Bind LangDict for language '%s'", lang)
                else:
                    mogrify = 'lower' if ignorecase else '__str__'
                    for token in months:
                        if getattr(token, mogrify)() in getattr(memo, mogrify)():
                            self.tokens.append(token)

    def get_tokens(self):
        return self.tokens
