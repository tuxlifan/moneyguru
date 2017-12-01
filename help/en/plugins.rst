Plugins
=======

Since moneyGuru v2.5, it's possible to expand moneyGuru's capability through Python plugins. Plugins
are Python 3 source files that come in two flavors: "core" and "user".

Core plugins are bundled directly in moneyGuru and most of them are enabled by default, with the exceptions listed below.

User plugins are located in the plugin folder (the location of that folder depends on the system,
but you can open that folder through "File --> Open Plugin Folder") and are disabled by default.
To install a new user plugin, you can simply copy the python source file of that plugin in that
folder and restart moneyGuru.

You can enable and disable plugins through the "Plugin management" view, available whenever you
open a new tab. Simply check/uncheck the box next to the plugin you want to enable/disable and
restart moneyGuru.

**Warning.** moneyGuru plugins are not sandboxed, which means that technically, they could contain
malicious code. Only install plugins from trusted sources or after having reviewed the code
yourself.

Plugin types
------------

Plugins are still relatively new in moneyGuru's design and they don't allow a hugely broad range
of capabilities. For now, this is the types of plugins that are supported:

* Read-only tables (``ReadOnlyTablePlugin``)
* Currency providers (``CurrencyProviderPlugin``)
* Import Actions (``ImportActionPlugin``)
* Import match bindings (``ImportBindPlugin``)

The "Read-only table" type is a "view" kind of plugin, that is, it creates a new tab type. When
this type of plugin is installed, a new entry will appear in the "Plugins" list of the New Tab
view. Simply double-click on it to open it. The data in those tables is not "live" data and thus
isn't refreshed when data in the document changes, so the tab has to be closed and reopened for the
data to be refreshed.

But despite that limitation, there's quite a lot of possibilities, especially for custom reports.
Printing, sorting and CSV-copy-pasting (selecting rows, copying data and then pasting it in
Excel/Numbers) work with those tables.

Currency providers allow you to create new currencies besides builtin ones *and* define a way to
fetch exchange rates information for these currencies. When enabled, they'll add currencies to the
system and that currency will be usable in the same way as with any other currency.

Import actions allow us to define new actions to perform on transactions about to be imported. You
know, those "Day <--> Month" swap things? They're import actions. So, adding a new plugin of this
type will add new options to this list.

Import match bindings are plugins that allow us to re-define the way we do automatic matching when
importing transactions in an existing account. For now, we only have one core plugin of this type
that match transactions based on IDs supplied by the OFX format. If you add a plugin of that type,
additional criterias will be used for matching (for example, you could match based on date+amount).

Core plugins that are not enabled by default
--------------------------------------------

You can enable any core plugin that is not enabled by default in the same way as you would enable
a user plugin in the "Plugin management" view as described above on this page.

Fuzzy Date Bind Plugin
^^^^^^^^^^^^^^^^^^^^^^
With the ``Fuzzy Date Bind Plugin`` you can let moneyGuru match transactions whose dates are not exactly
the same but within a certain date range (up to 4 days earlier or later) during import. For a match to
occurr also at least one amount in the splits of the compared transactions must have the same value.

To help match the most logical pairs the following heuristic is used:
    * a match with exactly the *same dates* has the highest weight
    * existing transactions with a date *earlier* than the imported transaction are preferred after that,
      with a higher weight the closer the dates match.
    * existing transactions with a date *later* than the imported transaction have the lowest weights
      which are even more decreased for more distant dates.

Therefore matches with the same dates are matched as they would have been without this plugin and
the common case of an account withdrawal ('imported' transaction; with e.g. the monthly statement)
being recorded with a date a few days after the purchase ('existing' transaction, entered e.g. with
a manual entry) should also be matched automatically.

This plugin is not enabled by default to prevent unexpected behavior.

Creating a plugin
-----------------

There's :mod:`a small convenience API <core.plugin>`, but it's a rather slim one. You're mostly
coding straight on top of moneyGuru's code. There's a
:doc:`developer documentation <developer/index>` telling you about moneyGuru's API as a whole.

So, to create a plugin, I'd suggest that you take one of the examples (available
`on Github <https://github.com/hsoft/moneyguru/tree/develop/core/plugin>`__), duplicate it and
try to wade your way through with example comments. 

I'm very interested in knowing about plugin development efforts so don't hesitate to
`contact me <mailto:hsoft@hardcoded.net>`_ if you need help with the development of your plugin.

