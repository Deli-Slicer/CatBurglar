"""
Grab-bag module to hold utility classes and functions.

"""


class Timer:
    """

    Generic timer object to assist with gameplay and animation.

    It can tick at a passed rate, but uses 1/60th of a second as a default in
    the absence of a passed time interval. It can also be paused so update
    attempts do nothing to the amount of time left and set to restart whenever
    time is added to it.

    """
    def __init__(
            self,
            remaining: float = 0.0,
            running: bool = True,
            start_after_adding_time: bool = True
    ):
        """
        :param remaining: how much time is left on this clock
        :param running: whether callling update will decrement the clock
        :param start_after_adding_time: whether adding time will start it running
        """
        self.running = running
        self._remaining = remaining
        self.start_after_adding_time = start_after_adding_time

    @property
    def remaining(self) -> float:
        return self._remaining

    @remaining.setter
    def remaining(self, amount: float) -> None:
        """
        Set the amount of time remaining to a specific value.

        :param amount:
        :return:
        """

        # Enable the += operator to work with the setter so adding time auto-starts timer
        if self._remaining < amount and self.start_after_adding_time:
            self.running = True

        self._remaining = amount

    def update(self, delta_time: float = 1 / 60) -> None:
        """
        Decrement the timer by the passed amount if it's currently enabled.

        :param delta_time: how much to decrement remaining time by.
        :return:
        """
        if self.running:

            # clamp minimum time to zero
            self._remaining = max(0.0, self._remaining - delta_time)

            if self._remaining == 0.0:
                self.running = False

