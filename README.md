# WPD_Limiter
WPD(Token Per Day) usage limiter using Redis. WPD although not accurate, it can function as a simple alternative for token limiter in LLMs. If you would prefer an exact token limiter, you can check out: [Gemini Token Tracker](https://github.com/Shahdee-Zaman/Gemini-TPD_Limiter).

## Features
- Tracks usage of Word Count
- Automatically reset daily usage count based on UTC date
- Simple to implement and use

## Requirements
- Python
- Redis

## For Windows
Requires WSL(Windows Subsystem for Linux) or Docker for running Redis on Windows

## Example
Gemini_call.py is an example class to show how to use Redis_WPD_Limit.py.

## License
MIT




