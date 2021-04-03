"""
Grab-bag module to hold utility classes and functions.

"""


class CountdownTimer:
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
        # don't try to update if no time is elapsing
        if delta_time and self.running:

            # clamp minimum time to zero
            self._remaining = max(0.0, self._remaining - delta_time)

            if self._remaining == 0.0:
                self.running = False


class StopwatchTimer:
    """

    Starts keeping time when set to running mode.

    """
    def __init__(
        self,
        time: float = 0.0,
        running: bool = False,
        maximum: float = None
    ):
        self.time = time
        self.running = running
        self.maximum = maximum
        self._completion = 0.0 if maximum else None

    def update(self, delta_time: float = 1 / 60) -> None:

        if delta_time and self.running:
            self.time += delta_time
        else:
            return

        if self.maximum:
            if self.maximum <= self.time:
                self.running = False
            self._completion = min(1.0, self.time / self.maximum)

    @property
    def completion(self) -> float:
        return self._completion


