# InfoCenter Customization Folder
The contents of this folder allows you to customize the interaction with the user.  This includes adding contextual menu items, executing custom actions and providing custom forms when specific user interaction is required.

## Contents 
| File            | Description                    |
|-----------------|------------------------------- |
|**commands.json**| Menu definitions               |
|**code.js**      | Enabling logic and custom code |
|**forms.json**   | Custom form definitions        |
|**sql.py**       | Custom SQL statements          |
|**process.py**   | Custom process statements      |

---
## Getting started

### Adding a menu item
**commands.json** is a JSON file that provides a list of menu definitions to the client.

Each defintion requires:
- ***cmd*** Command reference (This is used in *code.js*)
- ***label*** Name of the menu item
- ***type*** List of menu lists that the definition will appear in

| *type*     | Location                                    |
| ---------- | ------------------------------------------- |
| container  | Menu bar across the top of a container view |
| properties | Dropdown menu of the properties view        |


```json
{
	"cmd": "hello_world",
	"label": "Greetings",
	"type": ["container", "properties"]
}
```
See the *demo* menu definitions [here](commands.json)


### Enabling menu items and the actions taken on their selection
**code.js** is a JavaScript file that is used to implement the code behind all the menu items defined in *commands.json*

It starts by associating customizations with the appropriate *vendor* (folder name)

```js
ICC.demo = {

};
```

Then each *cmd* (menu item) must be defined
```js
ICC.demo = {
    hello_world: {

    }
};
```

**Enabling:**

The *enable* function is evaluated by the client to determine if it should display the menu item.

To help with the determination logic the client supplies the following parameters:

| Parameter | Description                      |
| --------- | -------------------------------- |
| parent    | Current location                 |
| list      | Array of selected items (if any) |
| rights    | User's rights                    |

```js
ICC.demo = {
    hello_world: {
        enable: function(parent, list, rights) {
            // Enable only when nothing is selected
            return !list || list.length == 0;
        }
    }
};
```

**Custom code:**

The *do* function is executed when the menu item is selected by the user.

To help with the determination logic the client supplies the following parameters:

| Parameter | Description                      |
| --------- | -------------------------------- |
| parent    | Current location                 |
| list      | Array of selected items (if any) |
```js
ICC.demo = {
    hello_world: {
        enable: function(parent, list, rights) {
            // Enable only when nothing is selected
            return !list || list.length == 0;
        },

        do: function(parent, list) {
            //
            // Custom code here
            //
            // Give user informational feedback that something happened
            //	Syntax:
            //		notify.info(<title>,<message>)
            //
            ICC.globals.notify.info('Greetings', `Hello world!`);
            return true;
        }
    }
};
```
See the *demo* menu implementations [here](code.js)

---

## Adding a custom form

Interaction with the user, either to display or obtain information, requires the use of custom forms. This is accomplished by using **forms.json** to define the forms that will then be referenced in *code.js*. To take full advantage of this capability you should be familiar with the components that make up an eDOCS form.

**Adding forms:**

The JSON file consists of a list of forms:
```json
{
	"forms": [

    ]
}
```

Each form definition is a dictionary with required keys and a list of field definitions (*defs*):
```json
{
	"forms": [
		{
			"data": {
				"fldtype": "form",
				"name": "hello_world_form",
				"prompt": "Hello world",
				"localonly": true,
				"defs": [

                ]
            }
        }
    ]
}
```

See the *demo* form definitions [here](forms.json)


**Accessing forms:**

Once defined, the custom code can ask the client to display the form using runform()

Syntax: runform(*form defaults*,*vendor*,*form name*,*title*)
```js
    ICC.globals.runform({}, 'demo', 'hello_world_form', 'Hi there').then(
    res => {
        
    }, err => {
        ICC.globals.notify.warning('Custom Code Says', `err: ${err.toString()}`);
    }
```
Code execution is suspended until the user is finished and dismisses the form, Ok/Cancel. At this point the execution resumes with *res* containing the response from the user's interaction.

See the *demo* form interactions [here](code.js)

---

## Accessing the REST API from within custom code
During code execution there may be a need to call into the REST API to access additional information. This is done by using restrequest() and properly formed URL.

Syntax: restrequest(*method*,*url*)
```js
    ICC.globals.restrequest("GET", urlRequest).then(
    res => {
        
    }, err => {
        ICC.globals.notify.warning('Custom Code Says', `err: ${err.toString()}`);
    }
```

If the existing REST API does not support your needs, you can create a predefined SQL and then call into the REST API to execute it.

**sql.py** is a Python file which constructs an SQL statement that will be executed by the REST API before returning the results to the client. *component* is the name associated with the custom statement.
```python
def GetCustomSQL(component,inputDict):
    status = "ok"
    strSQL = ""
    
    if component == "aboutme": # Example of a statement based on the current user
        strSQL = "SELECT * FROM DOCSADM.PEOPLE WHERE USER_ID = '%s'" % inputDict.get("_userid")
    else:
        status = "Not implemented"
    
    return status, strSQL
```

See the *demo* predefined custom SQL statements [here](sql.py)

The URL will now refer to the named statement:
```js
    urlRequest = 'custom/sql/demo/aboutme?library=' + ICC.globals.primarylibrary;
    ICC.globals.restrequest("GET", urlRequest).then(
    res => {
        
    }, err => {
        ICC.globals.notify.warning('Custom Code Says', `err: ${err.toString()}`);
    }
```

If additional data is external to eDOCS, you can create a custom process to access the data and then call into the REST API to execute it.

**process.py** is a Python file which executes native code before returning the results to the client. *component* is the name associated with the custom process.
```python
def GetCustomProcess(component,inputDict):
    status = "ok"
    strSQL = ""
    
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
    
    return status, strSQL
```
See the *demo* predefined process statements [here](process.py)

The URL will now refer to the named process:
```js
    urlParameter = 'https%3A//query1.finance.yahoo.com/v7/finance/quote?symbols=OTEX';
	urlRequest = 'custom/process/demo/geturl?library=' + ICC.globals.primarylibrary + '&url=' + urlParameter;
    ICC.globals.restrequest("GET", urlRequest).then(
    res => {
        
    }, err => {
        ICC.globals.notify.warning('Custom Code Says', `err: ${err.toString()}`);
    }
```
See the *demo* REST API interactions [here](code.js)