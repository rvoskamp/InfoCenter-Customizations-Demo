ICC.demo = {
	/* ================================================================================
	
		ICC.<vendor> = {
			vendor : Name of folder containing the customizations


			--- Command Handlers ---
				Implementation of each menu item ("cmd") defined in commands.json

			<command>: {

			enable: function(parent, list, rights) {
				Parameters
					parent: Object containing information about the current container
					list: Array of selected list items
					rights: Object containing access rights


				Returns true or false 
					true: show menu item
					false: hide menu item
			},

			do: function(parent, list) {
				Parameters
					parent: Object containing information about the current container
					list: Array of selected list items


				Code that is executed when menu item is selected


				Returns true or false 
					true: 
					false: 
			}
		}
		
	================================================================================
	The following command handler examples show different types of interactions
	================================================================================ */
	

	/* -----------------------------------------------------------------------------
			Initating an action with no further inputs
	--------------------------------------------------------------------------------
		{
			"cmd": "punch_clock",
			"label": "Punch clock",
			"type": ["container"]
		}
	*/
		punch_clock: {
			
			enable: function(parent, list, rights) {
				// Enable only when nothing is selected
				return !list || list.length == 0;
			},
			
			do: function(parent, list) {
				//
				// Code: Add time stamped entry
				//
				// Give user informational feedback that something happened
				//	Syntax:
				//		notify.info(<title>,<message>)
				//
				ICC.globals.notify.info('Punch Clock', `Have a nice day!`);
				return true;
			}
		},
		
		
	/* -----------------------------------------------------------------------------
			Initating an action with minimal inputs using custom form
	--------------------------------------------------------------------------------
		{
			"cmd": "time_sheet",
			"label": "Time sheet",
			"type": ["container", "properties"]
		}
	*/
		time_sheet: {
			
			enable: function(parent, list, rights) {
				// Enable when either nothing is selected or only 1 item
				return !list || (!!list && list.length <= 1);
			},
			
			do: function(parent, list) {
				// Pre-populate form defaults
				if (!list){
					// Nothing is selected...
					formDefaults = {}; // ... nothing to default
				} else {
					// Single item selected...
					formDefaults = Object.assign({}, list[0]); // ...use the meta data of the selected item
				}
				
				// Display custom form to the user...
				//	Syntax:
				//		runform(<defaults>,<vendor>,<form name>,<title>)
				//	Note:
				//		Custom form must be defined in forms.json
				ICC.globals.runform(formDefaults, 'demo', 'time_sheet', 'Time sheet').then(
					res => {
						// Handle response once the form has been dismissed
						let success = res.success; // true: 'ok', false: 'cancel'
						if (!!success){
							// Note:
							//	The response will only contain form inputs that have changed
							//	You will have to refer to the defaults for anything that hasn't changed
							client = (res.data.CLIENT_ID) ?  res.data.CLIENT_ID : list[0].CLIENT_ID;
							matter = (res.data.MATTER_ID) ? res.data.MATTER_ID : list[0].MATTER_ID;
							time = (res.data.TIME) ? res.data.TIME : "0";
							billable = (res.data.BILLABLE == "Y") ? "":"non-";
							//
							// Code: Add current user's hours against against the appropriate Client and Matter
							//
							// Give user informational feedback that something happened
							//	Syntax:
							//		notify.info(<title>,<message>)
							//
							action = 'Logged ' + time + ' ' + billable + 'billable hours against:';
							bodyparts = [];
							bodyparts.push(`${action}`);
							bodyparts.push(`${client}`);
							bodyparts.push(`${matter}`);
							body = bodyparts.join('\r\n');
							ICC.globals.notify.info('Time Sheet', `${body}`);
						}
					}, err => {
						// Error case
						// 	Give user informational feedback that something bad happened
						//	Syntax:
						//		notify.warning(<title>,<message>)
						ICC.globals.notify.warning('Custom Code Says', `err: ${err.toString()}`);
					}
				);
				return true;
			}
		},
	
	/* -----------------------------------------------------------------------------
			Initating an action with no further inputs
				Access internal information using custom SQL (REST API)
				Display information using custom forms
	--------------------------------------------------------------------------------
		{
			"cmd": "rolodex",
			"label": "Rolodex",
			"type": ["container", "properties"]
		}
	*/
		rolodex: {
			
			enable: function(parent, list, rights) {
				// Enable when either nothing is selected or only 1 item
				return !list || (!!list && list.length <= 1);
			},
			
			do: function(parent, list) {
				// Retrieve information for the appropriate user (self or author)
				//	Syntax:
				//		custom/sql/<vendor>/<sql id>?library=<library>  (optional parameters)
				// Note:
				//	Only predefined statements will be executed
				//		<sql id> is the access to the defined SQL statement found in sql.py
				
				if (!!list && list.length==1){
					urlRequest = 'custom/sql/demo/aboutuser?library=' + ICC.globals.primarylibrary + '&AUTHOR=' + list[0].AUTHOR_ID;
				} else {
					urlRequest = 'custom/sql/demo/aboutme?library=' + ICC.globals.primarylibrary;
				}
				// Have the client issue a fully constructed request to the REST API
				//	Syntax:
				//		restrequest(<method>,<url>)
				ICC.globals.restrequest("GET", urlRequest).then(
					res => {
						// Handle response from the request
						// Display custom form to the user...
						//	Syntax:
						//		runform(<defaults>,<vendor>,<form name>,<title>)
						//	Note:
						//		Custom form must be defined in forms.json
						ICC.globals.runform(res.data.list[0], 'demo', 'rolodex_card', 'Rolodex card').then(
							res => {
								test = 'hello';
							}, err => {
								ICC.globals.notify.warning('Custom Code Says', `err: ${err.toString()}`);
							}
						);
					}
				);
				return true;
			}
		},
		
	/* -----------------------------------------------------------------------------
			Initating an action with no further inputs
				Access external information using custom process (REST API)
				Display information using custom forms
	--------------------------------------------------------------------------------
		{
			"cmd": "stock_ticker",
			"label": "Stock ticker",
			"type": ["container"]
		}
	*/
	
		stock_ticker: {
			
			enable: function(parent, list, rights) {
				return !list || list.length == 0;
			},
			
			do: function(parent, list) {
				// Retrieve information from an external process/service
				//	Syntax:
				//		custom/process/<vendor>/<process id>?library=<library>  (optional parameters)
				// Note:
				//	Only predefined statements will be executed
				//		<process id> is the access to the defined SQL statement found in process.py
				
				const urlParameter = 'https%3A//query1.finance.yahoo.com/v7/finance/quote?symbols=OTEX';
				const urlRequest = 'custom/process/demo/geturl?library=' + ICC.globals.primarylibrary + '&url=' + urlParameter;
				// Have the client issue a fully constructed request to the REST API
				//	Syntax:
				//		restrequest(<method>,<url>)
				ICC.globals.restrequest("GET", urlRequest).then(
					res => {
						// Handle response from the request
						let price = "";
						let nQuotes = !!res.data && !!res.data.quoteResponse && !!res.data.quoteResponse.result ? res.data.quoteResponse.result.length : 0;
						// Give user informational feedback
						//	Syntax:
						//		notify.info(<title>,<message>)
						//
						bodyparts = [];
						if (nQuotes){
							price = res.data.quoteResponse.result[0].regularMarketPrice;
							bodyparts.push(`OTEX last price: ${price}`);
						}
						bodyparts.push(".\r\n");
						bodyparts.push("Find latest news at:");
						bodyparts.push("https://www.opentext.com/about/press-releases");
						body = bodyparts.join('\r\n');
						ICC.globals.notify.info('Stock ticker', `${body}`);
					}, err => {
						// Error case
						//	Give user informational feedback that something bad happened
						//	Syntax:
						//		notify.warning(<title>,<message>)
						ICC.globals.notify.warning('Custom Code Says', `err: ${err.toString()}`);
					}
				);
				return true;
			}
		},

	/* -----------------------------------------------------------------------------
			Initating an action with minimal inputs using custom form
	--------------------------------------------------------------------------------
		{
			"cmd": "review_document",
			"label": "Review",
			"type": ["container", "properties"]
		}
	*/	
		review_document: {
			enable: function(parent, list, rights) {
				if (!!list && list.length == 1){
					if (list[0].STATUS == "0"){
						return true;
					}
				}
				return false;
			},
			
			
			do: function(parent, list) {
				// Display custom form to the user...
				//	Syntax:
				//		runform(<defaults>,<vendor>,<form name>,<title>)
				//	Note:
				//		Custom form must be defined in forms.json
				formDefaults = {}; // Nothing to default
				ICC.globals.runform(formDefaults, 'demo', 'review_document', 'Review request').then(
					res => {
						// Handle response once the form has been dismissed
						let success = res.success; // true: 'ok', false: 'cancel'
						if (!!success){
							// Make the document read-only by updating the profile
							const data = {"%STATUS": '%MAKE_READ_ONLY'};
							const url = list[0].type + '/' + list[0].id + '/profile?library=' + list[0].lib;
							// Have the client issue a fully constructed request to the REST API
							//	Syntax:
							//		restrequest(<method>,<url>)
							ICC.globals.restrequest("PUT", url, data).then(
								res => {
									// Refresh the current container to update the profile change
									ICC.globals.refresh();
								}, err => {
									ICC.globals.notify.warning('Custom Code Says', `err: ${err.toString()}`);
								}
							);
							return true;
						}
					}
				);
				return true;
			}
		}
};