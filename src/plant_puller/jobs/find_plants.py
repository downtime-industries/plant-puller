from plant_puller.task.job import Job
from plant_puller.task.util import Status
from plant_puller.util.datastore import create_docstore

docstore = create_docstore()

class PlantFinder(Job):
    def __init__(self, docstore, resume: bool = False):
        super().__init__(docstore=docstore, name="plant-finder", resume=resume)
        self.plant_finder_prompt = "I NEED PLANTS"


if __name__=="__main__":
    pass