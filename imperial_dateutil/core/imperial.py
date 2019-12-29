import datetime


MAKR_CONSTANT = 0.11407955


class ImperialDatingSystem:
    """
    The Imperial Dating System of the Imperium of Man, also known as the Imperial Calendar, is fairly complex in
    nature, and has been structured so as to deal with the vast amount of recorded history that exists in the 41st
    Millenium and the massive distances between settled human worlds, which can lead to long periods of isolation.

    Also the vagaries and time-warping effects of the Immaterium can make it almost impossible to keep accurate track of
    time over long journeys.

    The Imperium has developed its own method of recording dates, which needs a bit of explanation. Most importantly,
    the years are always Anno Domini (A.D.) using the numbering system of our own present-day Gregorian Calendar,
    so the dates themselves are the ones that we are familiar with now.

    A typical date as Imperial scholars write it would look something like 0.123.456.M41. This date can be divided up so
    that each part is explained separately below:

    +--------------+---------------+------+------------+
    | Check Number | Year Fraction | Year | Millennium |
    +==============+===============+======+============+
    | 0            | 123           | 456  | M41        |
    +--------------+---------------+------+------------+

    Following the birth of the Great Rift and the start of the Era Indomitus, temporal anomalies spread across the galaxy
    making the use of a universal dating system extremely difficult as different Imperial worlds began to experience the
    passage of time at different subjective rates.

    A new, more localised dating system came into existence that was different for each world. It used the birth of the
    Great Rift as the standard event from which all time was calculated, either before or after its creation.

    Copyright
        this descriptions are copied from https://warhammer40k.fandom.com/wiki/Imperial_Dating_System

    :param check_number:
        The check number refers to the accuracy of a given date, which is required for clarity
        due to the common distortions of subjective linear time that occur while travelling within the Warp,
        and inaccuracies in timing on remote or isolated Imperial worlds and star systems.
    :type check_number: int
    :param year_fraction:
        For record-keeping, each year is divided into 1000 equal parts, numbered 001-000,
        rather than months or weeks. Note that this system is not generally used by Imperial citizens in everyday
        life, but is simply for administrative use by the Adeptus Terra.
    :type year_fraction: int
    :param year: This is the year within the millennium, running from 001-999.
    :type year: int
    :param millennium:
        This is the millennium since the birth of the ancient human religious figure Jesus Christ
        in which the event took place.
    :type millennium: int
    """

    def __init__(self, check_number, year_fraction, year, millennium):
        """
        :type check_number: int
        :type year_fraction: int
        :type year: int
        :type millennium: int
        """
        self.check_number = check_number
        self.year_fraction = year_fraction
        self.year = year
        self.millennium = millennium

        if check_number > 9 or check_number < 0:
            raise ValueError
        if year_fraction > 999 or year_fraction < 0:
            raise ValueError
        if year > 999 or year < 0:
            raise ValueError
        if millennium < 1:
            raise ValueError

    @classmethod
    def _generate_year_fraction(cls, converted_date, hour=0):
        determined_hour = (converted_date * 24) + hour
        imperial_fraction = int(determined_hour * MAKR_CONSTANT)

        return imperial_fraction

    def to_gregorian(self):
        """
        A function returns a tuple of minimum, median, and maximum values(datetime) calculated from the imperial format.

        .. Note:: minimum is closer to correct value

        :return: (minimum, median, maximum)
        """
        if self.millennium > 3:
            raise ValueError("Gregorian date system not supported after M3")

        determined_time = self.year_fraction / MAKR_CONSTANT
        days = determined_time / 24 - 1
        year = (self.millennium - 1) * 1000 + self.year

        base_datetime = datetime.datetime(year, 1, 1)

        t = base_datetime + datetime.timedelta(days)
        t = datetime.datetime(year=t.year, month=t.month, day=t.day, hour=t.hour)

        min_t = base_datetime + datetime.timedelta(days - 1)
        min_t = datetime.datetime(year=min_t.year, month=min_t.month, day=min_t.day)

        max_t = base_datetime + datetime.timedelta(days + 1)
        max_t = datetime.datetime(year=max_t.year, month=max_t.month, day=max_t.day)

        return min_t, t, max_t

    @classmethod
    def from_gregorian(cls, t, check_number=0):
        """
        A function returns ImperialDatingSystem of given gregorian date/datetime

        :param t: Gregorian based datetime or date
        :type t: datetime.datetime or datetime.date
        :param check_number: accuracy of `t`, numbered 0-9
        :return: Imperial time format of given `t`
        """
        if not isinstance(t, datetime.datetime) or not isinstance(t, datetime.date):
            raise TypeError

        year_fraction = cls._generate_year_fraction(t.timetuple().tm_yday+1, t.timetuple().tm_hour)
        year = t.year % 1000
        millennium = (t.year // 1000) + 1

        return cls(check_number, year_fraction, year, millennium)

    @classmethod
    def now(cls):
        """
        A function returns ImperialDatingSystem of current time

        :return: Imperial time format of current time
        """
        t = datetime.datetime.utcnow()
        self = cls.from_gregorian(t)
        return self

    def __str__(self):
        return '{}{:03d}{:03d}.M{}'.format(
            self.check_number,
            self.year_fraction,
            self.year,
            self.millennium,
        )

    def __repr__(self):
        return '<check_digit={}, year_fraction={:03d}, year={:03d}, millennium=M{}>'.format(
            self.check_number,
            self.year_fraction,
            self.year,
            self.millennium,
        )

    def _cmp(self, other):
        if isinstance(other, ImperialDatingSystem):
            if other.check_number != self.check_number:
                raise TypeError("Can not perform operation between data with different accuracy.")

            m_cmp = 0 if self.millennium == other.millennium else 1 if self.millennium > other.millennium else -1
            y_cmp = 0 if self.year == other.year else 1 if self.year > other.year else -1
            yf_cmp = 0 if self.year_fraction == other.year_fraction else 1 if self.year_fraction > other.year_fraction else -1

            if m_cmp == 0:
                if y_cmp == 0:
                    return yf_cmp
                else:
                    return y_cmp
            else:
                return m_cmp
        else:
            raise NotImplementedError

    def __eq__(self, other):
        if isinstance(other, ImperialDatingSystem):
            return self._cmp(other) == 0
        else:
            return NotImplemented

    def __le__(self, other):
        if isinstance(other, ImperialDatingSystem):
            return self._cmp(other) <= 0
        else:
            return NotImplemented

    def __lt__(self, other):
        if isinstance(other, ImperialDatingSystem):
            return self._cmp(other) < 0
        else:
            return NotImplemented

    def __ge__(self, other):
        if isinstance(other, ImperialDatingSystem):
            return self._cmp(other) >= 0
        else:
            return NotImplemented

    def __gt__(self, other):
        if isinstance(other, ImperialDatingSystem):
            return self._cmp(other) > 0
        else:
            return NotImplemented

    def __add__(self, other):
        if isinstance(other, ImperialDatingSystem):
            if other.check_number != self.check_number:
                raise TypeError("Can not perform operation between data with different accuracy.")

            year_fraction = (self.year_fraction + other.year_fraction)
            year = (self.year + other.year) + (year_fraction // 1000)
            millennium = (self.millennium + other.millennium) + (year // 1000)

            year_fraction = year_fraction % 1000
            year = year % 1000

            return type(self)(self.check_number, year_fraction, year, millennium)
        if isinstance(other, datetime.timedelta):
            year_fraction = self._generate_year_fraction(other.days % 365, (other.seconds / 60 / 60))
            year = other.days // 365 % 1000
            millennium = other.days // 365 // 1000

            return type(self)(
                self.check_number,
                self.year_fraction+year_fraction,
                self.year+year,
                self.millennium+millennium
            )
        else:
            return NotImplemented

    __radd__ = __add__
