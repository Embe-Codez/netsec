# Cisco FMC Access Control Policy Updater

## This Python script updates the settings for all allow rules in an access control policy in the Cisco Firepower Management Center (FMC) API.

### Requirements

    Python 3.x
    requests library
    A Cisco Firepower Management Center (FMC) with API access

### Installation

    Clone this repository to your local machine.
    Install the requests library: pip install requests.
    Create environment variables on your local machine based on the config.py file.
    Run the script: python main.py.

### Usage

    Enter the access control policy ID when prompted.
    Enter the intrusion policy ID when prompted.
    Enter the variable set ID when prompted.
    Enter the file policy ID when prompted.

### The script will then loop through each non-allow rule and update its settings as described below:

    By default, the script sets the following values for each non-allow rule:
        logBegin is set to True
        logEnd is set to False
        sendEventsToFMC is set to True
        enableSyslog is set to True
    If an allow rule already has a syslogConfig attribute, the script will not overwrite it.
    If the rule already has sendEventsToFMC set to True, the script will not overwrite it.
    If the rule already has logBegin set to True, the script will not overwrite it.
    If an allow rule does not already have an ipsPolicy attribute, the script will add it with the specified intrusion policy ID.
    If an allow rule does not already have a variableSet attribute, the script will add it with the specified variable set ID.
    If an allow rule does not already have a filePolicy attribute, the script will add it with the specified file policy ID.

### Note: If a PUT request fails, the script will retry up to three times before moving on to the next rule.

### Please ensure that you have the necessary access credentials before running the script.