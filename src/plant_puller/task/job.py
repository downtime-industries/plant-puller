from plant_puller.task.util import Status, Type
from opensearchpy import OpenSearch
from opensearchpy.helpers.search import Search
from uuid import uuid4
from datetime import datetime

class Job:
    def __init__(self, docstore: OpenSearch, name: str, resume: bool):
        print("2: ", type(docstore))
        self.docstore = docstore
        self.name = name
        self.type = Type.Job

        # If we are resuming the most recent job fetch it's state
        if resume:
            state = self.fetch_job_state()
            for key in state: 
                setattr(self, key, state[key])
        else:
            self._id = uuid4()
            self.status = Status.Created
            self.created = datetime.now().isoformat()

    def __dict__(self):
        return {
            "name": self.name,
            "type": self.type,
            "_id": self._id,
            "created": self.created, 
            "status": self.status
        }

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.push_job_state()
        

    def fetch_job_state(self):
        print(Type(self.docstore))
        return self.docstore.search(
            body={
                "query": {
                    "match": {
                        "type": {
                            "value": Type.Job
                        },
                        "name": {
                            "value": self.name
                        }
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

    def push_job_state(self):
        print(type(self.docstore))
        self.docstore.index(
            index='plant-puller-state',
            body=self.__dict__()
        )