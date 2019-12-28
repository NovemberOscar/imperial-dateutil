Imperial Dating System
=======================================

.. note::
    The Emperor DOES protects!

Usage
---------------------------------------

After praying to Machine-God Omnisiah, then command this Lingua-technis to your Cogitator.

    >>> from imperial_dateutil import ImperialDatingSystem
    >>> from datetime import datetime
    >>> d_t = ImperialDatingSystem(0, 123, 456, 41)
    <check_digit=0, year_fraction=123, year=456, millennium=M41>
    >>> print(d_t)
    0123456.M41
    >>> print(ImperialDatingSystem(0, 123, 456, 41) + ImperialDatingSystem(0, 123, 456, 41))
    0246912.M82
    >>> print(ImperialDatingSystem.now())
    0995019.M3
    >>> ImperialDatingSystem(0 ,123, 456, 41) == ImperialDatingSystem(0, 123, 456, 41)
    True
    >>> ImperialDatingSystem(0 ,123, 457, 41) > ImperialDatingSystem(0, 123, 456, 41)
    True
    >>> print(ImperialDatingSystem.from_gregorian(datetime(2005, 7, 18, 16)))
    0549005.M3


API
---------------------------------------

.. automodule:: imperial_dateutil.core.imperial
   :members:
   :undoc-members:
   :show-inheritance:
