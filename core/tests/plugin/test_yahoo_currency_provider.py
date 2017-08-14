# Copyright 2017 Virgil Dupras
#
# This software is licensed under the "GPLv3" License as described in the "LICENSE" file,
# which should be included with this package. The terms are also available at
# http://www.gnu.org/licenses/gpl-3.0.html

import pytest

from ...plugin.yahoo_currency_provider import YahooProviderPlugin

@pytest.mark.needs_network
def test_boc_currency_provider_EUR():
    provider = YahooProviderPlugin()
    # don't crash
    rate = provider.get_currency_rate_today('UAH')
    assert isinstance(rate, float)

