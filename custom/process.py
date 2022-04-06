'''
Custom Process REST API Module
Support for custom processes external to eDOCS
Copyright (C) 2020 OpenText Corporation

!!! CAUTION !!! ===============================================================================================================

    This module allows external python code to be executed natively and has the power to damage or destroy.

    Because of the inherent danger associated with the improper use of this module, OpenText recommends that you incorporate
    this module only when other REST API commands do not provide the program functionality you require.

=============================================================================================================== !!! CAUTION !!!
'''

# ----------------------------------------------------------------------------------------------------------
#   GetCustomProcess(vendor,component,inputDict)
#       Returns custom JSON data that the caller should expect
#
#       It uses the vendorID to call the approriate custom implementation of GetCustomProcess(inputDict)
#       If none is found, or not implemented correctly, an error will be returned an reported in the log
# ----------------------------------------------------------------------------------------------------------
def GetCustomProcess(vendor,component,inputDict):

    if vendor == "demo":
        from edocs.custom.demo.process import GetCustomProcess
#    elif vendor == "<FolderName>": #   Example how to add another vendor
#        from edocs.custom.<FolderName>.sql import GetCustomProcess
    else:
        return "Not implemented",""

    return GetCustomProcess(component,inputDict)