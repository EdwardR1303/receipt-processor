import re
import math

class ReceiptProcessor():
    def __init__(self, receipt={}):
        self.receipt = receipt
        self.retailer = receipt['retailer']
        self.purchase_date = receipt['purchaseDate']
        self.purchase_time = receipt['purchaseTime']
        self.items = receipt['items']
        self.total = receipt['total']

        self.total_points = 0
        self.process_receipt()

    def process_receipt(self):
        self.points_alphanum_rule()
        self.points_round_dollar_rule()
        self.points_multiple_of_25_rule()
        self.points_two_items_rule()
        self.points_description_multiple_of_3_rule()
        self.points_odd_date_rule()
        self.points_specific_time_rule()
    
    def points_alphanum_rule(self):
        """One point for every alphanumeric character in the retailer name."""
        pattern = r"^[\w\s\-&]+$"
        if not re.match(pattern, self.retailer):
            raise Exception('Invalid format for retailer')
        
        for char in self.retailer:
            if char.isalnum():
                self.total_points += 1

    def points_round_dollar_rule(self):
        """50 points if the total is a round dollar amount with no cents."""
        pattern = r"^\$?\d+\.\d{2}$"
        if not re.match(pattern, self.total):
            raise Exception('Invalid format for total')
        
        if self.total.endswith(".00"):
            self.total_points += 50

    def points_multiple_of_25_rule(self):
        """25 points if the total is a multiple of 0.25."""

        if self.total.endswith((".00", ".25", ".50", ".75")):
            self.total_points += 25

    def points_two_items_rule(self):
        """5 points for every two items on the receipt."""
        
        item_count = len(self.items)
        pairs = item_count//2

        self.total_points += pairs*5

    def points_description_multiple_of_3_rule(self):
        """If the trimmed length of the item description is a multiple of 3, 
            multiply the price by 0.2 and round up to the nearest integer. 
            The result is the number of points earned."""

        for item in self.items:
            description = item['shortDescription'].strip()
            if len(description) % 3 == 0:
                price = item['price']
                self.total_points += math.ceil(float(price)*0.2)


    def points_odd_date_rule(self):
        """6 points if the day in the purchase date is odd."""
        
        #Assumes the date is in YYYY-MM-DD format
        pattern = r"^\d{4}-\d{2}-\d{2}$"
        if not re.match(pattern, self.purchase_date):
            raise Exception('Invalid format for purchase_date')
        
        day = self.purchase_date.split('-')[-1]
        if int(day) % 2 == 1:
            self.total_points += 6


    def points_specific_time_rule(self):
        """10 points if the time of purchase is after 2:00pm and before 4:00pm."""
        
        #Assumes the purchase time is in military time
        pattern = r"^\d{2}:\d{2}$"
        if not re.match(pattern, self.purchase_time):
            raise Exception('Invalid format for purchase_time')
        hour = int(self.purchase_time.split(':')[0])

        if hour >= 14 and hour < 16:
            self.total_points += 10