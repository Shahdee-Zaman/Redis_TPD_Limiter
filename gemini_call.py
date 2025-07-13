import os
import google.generativeai as genai
from Redis_TPD_Limit import TPDLimit

"""
    Google's Gemini api is used as it allows free calls.
    If you have your api key set as an environment variable, you do not need to pass it directly in Generative AI.
    Google also has separate TPD(Token per Day) for each model.
    You can keep track of each model and move on to the next model when you reach you TPD limit.
    Limit is for token used is lower by 10000 in TPDLimit for any response however it is still advised to pass a lower number in case of lengthy response. 
"""

# Uncomment and pass your API key below if you do not wish to set the environment variable.
# genai.configure(api_key="your_api_key_here")

prompt = input("What is your question?")

# Multiple dbs used rather than ports to lower resource usage
flash = TPDLimit(host='localhost', port=6379, limit=900000)
lite = TPDLimit(host='localhost', port=6379, db=1, limit=900000)

# Proceed only if there is enough tokens left
if flash.generate(prompt):
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content(prompt)
    print(response.text)
    # Increment the response to Redis database
    flash.response_count(response.text)

# Different model called if the first model has reached the token limit
elif lite.generate(prompt):
    model = genai.GenerativeModel('gemini-2.0-flash-lite')
    response = model.generate_content(prompt)
    print(response.text)
    # Response incremented for proper tracking
    lite.response_count(response.text)

print(flash.token_used())
print(lite.token_used())
