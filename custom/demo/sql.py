'''
Custom SQL REST API Module
Support for custom access to SQL tables that support the DM document management system

!!! CAUTION !!! ===============================================================================================================

    This module allows you to modify the SQL database that supports your DM system. However, with this power also comes
    the power to damage or destroy the SQL database tables that DM uses to control your document management environment.

    Examples of damage that can occur include the corruption of data in the SQL databases used by DM, the loss of system
    data maintained by DM, and the inability of DM to recover document objects stored in your DM repository.

    Because of the inherent danger associated with the improper use of this module, OpenText recommends that you incorporate
    this module only when other REST API commands do not provide the program functionality you require.

=============================================================================================================== !!! CAUTION !!!

GetCustomSQL(component,inputDict)
    Returns a single valid SQL statement based on the given dictionary of inputs

    INPUT:
    component - Which component should be executed
    inputDict - Dictionary containing all the parameters of the request
                Also included are:
                    _userid     - String containing the User ID of the user making the request
                    _groupid    - String containing the primary group of the user making the request

    OUTPUT:
    status - String containing 'ok' on success, anything else on failure
    strSQL - String containing a single valid SQL statement to be executed

    On success the SQL statement returned will be executed in the context of the user making the request
    On failure, any non 'ok' status, will be recported in the log
'''

def GetCustomSQL(component,inputDict):
    status = "ok"
    strSQL = ""
    
    if component == "aboutme": # Example of a statement based on the current user
        strSQL = "SELECT * FROM DOCSADM.PEOPLE WHERE USER_ID = '%s'" % inputDict.get("_userid")
    
    elif component == "aboutuser": # Example of a statement based on the specified user
        strSQL = "SELECT * FROM DOCSADM.PEOPLE WHERE USER_ID = '%s'" % inputDict.get("AUTHOR").upper()

    else:
        status = "Not implemented"
    
    return status, strSQL