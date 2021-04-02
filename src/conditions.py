from exmo.tasks.conditions import Condition


class LessTopBidCondition(Condition):
    def __init__(self, threshold):
        self.threshold = float(threshold)

    def check(self, data) -> bool:
        bid_top = data.get('BTC_USD').get('bid_top')
        print(bid_top)
        mark = bid_top and (float(bid_top) > self.threshold)
        print(mark)
        return bid_top and (float(bid_top) > self.threshold)
