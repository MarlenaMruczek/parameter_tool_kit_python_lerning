# Parameters Tool Kit

A Python tool for comparing two versions of a parameter set (old vs. new), validating the input data, and generating a report of the differences. 
The tool is intended to be run through the batch file `run.bat`, which starts the Python script and keeps the console window open so the messages can be read.

## Features

- Loads parameter sets from JSON files
- Validates the structure (required keys: `name`, `unit`, `min`, `max`, and `value` or `points`)
- Checks that values are within the allowed `min`/`max` bounds
- Reports every problem found in one run, not just the first one
- Compares old and new parameters and generates `report.csv`
