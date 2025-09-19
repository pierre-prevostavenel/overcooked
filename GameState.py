class GameState:
    def __init__(self):
        self.completed_orders = 0
        self.failed_orders = 0

    def complete_order(self):
        self.completed_orders += 1

    def fail_order(self):
        self.failed_orders += 1

    def __repr__(self):
        return f"Completed Orders: {self.completed_orders}\n Failed Orders: {self.failed_orders}"
       