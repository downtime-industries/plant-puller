from plant_puller.task.job import Job
from plant_puller.task.util import Status
from plant_puller.util.datastore import create_docstore

hosts=['127.0.0.1']
docstore = create_docstore(hosts=hosts)

class PlantFinder(Job):
    def __init__(self, docstore, resume: bool = False):
        print("1: ", type(docstore)) 
        super().__init__(docstore=docstore, name="plant-finder", resume=resume)

    def __dict__(self):
        return super().__dict__()

if __name__=="__main__":
    with PlantFinder(docstore=docstore) as test:
        test.status = Status.Started

    print("Finished")

    with PlantFinder(docstore=docstore, resume=True) as test2:
        print(test2.status)