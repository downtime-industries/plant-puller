from plant_puller.task.job import Job
from plant_puller.task.task import Task
from plant_puller.task.util import Status
from plant_puller.util.datastore import create_docstore

docstore = create_docstore()

class PlantFinder(Job):
    def __init__(self, docstore, resume: bool = False):
        super().__init__(docstore=docstore, name="plant-finder", resume=resume)
        self.plant_finder_prompt = "I NEED PLANTS"



def FindSitesWithPlants(Task):
    """Finds sites that list common houseplants.

    Creates sample queries and then searches Google
    using the provided sample queries. 

    Attributes: 
        prompt (str): LLM prompt for generating sample queries
        queries (list(str)): List of queries to search google for
        num_queries (int): Number of queries to generate
    """
    
    def __init__(self):
        pass

    def run(self):
        # prompt LLM 
        # return and clean results
        # google search for results
        # store results/urls in index
        pass

class ScrapePlantSite(Task):
    """Downloads pages identified in the previous step

    """
    def __init__(self):
        pass

    def run(self):
        # read from URL queue
        # fetch page
        # clean page
        # store pages
        pass


class ExtractPlantList(Task):
    """Extract plant names from page

    """
    def __init__(self):
        pass

    def run(self):
        # read from URL queue
        # fetch page
        # clean page
        # store pages
        pass

if __name__=="__main__":
    pass