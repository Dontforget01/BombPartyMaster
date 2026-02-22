# Bomb Party Master

Bomb Party Master is a Windows desktop application designed to assist Bomb Party gameplay by detecting on-screen syllables and suggesting valid French words.

The project focuses on OCR processing, word selection logic, and controlled user interaction.


## Project Overview

The application continuously observes a user-defined region of the screen where the game displays syllables.
When a syllable is detected, the system searches for a valid word from a French dictionary while tracking previously used words and letters.

The application never types automatically without user input.


## Internal Architecture

The project is structured into multiple modules, each with a clear responsibility.

### OCR System

- Periodically captures a defined screen region
- Uses OCR to extract text
- Filters and validates detected syllables
- Prevents duplicate detection

### Word Solver

- Searches a French dictionary
- Ensures the syllable is present
- Avoids reused words
- Optimizes letter coverage over time

### Typing System

- Simulates human-like typing behavior
- Includes delays and realistic keystroke timing
- Requires explicit user confirmation before typing

### UI System

- Displays detected syllables and suggested words
- Shows letter progression and history
- Allows enabling/disabling OCR and auto-typing
- Provides feedback on current application state


## User Workflow

1. The user launches the application
2. An OCR zone is selected on screen
3. OCR scanning is enabled
4. A syllable is detected and displayed
5. A valid word is suggested
6. The user decides whether to type, validate, or skip the word

This workflow ensures full user control at all times.

---

## Keyboard Controls

| Key   | Description                       |
|-------|-----------------------------------|
| SPACE | Type the suggested word           |
| ENTER | Validate the word                 |
| ESC   | Skip and search for another word  |


## Distribution

The Windows executable is distributed through GitHub Releases.
The source code is provided for educational review only.



## Legal Notice

This project is not open-source.

The source code is protected under a proprietary license.
Any reuse, modification, redistribution, or commercial use is strictly prohibited without explicit written permission from the author.

See the LICENSE file for full terms.


## Author

Anwar ALLAL
Student – Game Development / Computer Science
