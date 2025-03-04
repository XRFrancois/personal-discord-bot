# personal-discord-bot
This repository contains all the files related to my project of making a personal discord bot for my server.

I intend on doing a Python version and a Javascript version with Node.js for comparison.

## Requirements
Details of the drafted requirements can be found in ./docs
Python 3.8+

## Design

## Implementation
Can be found in ./src

## Tests
Can be found in ./test

## Deployment

## Maintenance


## Run
- Create a virtual environment with Python 3.8+
```python -m venv .venv```

- Activate the environment
```.venv\Scripts\activate.bat```

- Upgrade pip before installing
```python.exe -m pip install --upgrade pip```

- Install the package dependancies
```pip install -r requirements.txt```

- Run the bot
```python src/main.py```

- Deactivate the environment
```deactivate```

### Personal Notes
When creating a slash command, it can be server specific or global.
After adding a new one, I need to sync on the desired scale. Server specific with the Guild ID is preferred for development purposes.
Once it is up, discord must be refreshed.