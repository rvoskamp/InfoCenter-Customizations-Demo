'''
Custom Process REST API Module
Support for custom access to SQL tables that support the DM document management system

!!! CAUTION !!! ===============================================================================================================

    This module allows you to execute predefined python scripts. However, with this power also comes
    the power to damage or destroy the SQL database tables that DM uses to control your document management environment.

    Examples of damage that can occur include the corruption of data in the SQL databases used by DM, the loss of system
    data maintained by DM, and the inability of DM to recover document objects stored in your DM repository.

    Because of the inherent danger associated with the improper use of this module, OpenText recommends that you incorporate
    this module only when other REST API commands do not provide the program functionality you require.

=============================================================================================================== !!! CAUTION !!!

GetCustomProcess(component,inputDict)
    Returns single python data structure after executing python code natively

    INPUT:
    component - Which component should be executed
    inputDict - Dictionary containing all the parameters of the request
                Also included are:
                    _userid         - String containing the User ID of the user making the request
                    _groupid        - String containing the primary group of the user making the request
                    _requestBody    - Dictionary containing the full body of the request
                    _responseBody   - Dictionary containing the full response to the request

    OUTPUT:
    status - String containing control flow
                - 'ok'      Continue with normal processing
                - 'cancel'  Cancel normal processing and return as success
                - 'abort'   Cancel normal processing and return as failure
                - Anything else will be treated as an internal error and will disable the event handler              
    data - Data to be turned to the client
                - On 'abort', string containing the 'abort' error message
                - On 'cancel', data structure in the same format of normal execution
'''

def GetCustomProcess(component,inputDict):
    status = "ok"
    data = ""
    
    if component == 'geturl':
        pURL = inputDict.get("url")
        if pURL:
            import json
            import urllib.request
            with urllib.request.urlopen(pURL) as response:
                html = response.read()
                data = json.loads(html)

    else: # Undefined process
        status = "Not implemented"
    
    return status, data