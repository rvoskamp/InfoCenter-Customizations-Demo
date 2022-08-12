# InfoCenter Customizations
You can customize InfoCenter to include client side menu items and forms. You can also manipulate data at the REST API level.

See details about the contents of the *custom* folder [here](./custom/).

# Installation of sample customizations
Download the *custom* folder to your installation of the REST API under the *edocs* folder.
```
..\edocs
    apihandlers
    controllers
    custom
```

:sparkles:
##  **New for 22.3**
# Configuration requirements for customizations

We have introduced a new "Customizations" section in the RESTAPI.JSON file to set access and security for each customization.

Firstly, define the custom folders that you want to authorize for the system.

```JSON
    "Customizations": {
        "AuthorizedVendors": {
            "<folder name>" : {}
        }
    }
```

You then have the option to further restrict access to these customizations based on the user's primary group. This is achieved by using "AccessGranted" to list only those groups whose members are allowed access.

```JSON
    "Customizations": {
        "AuthorizedVendors": {
            "<folder name>" : {
                "AccessGranted" : [
                    <Groups who should have access>
                ]
            }
        }
    }
```

Or, if simpler, use "AccessDenied" to deny access to only the members of the listed groups.

```JSON
    "Customizations": {
        "AuthorizedVendors": {
            "<folder name>" : {
                "AccessDenied" : [
                    <Groups who should NOT have access>
                ]
            }
        }
    }
```

An optional "Signatures" configuration has been added to prevent unauthorized changes being served to the client. Each file that has a signature that will be checked against its current content to confirm that nothing has changed.

```JSON
    "Customizations": {
        "AuthorizedVendors": {
            "<folder name>" : {
                "Signatures": {
                    "<file name>": <signature>
                }
            }
        }
    }
```

The new "FlightCheck" customization tool has been added to do a precheck of the custom files for correctness, to flag access to external systems and to generate correct JSON data that can be used in your RESTAPI.JSON file.

# Customization Tools
We've provided tools to help you get started with your own customizations. Download the *Customization Tools* folder to where you you will be doing most of your development.