import redis
from datetime import datetime, timezone

# ----------------- Start Of Class Creation -----------------

class TPDLimit:

    """
        Create a redis database that keeps real time track of all tokens called using word count.
        Redis will allow for easy tracking of word usage and ensure a restart does not result in loss of count.
        Generate and response_count need to be called for proper tracking.
        Generate requires a single parameter that includes all inputs (System Instruction and user prompt).
        Response requires a single parameter which is the response.
    """

    def __init__(self, host, port, limit, db=0):
        # Redis setup
        self.database = redis.Redis(host, port, db)
        # Setting WPD Usage Limit. Leaving Extra space for outputs.
        self.AI_WPD_limit = limit - 10000

    # Check for Daily WPD reset
    def check_daily_reset(self):
        current_date = datetime.now(timezone.utc).strftime('%y:%m:%d')
        # Decode the date to compare with current_date
        if str(self.redis_decoder('date')) != current_date:
            self.database.set('date', current_date)
            self.database.set('token_usage', 0)


    # Check if the prompt is within WPD limit
    def has_tokens(self, input):
        estimated_total = int(self.redis_decoder('token_usage')) + len(input)
        # Resulting input will exceed WPD usage limit
        if estimated_total <= self.AI_WPD_limit:
            self.database.incrby('token_usage', len(input))
            return True
        return False




# ----------------- End Of Class Creation -----------------

    # ----------------- Helper Functions -----------------

    # Returns the number of words used
    def token_used(self):
        self.check_daily_reset()
        if self.redis_decoder('token_usage'):
            return int(self.redis_decoder('token_usage'))

        # Return 0 if no word has been added
        else:
            return 0

    # Decode returned values from bytes
    def redis_decoder(self, value):
        decoded = self.database.get(value)
        return decoded.decode() if decoded else None

    # ----------------- End of Helper Functions -----------------

    # ----------------- Main Function -----------------

    # The required function that needs to be called to properly run the Class
    # Returns True if the api call can proceed
    def generate(self, prompt):
        self.check_daily_reset()
        if self.has_tokens(prompt):
            return True
        return False

    # Increments the word count of response
    def response_count(self, response):
        self.database.incrby('token_usage', len(response))



