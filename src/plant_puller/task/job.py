from plant_puller.task.util import Status, Type
from opensearchpy import OpenSearch
from opensearchpy.helpers.search import Search
from uuid import uuid4
from datetime import datetime
from plant_puller.task.state_tracker import StateTracker
from collections import OrderedDict

class Job(StateTracker):
    """ Job Class
    
    This class defines an arbitrary standard for creating jobs in Python with stored state in OpenSearch. 
    Every time the class is created it will get all it's parameters. Then as it's state changes or it's
    de-allocated it will store it's state.

    Attributes:
        status (Status): Current state for the job conforming to the options in Status
        name (str): Name of the current job
        docstore (OpenSearch): An instance of the OpenSearch python class
    """
    def __init__(self, docstore: OpenSearch, name: str, resume: bool):
        super().__init__(type=Type.Job, name=name, resume=resume)
        self.step_list = OrderedDict()


    def add_step(self, task_list: TaskList):
        self.step_list.update({task_list.name: task_list})
        

    def run(self):
        pass

