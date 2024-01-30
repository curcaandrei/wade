from flask import Flask, request, jsonify
from SPARQLWrapper import SPARQLWrapper, JSON

app = Flask(__name__)

@app.route('/query', methods=['POST'])
def query_rdf_store():
    sparql_query = request.json['query']

    # Interact with RDF store using the SPARQL query
    rdf_store_result = execute_sparql_query(sparql_query)

    # Return the result
    return jsonify(rdf_store_result)

def execute_sparql_query(query):
    endpoint_url = "http://34.16.185.124:9999/blazegraph/sparql"
    sparql = SPARQLWrapper(endpoint_url)

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    results = sparql.query().convert()

    output = []
    for result in results["results"]["bindings"]:
        output.append({var: binding[var]["value"] for var in binding})

    return {"results": output}

if __name__ == '__main__':
    app.run(port=5000)
