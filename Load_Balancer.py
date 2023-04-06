'''
This is an example of a toy-load-balancer 
which implements the token bucket algorithm
'''
import time
import random
import logging
class LoadBalancer:
    def __init__(self, server_list, capacity, rate):
        self.server_list = server_list
        self.capacity = capacity
        self.rate = rate
        self.tokens = capacity

        # Initialize the timestamp to the current time
        self.last_refill_time = time.time()

    def get_server(self):
        # Refill the tokens based on the elapsed time since the last refill
        self.refill()

        # If there are no tokens available, return None
        if self.tokens <= 0:
            return None

        # Choose a server and decrement the token count
        server = random.choice(self.server_list)
        self.tokens -= 1

        return server

    def refill(self):
        # Calculate the elapsed time since the last refill
        current_time = time.time()
        time_elapsed = current_time - self.last_refill_time

        # Calculate the number of tokens that should have been refilled
        tokens_refilled = time_elapsed * self.rate

        # Add the tokens to the bucket, up to the maximum capacity
        self.tokens = min(self.capacity, self.tokens + tokens_refilled)
        logging.info(f"Tokens = {self.tokens}")

        # Update the last refill time
        self.last_refill_time = current_time
