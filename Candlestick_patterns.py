class Doji:
    def __init__(self, body_percent=0.1):
        self.name = "doji"
        self.body_percent = body_percent
        self.success_green = 0
        self.success_red = 0
        self.success_all = 0

        self.failure_green = 0
        self.failure_red = 0
        self.failure_all = 0

        self.total_tries_green = 0
        self.total_tries_red = 0
        self.total_tries_all = 0

        self.acc_over_time_green = []
        self.acc_over_time_red = []
        self.acc_over_time_all = []

        self.acc_green = 0
        self.acc_red = 0
        self.acc_all = 0

    def reset(self):
        self.success_green = 0
        self.success_red = 0
        self.success_all = 0

        self.failure_green = 0
        self.failure_red = 0
        self.failure_all = 0

        self.total_tries_green = 0
        self.total_tries_red = 0
        self.total_tries_all = 0

        self.acc_over_time_green = []
        self.acc_over_time_red = []
        self.acc_over_time_all = []

        self.acc_green = 0
        self.acc_red = 0
        self.acc_all = 0


    def evaluate(self, open, high, low, close):
        lower_shadow = min(open, close) - low
        upper_shadow = high - max(open, close)
        body = abs(open - close)
        whole_candle = high - low

        if body / whole_candle <= self.body_percent:
            if open < close:
                return True, True, False
            else:
                return True, False, True
        else:
            return False, False, False

    def append(self, open, high, low, close, trend, future_price, min_percent_increase):
        lower_shadow = min(open, close) - low
        upper_shadow = high - max(open, close)
        body = abs(open - close)
        whole_candle = high - low

        if body / whole_candle <= self.body_percent:
            self.total_tries_green += 1
            self.total_tries_red += 1
            self.total_tries_all += 1

            if trend >= 0.5 and future_price < (close * (1 - min_percent_increase)):
                if open > close:
                    self.success_green += 1
                    self.acc_over_time_green.append(1)
                else:
                    self.success_red += 1
                    self.acc_over_time_red.append(1)
                self.success_all += 1
                self.acc_over_time_all.append(1)
            elif trend < 0.5 and future_price > (close * (1 + min_percent_increase)):
                if open > close:
                    self.success_green += 1
                    self.acc_over_time_green.append(1)
                else:
                    self.success_red += 1
                    self.acc_over_time_red.append(1)
                self.success_all += 1
                self.acc_over_time_all.append(1)

            else:
                if open > close:
                    self.failure_green += 1
                    self.acc_over_time_green.append(0)
                else:
                    self.failure_red += 1
                    self.acc_over_time_red.append(0)
                self.failure_all += 1
                self.acc_over_time_all.append(0)

            if self.total_tries_green >= 1:
                self.acc_green = self.success_green / self.total_tries_green
            if self.total_tries_red >= 1:
                self.acc_red = self.success_red / self.total_tries_red
            if self.total_tries_all >= 1:
                self.acc_all = self.success_all / self.total_tries_all
            return True
        else:
            if self.total_tries_green >= 1:
                self.acc_green = self.success_green / self.total_tries_green
            if self.total_tries_red >= 1:
                self.acc_red = self.success_red / self.total_tries_red
            if self.total_tries_all >= 1:
                self.acc_all = self.success_all / self.total_tries_all
            return False


class Hammer:
    def __init__(self, body_percent=0.25, max_upper_shadow=0.05):
        self.name = "hammer"
        self.body_percent = body_percent
        self.max_upper_shadow = max_upper_shadow
        self.success_green = 0
        self.success_red = 0
        self.success_all = 0

        self.failure_green = 0
        self.failure_red = 0
        self.failure_all = 0

        self.total_tries_green = 0
        self.total_tries_red = 0
        self.total_tries_all = 0

        self.acc_over_time_green = []
        self.acc_over_time_red = []
        self.acc_over_time_all = []

        self.acc_green = 0
        self.acc_red = 0
        self.acc_all = 0

    def reset(self):
        self.success_green = 0
        self.success_red = 0
        self.success_all = 0

        self.failure_green = 0
        self.failure_red = 0
        self.failure_all = 0

        self.total_tries_green = 0
        self.total_tries_red = 0
        self.total_tries_all = 0

        self.acc_over_time_green = []
        self.acc_over_time_red = []
        self.acc_over_time_all = []

        self.acc_green = 0
        self.acc_red = 0
        self.acc_all = 0

    def evaluate(self, open, high, low, close):
        lower_shadow = min(open, close) - low
        upper_shadow = high - max(open, close)
        body = abs(open - close)
        whole_candle = high - low

        if body / whole_candle <= self.body_percent and (upper_shadow / whole_candle) <= self.max_upper_shadow:
            if open > close:
                return True, True, False
            else:
                return True, False, True
        else:
            return False, False, False


    def append(self, open, high, low, close, trend, future_price, min_percent_increase):
        lower_shadow = min(open, close) - low
        upper_shadow = high - max(open, close)
        body = abs(open - close)
        whole_candle = high - low
        if whole_candle == 0:
            return

        if body / whole_candle <= self.body_percent and (upper_shadow / whole_candle) <= self.max_upper_shadow:
            self.total_tries_green += 1
            self.total_tries_red += 1
            self.total_tries_all += 1

            if future_price > (close * (1 + min_percent_increase)):
                if open > close:
                    self.success_green += 1
                    self.acc_over_time_green.append(1)
                else:
                    self.success_red += 1
                    self.acc_over_time_red.append(1)
                self.success_all += 1
                self.acc_over_time_all.append(1)
            else:
                if open > close:
                    self.failure_green += 1
                    self.acc_over_time_green.append(0)
                else:
                    self.failure_red += 1
                    self.acc_over_time_red.append(0)
                self.failure_all += 1
                self.acc_over_time_all.append(0)

                if self.total_tries_green >= 1:
                    self.acc_green = self.success_green / self.total_tries_green
                if self.total_tries_red >= 1:
                    self.acc_red = self.success_red / self.total_tries_red
                if self.total_tries_all >= 1:
                    self.acc_all = self.success_all / self.total_tries_all
                return True
        else:
            if self.total_tries_green >= 1:
                self.acc_green = self.success_green / self.total_tries_green
            if self.total_tries_red >= 1:
                self.acc_red = self.success_red / self.total_tries_red
            if self.total_tries_all >= 1:
                self.acc_all = self.success_all / self.total_tries_all
            return False


class ShootingStar:
    def __init__(self, body_percent=0.25, max_lower_shadow=0.05):
        self.name = "shooting_star"
        self.body_percent = body_percent
        self.max_lower_shadow = max_lower_shadow
        self.success_green = 0
        self.success_red = 0
        self.success_all = 0

        self.failure_green = 0
        self.failure_red = 0
        self.failure_all = 0

        self.total_tries_green = 0
        self.total_tries_red = 0
        self.total_tries_all = 0

        self.acc_over_time_green = []
        self.acc_over_time_red = []
        self.acc_over_time_all = []

        self.acc_green = 0
        self.acc_red = 0
        self.acc_all = 0

    def reset(self):
        self.success_green = 0
        self.success_red = 0
        self.success_all = 0

        self.failure_green = 0
        self.failure_red = 0
        self.failure_all = 0

        self.total_tries_green = 0
        self.total_tries_red = 0
        self.total_tries_all = 0

        self.acc_over_time_green = []
        self.acc_over_time_red = []
        self.acc_over_time_all = []

        self.acc_green = 0
        self.acc_red = 0
        self.acc_all = 0

    def evaluate(self, open, high, low, close):
        lower_shadow = min(open, close) - low
        upper_shadow = high - max(open, close)
        body = abs(open - close)
        whole_candle = high - low

        if body / whole_candle <= self.body_percent and (lower_shadow / whole_candle) <= self.max_lower_shadow:
            if open > close:
                return True, True, False
            else:
                return True, False, True
        else:
            return False, False, False

    def append(self, open, high, low, close, trend, future_price, min_percent_increase):
        lower_shadow = min(open, close) - low
        upper_shadow = high - max(open, close)
        body = abs(open - close)
        whole_candle = high - low

        if body / whole_candle <= self.body_percent and (lower_shadow / whole_candle) <= self.max_lower_shadow:
            self.total_tries_green += 1
            self.total_tries_red += 1
            self.total_tries_all += 1

            if close > (future_price * (1 + min_percent_increase)):
                if open > close:
                    self.success_green += 1
                    self.acc_over_time_green.append(1)
                else:
                    self.success_red += 1
                    self.acc_over_time_red.append(1)
                self.success_all += 1
                self.acc_over_time_all.append(1)
            else:
                if open > close:
                    self.failure_green += 1
                    self.acc_over_time_green.append(0)
                else:
                    self.failure_red += 1
                    self.acc_over_time_red.append(0)
                self.failure_all += 1
                self.acc_over_time_all.append(0)

            if self.total_tries_green >= 1:
                self.acc_green = self.success_green / self.total_tries_green
            if self.total_tries_red >= 1:
                self.acc_red = self.success_red / self.total_tries_red
            if self.total_tries_all >= 1:
                self.acc_all = self.success_all / self.total_tries_all
            return True
        else:
            if self.total_tries_green >= 1:
                self.acc_green = self.success_green / self.total_tries_green
            if self.total_tries_red >= 1:
                self.acc_red = self.success_red / self.total_tries_red
            if self.total_tries_all >= 1:
                self.acc_all = self.success_all / self.total_tries_all
            return False


class HangingMan:
    def __init__(self, body_percent=0.1, max_upper_shadow=0.2):
        self.name = "hanging_man"
        self.body_percent = body_percent
        self.max_upper_shadow = max_upper_shadow
        self.success_green = 0
        self.success_red = 0
        self.success_all = 0

        self.failure_green = 0
        self.failure_red = 0
        self.failure_all = 0

        self.total_tries_green = 0
        self.total_tries_red = 0
        self.total_tries_all = 0

        self.acc_over_time_green = []
        self.acc_over_time_red = []
        self.acc_over_time_all = []

        self.acc_green = 0
        self.acc_red = 0
        self.acc_all = 0

    def reset(self):
        self.success_green = 0
        self.success_red = 0
        self.success_all = 0

        self.failure_green = 0
        self.failure_red = 0
        self.failure_all = 0

        self.total_tries_green = 0
        self.total_tries_red = 0
        self.total_tries_all = 0

        self.acc_over_time_green = []
        self.acc_over_time_red = []
        self.acc_over_time_all = []

        self.acc_green = 0
        self.acc_red = 0
        self.acc_all = 0

    def evaluate(self, open, high, low, close):
        lower_shadow = min(open, close) - low
        upper_shadow = high - max(open, close)
        body = abs(open - close)
        whole_candle = high - low

        if body / whole_candle <= self.body_percent and (upper_shadow / whole_candle) <= self.max_upper_shadow:
            if open > close:
                return True, True, False
            else:
                return True, False, True
        else:
            return False, False, False

    def append(self, open, high, low, close, trend, future_price, min_percent_increase):
        lower_shadow = min(open, close) - low
        upper_shadow = high - max(open, close)
        body = abs(open - close)
        whole_candle = high - low

        if body / whole_candle <= self.body_percent and (upper_shadow / whole_candle) <= self.max_upper_shadow:
            self.total_tries_green += 1
            self.total_tries_red += 1
            self.total_tries_all += 1

            if future_price < (close * (1 - min_percent_increase)):
                if open > close:
                    self.success_green += 1
                    self.acc_over_time_green.append(1)
                else:
                    self.success_red += 1
                    self.acc_over_time_red.append(1)
                self.success_all += 1
                self.acc_over_time_all.append(1)
            else:
                if open > close:
                    self.failure_green += 1
                    self.acc_over_time_green.append(0)
                else:
                    self.failure_red += 1
                    self.acc_over_time_red.append(0)
                self.failure_all += 1
                self.acc_over_time_all.append(0)

                if self.total_tries_green >= 1:
                    self.acc_green = self.success_green / self.total_tries_green
                if self.total_tries_red >= 1:
                    self.acc_red = self.success_red / self.total_tries_red
                if self.total_tries_all >= 1:
                    self.acc_all = self.success_all / self.total_tries_all
                return True
        else:
            if self.total_tries_green >= 1:
                self.acc_green = self.success_green / self.total_tries_green
            if self.total_tries_red >= 1:
                self.acc_red = self.success_red / self.total_tries_red
            if self.total_tries_all >= 1:
                self.acc_all = self.success_all / self.total_tries_all
            return False


class GravestoneDoji:
    def __init__(self, body_percent=0.1, max_lower_shadow=0.2):
        self.name = "gravestone_doji"
        self.body_percent = body_percent
        self.max_lower_shadow = max_lower_shadow
        self.success_green = 0
        self.success_red = 0
        self.success_all = 0

        self.failure_green = 0
        self.failure_red = 0
        self.failure_all = 0

        self.total_tries_green = 0
        self.total_tries_red = 0
        self.total_tries_all = 0

        self.acc_over_time_green = []
        self.acc_over_time_red = []
        self.acc_over_time_all = []

        self.acc_green = 0
        self.acc_red = 0
        self.acc_all = 0

    def reset(self):
        self.success_green = 0
        self.success_red = 0
        self.success_all = 0

        self.failure_green = 0
        self.failure_red = 0
        self.failure_all = 0

        self.total_tries_green = 0
        self.total_tries_red = 0
        self.total_tries_all = 0

        self.acc_over_time_green = []
        self.acc_over_time_red = []
        self.acc_over_time_all = []

        self.acc_green = 0
        self.acc_red = 0
        self.acc_all = 0

    def evaluate(self, open, high, low, close):
        lower_shadow = min(open, close) - low
        upper_shadow = high - max(open, close)
        body = abs(open - close)
        whole_candle = high - low

        if body / whole_candle <= self.body_percent and (lower_shadow / whole_candle) <= self.max_lower_shadow:
            if open > close:
                return True, True, False
            else:
                return True, False, True
        else:
            return False, False, False

    def append(self, open, high, low, close, trend, future_price, min_percent_increase):
        lower_shadow = min(open, close) - low
        upper_shadow = high - max(open, close)
        body = abs(open - close)
        whole_candle = high - low

        if body / whole_candle <= self.body_percent and (lower_shadow / whole_candle) <= self.max_lower_shadow:
            self.total_tries_green += 1
            self.total_tries_red += 1
            self.total_tries_all += 1

            if future_price < (close * (1 - min_percent_increase)):
                if open > close:
                    self.success_green += 1
                    self.acc_over_time_green.append(1)
                else:
                    self.success_red += 1
                    self.acc_over_time_red.append(1)
                self.success_all += 1
                self.acc_over_time_all.append(1)
            else:
                if open > close:
                    self.failure_green += 1
                    self.acc_over_time_green.append(0)
                else:
                    self.failure_red += 1
                    self.acc_over_time_red.append(0)
                self.failure_all += 1
                self.acc_over_time_all.append(0)

                if self.total_tries_green >= 1:
                    self.acc_green = self.success_green / self.total_tries_green
                if self.total_tries_red >= 1:
                    self.acc_red = self.success_red / self.total_tries_red
                if self.total_tries_all >= 1:
                    self.acc_all = self.success_all / self.total_tries_all
                return True
        else:
            if self.total_tries_green >= 1:
                self.acc_green = self.success_green / self.total_tries_green
            if self.total_tries_red >= 1:
                self.acc_red = self.success_red / self.total_tries_red
            if self.total_tries_all >= 1:
                self.acc_all = self.success_all / self.total_tries_all
            return False
