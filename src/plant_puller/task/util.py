from collections import namedtuple
from uuid import uuid4

StatusDict = namedtuple('Status', ['Created', 'Started', 'Completed', 'Failed'])
Status = StatusDict('Created', 'Started', 'Completed', 'Failed')

TypeDict = namedtuple('Type', ['Job', 'TaskList', 'Task'])
Type = TypeDict('Job', 'TaskList', 'Task')
