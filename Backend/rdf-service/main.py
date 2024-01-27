from flask import Flask
from SPARQLWrapper import SPARQLWrapper, JSON

app = Flask(__name__)

@app.route('/query')
def query_rdf():
    endpoint_url = "http://34.16.185.124:9999/blazegraph/sparql"
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery("""
        PREFIX ex: <http://example.org/>
        SELECT ?object
        WHERE {
            ex:subject ex:predicate ?object.
        }
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    output = ""
    for result in results["results"]["bindings"]:
        output += result["object"]["value"] + "\n"

    return output

@app.route('/')
def hello():
    return "RDF-service hello"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
