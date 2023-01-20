# pmodules aka. python modules
A collection of useful scripts in python.

## ConfigParser
Allows loading a json file and working with it in a simple and abstract way.

## MQTT
Allows the abstraction of dealing with mqtt messages based on the paho client.
The ``MqttListener`` class allows subscribing to topics and handling messages. A callback function is assigned to the listener.
With the help of the ``MqttSender`` class messages can be published in an arbitrary topic.
In case of a disconnect, the connection is automatically re-established.

## Logger
A logger class which gives the possibility to log functions using decorators.
At the moment it includes a simple approach of profiling as well

### Usage
import with: ``from log import *``
This will include the log-instance.

An example can be found directly in the file.  
Initialize the logger in the main function:
``log.init(args)`` with the args:  
``file_path`` - the filename including a path. The folder must exist.  
``log_level`` - set the level of logging which will be saved to the file.  
``verbose`` - print the log to the terminal.  
``use_subprocess`` - use a subprocess (python's multiprocessing) for saving the log to a file.  
``date_in_name`` - adds the current date and time between the filename and the file ending: ``log.txt`` -> ``log{date}``  
Close the logger at the end for closing the subprocess/filewriter with ``log.close()``

decorators:  
``@log.debug`` - saves as much information as possible  
``@log.default`` - saves an adequate amount of information  
``@log.info`` - saves less information  
``@log.profile`` - profiles the function

methods:  
``print_info(input_string)`` - prints the input string as an info message to the terminal and logs it to the file  
``print_error(input_string)`` - prints the input string as an error message to the terminal and logs it to the file  
``log(input)`` - directly log a string  
``print_profiling()`` - prints the results of the profiles functions


log levels:  
``DEBUG``, ``DEFAULT``, ``INFO``
