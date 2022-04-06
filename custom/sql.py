'''
Custom SQL REST API Module
Support for custom access to SQL tables that support the DM document management system
Copyright (C) 2020 OpenText Corporation

!!! CAUTION !!! ===============================================================================================================

    This module allows external python code to be executed natively and has the power to damage or destroy.

    Because of the inherent danger associated with the improper use of this module, OpenText recommends that you incorporate
    this module only when other REST API commands do not provide the program functionality you require.

=============================================================================================================== !!! CAUTION !!!
'''

# ----------------------------------------------------------------------------------------------------------
#   GetCustomSQL(vendor,component,inputDict)
#       Returns a status and string (on success the string should contain a single valid SQL statement)
#       On success the SQL statement returned will be executed in the context of the user making the request
#
#       It uses the vendorID to call the approriate custom implementation of GetCustomSQL(inputDict)
#       If none is found, or not implemented correctly, an error will be returned an reported in the log
# ----------------------------------------------------------------------------------------------------------
def GetCustomSQL(vendor,component,inputDict):

    if vendor == "demo": #   Simple examples to to show what is capable
        from edocs.custom.demo.sql import GetCustomSQL
#    elif vendor == "<FolderName>": #   Example how to add another vendor
#        from edocs.custom.<FolderName>.sql import GetCustomSQL
    else:
        return "Not implemented",""

    return GetCustomSQL(component,inputDict)