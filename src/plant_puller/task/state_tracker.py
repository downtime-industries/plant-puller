class StateTracker:
    def __init__(self, docstore: OpenSearch, type):
        self.docstore = docstore
        self.name = name
        self.type = type

        # If we are resuming the most recent job fetch it's state
        if resume:
            state = self._fetch_state()
            for key in state: 
                setattr(self, key, state[key])
        else:
            # Small note status must always be the last property set
            # as it triggers a state push
            self.id = uuid4()
            self.created = datetime.now().isoformat()
            self.status = Status.Created


    @property
    def status(self):
        """status (Status): Current status. *Note: changing status
        will trigger a write of Job state
        """
        return self._status


    @status.setter
    def status(self, status):
        if status not in Status:
            raise Exception("Invalid Status Set")
        self._status = status
        self._push_state()


    def __enter__(self):
        return self


    def __exit__(self, type, value, traceback):
        self._push_state()


    def _fetch_state(self):
        """Get the most recent matching state for object. 

        Finds the properties of the most recent item matching type
        and name of the state object. 
        """
        resp = self.docstore.search(
            body={
                "query": {
                    "bool": {
                        "must": [
                            {"match": {
                                "type": self.type,
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
            index='workflow-state', 
            size=1
        )

        # If no documents returned raise an exception
        if 'hits' not in resp or resp['hits']['total']['value'] == 0:
            raise Exception('No state to fetch')

        return resp['hits']['hits'][0]['_source']

    def _push_state(self):
        """Takes the current state and pushes to docstore. 

        Here we are pushing the state into our docstore. 
        This utilizes the self.__dict__() for encoding the object. 
        """
        self.docstore.index(
            index='workflow-state',
            body=self.__dict__()
        )