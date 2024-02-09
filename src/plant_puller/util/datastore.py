from os import getenv
from opensearchpy import OpenSearch
from dotenv import load_dotenv

load_dotenv()
host = getenv('HOST', "localhost")
port = getenv('PORT', 9200)
auth = ('admin', 'admin') # For testing only. Don't store credentials in code.

def create_docstore():
    return OpenSearch(
        hosts = [{'host': host, 'port': port}],
        http_auth = auth,
        use_ssl = True,
        verify_certs = False,
        ssl_show_warn=False
    )

if __name__=="__main__":
    docstore = create_docstore(hosts=[{'host': 'localhost', 'port': 9200}])
    print(docstore.cat.health())