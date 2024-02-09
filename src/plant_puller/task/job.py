from plant_puller.task.util import Status, Type
from opensearchpy import OpenSearch
from opensearchpy.helpers.search import Search
from uuid import uuid4
from datetime import datetime

class Job:
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
        self.docstore = docstore
        self.name = name
        self.type = Type.Job

        # If we are resuming the most recent job fetch it's state
        if resume:
            state = self._fetch_job_state()
            for key in state: 
                setattr(self, key, state[key])
        else:
            self.id = uuid4()
            self.created = datetime.now().isoformat()

            # Small note status must always be the last property set
            self.status = Status.Created

    def __dict__(self):
        representation = {
            "name": self.name,
            "type": self.type,
            "id": self.id,
            "created": self.created, 
            "status": self.status
        }
        return representation

    @property
    def status(self):
        """status (Status): Current job status. *Note: changing status
        will trigger a write of Job state
        """
        return self._status

    @status.setter
    def status(self, status):
        if status not in Status:
            raise Exception("Invalid Status Set")
        self._status = status
        self._push_job_state()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self._push_job_state()

    def _fetch_job_state(self):
        """Get the most recent matching job. 

        Finds the properties of the most recent job matching type job
        and with the matching job name. Will grab all the attributes 
        and set them for the job. 
        """
        resp = self.docstore.search(
            body={
                "query": {
                    "bool": {
                        "must": [
                            {"match": {
                                "type": Type.Job,
                            }},
                            {"match": {
                                "name": self.name
                            }}
                        ]
                    }
                },
                "sort": [{
                    "created": {
                        "order": "desc"
                    }
                }]
            }, 
            index='plant-puller-state', 
            size=1
        )

        # If no documents returned raise an exception
        if 'hits' not in resp or resp['hits']['total']['value'] == 0:
            raise Exception('No jobs to fetch')

        return resp['hits']['hits'][0]['_source']

    def _push_job_state(self):
        """Takes the current state of a job and pushes to docstore. 

        Here we are pushing the state for the job into our docstore. 
        This utilizes the self.__dict__() for encoding the job. 
        """
        self.docstore.index(
            index='plant-puller-state',
            body=self.__dict__()
        )