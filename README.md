# AppFirst Object Library
Python library that I use with AppFirst's afapi library to access data as objects and perform common operations. 
[Note: At this time I load this object file through the python shell, I hope to change it into a pip module soon]

## Server object
The server object is instantiated with a Server ID. Once initiated, it collects all of the process data for that server, including the /data/ and /detail/ endpoints of the API.

### Instantiation
<pre>
python -i afobject.py
api = AppFirstAPI('email','access_token')
myServer = Server(server_id)
</pre>

### Data Structure
This object converts all the core system items into objects, and then imports all server processes, and all process data, and details.
<pre>
myServer.hostname = string
myServer.id = int
myServer.processes = list of PIDs
</pre>
In the PID list, you can access the following keys: 
- info (general process info including name and arguments)
- data (specific info including cpu, file and socket activity)
- detail (specific info including File handles, Registry Keys and Threads)

### Methods
*myServer.search_process_info(search,field='args')*<br/>
Method to search process info by field. Defaults to search for strings in command line arguments. returns list of PIDs
*myServer.search_process_data(search,context='files')*<br/>
Method to search process data. Defaults to comparing search value by operator.gt to socket_num. returns list of PIDs
*myServer.search_process_detail(search,comparator=operator.gt,field='socket_num')*<br/>
Method to search process details. Defaults to searchg for string in file handles accessed. returns list of PIDs

### General Methods
*generateRules(list)*
This method takes a list of process names and converts them into a rule list for passing to afapi.create_process_template

#### Example Template Creation
<pre>
api = AppFirstAPI('email','api key')
myServer = Server(server id)
results = Server.search_process_info('mcafee') - Returns a list of processes with 'mcafee' in the command line argument
procList = []
for proc in results:
    procList.append(myServer.processes[proc]['info']['name'])
count = 1
name = "Component "
rules = generateRules(procList)
for rule in rules:
    tempRule = []
    tempRule.append(rule)
    print (api.create_process_template(name=name+str(count),rules=tempRule))[1]
    count += 1
</pre>
