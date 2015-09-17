from afapi import AppFirstAPI
import operator
import json
#import types

class Server(object):
  def __init__(self,sID):
    # Define Object Data Structure
    self.processes = {}

    # Initialize Object with API data
    response,code = api.get_server(sID)
    try:
        for key in response:
            setattr(self,key,response[key])
    except:
        print "API returned {0} during initialization".format(code)
    
    # Populate Process data on initialization
    response, code = api.get_server_processes(self.id)
    for process in response['data']:
      self.processes[process['pid']] = {}
      self.processes[process['pid']]['info'] = process
      procData,code = api.get_process_data(uid=process['uid']) # realize I'm reusing 'code'
      if len(procData['data']) == 1: # Single snapshot
        self.processes[process['pid']]['data'] = procData['data'][0]
      else:
        self.processes[process['pid']]['data'] = procData['data']
      procData,code = api.get_process_details(uid=process['uid'])
      self.processes[process['pid']]['detail'] = procData['data']

      
  def search_process_info(self, search, field='args'): 
    output = []
    for process in self.processes:
      if search in self.processes[process]['info'][field]:
        output.append(self.processes[process]['info']['pid'])
    return output

  def search_process_detail(self, search, context='files'):
    output = []
    for process in self.processes:
      try:
        for item in self.processes[process]['detail'][context]:
          if search in item:
            output.append(self.processes[process]['info']['pid'])
      except KeyError:
        pass     
    return list(set(output)) # Return only the unique values of the list for multiple-matches within a single process
  
  def search_process_data(self, search, comparator=operator.gt, field='socket_num'): 
    output = []
    for process in self.processes:
      if comparator(self.processes[process]['data'][field],search):
        output.append(self.processes[process]['info']['pid'])
    return output

  def to_JSON(self):
    return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

  def save(self, filename):
    out_file = open(filename,'w')
    out_file.write(self.to_JSON())
    out_file.close()

# Non-object methods for data manipulation
def generateRules(proclist):
  rules = []
  for item in proclist:
    string = 'Processes matching {0} with arguments matching *'.format(item)
    rules.append(string)
  return rules

