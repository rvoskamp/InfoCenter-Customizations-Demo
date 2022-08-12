# Using customization files with InfoCenter

InfoCenter customizations use multiple files for defining and delivering the required components. It is strongly recommend to scan the contents of these files to avoid anything being ommitted due to a syntax error.

To assist with this task we have included **FlightCheck.py** which will scan the contents of required files and generate a log file for you to review. Simply Drag & Drop all the files found in a customization folder onto the FlightCheck.py file and a FlightCheck.log file will be generated within the customization folder.

The log file will contain details about the scan, it's results as well as a JSON structure containing the signatures of the supplied files.
