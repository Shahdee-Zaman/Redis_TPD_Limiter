import redis
from datetime import datetime, timezone

# ----------------- Start Of Class Creation -----

class TPDLimit():

    def __init__(self, host, port, limit):
        # Redis setup
        self.database = redis.Redis(host=host, port=port)
        # Setting TPD Usage Limit
        self.Gemini_TPD_limit = limit

    # Decode returned values from bytes
    def redis_decoder(self, value):
        decoded = self.database.get(value)
        return decoded if decoded else None


    # Check for Daily TPD reset
    def check_daily_reset(self):
        current_date = datetime.now(timezone.utc).strftime('%y:%m:%d')
        # Decode the date to compare with current_date
        if str(self.redis_decoder('date')) != current_date:
            self.database.set('date', current_date)
            self.database.set('token_usage', 0)


    # Check if the prompt is within TPD limit
    def has_tokens(self, input):
        estimated_total = int(self.redis_decoder('token_usage')) + len(input)
        # Resulting input will exceed TPD usage limit
        if estimated_total <= self.Gemini_TPD_limit:
            self.database.incrby('token_usage', len(input))
            return True
        return False

    # Returns the amount of tokens used
    def token_used(self):
        return int(self.redis_decoder('token_usage'))



# ----------------- End Of Class Creation -----

    def generate(self, prompt):
        self.check_daily_reset()
        if self.has_tokens(prompt):
            return True
        return False





