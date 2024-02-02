from flask import Flask, request, jsonify
from SPARQLWrapper import SPARQLWrapper, JSON
from src import userquery

app = Flask(__name__)

@app.route('/query', methods=['POST'])
def query_rdf_store():
    sparql_query = request.json['query']

    rdf_store_result = execute_sparql_query(sparql_query)

    return jsonify(rdf_store_result)

@app.route('/query_by_ids', methods=['POST'])
def query_by_ids():
    user_ids = request.json['ids']

    # Construct SPARQL query for the provided user IDs
    sparql_query = userquery.generate_sparql_query(user_ids)

    # Interact with RDF store using the constructed SPARQL query
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
        user_info = {var: result[var]["value"] for var in result}
        user_id = user_info['user'].rsplit('/', 1)[-1]
        user_info['id'] = user_id
        output.append(user_info)

    return {"results": output}


if __name__ == '__main__':
    app.run(port=5001)
