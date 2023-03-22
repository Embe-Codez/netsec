## [1.0.0] - 2023-03-13
Added

    Initial release of the script.
    Functionality to update all allow rules in an access control policy Cisco FMC.
    Prompts user for access control policy ID, intrusion policy ID, variable set ID, and file policy ID.
    Loops through each rule to update its settings.
    Sets default values for each allow rule for logBegin, logEnd, sendEventsToFMC, and enableSyslog.
    Adds IPS Policy attribute, Variable Set attribute, and File Policy attribute for allow rules that don't currently have those properties.
    README.md file with usage instructions.
    gitignore file for Python.