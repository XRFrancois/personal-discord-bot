# Discord Bot Requirements

## Project Overview
This bot is designed to assist in organizing roles and automating the creation of new categories + role and give it a textual and vocal channel. It will be written in Python and hosted on [did not decide yet].

## Functional Requirements
- The bot must be written in English.
- The bot must be able to:
  - Respond to user commands to perform the following tasks.
  - Create a new role with given permissions.
  - Create a new category for the new role that is only visible to users with that role AND visible to admins.
  - Create a text channel & a voice channel in that category.
  - Log its actions in a private channel.
  - Welcome users, explain the system and allow them to pick some roles.

## Non-Functional Requirements
- The bot must respond within 250ms to user commands.
- The bot must handle up to 5 concurrent users.
- The bot must log errors for debugging.

## Tech Stack & Dependencies
- **Programming Language**: Python (+ JavaScript?)
- **Framework**: discord.py (+discord.js)

## Future Features?
- Automatic moderation
- Mini-games like rock, paper, scissor
- Level system
- Log Data on player / games ? Build a database and a method to cross games between players (e.g. P1 x P2 x P3)