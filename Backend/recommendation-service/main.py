from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/recommendations', methods=['POST'])
def get_recommendations():
    data = request.json

    # Form the SPARQL query based on the received data
    sparql_query = form_sparql_query(data)

    # Communicate with RDF Service
    response = requests.post('https://rdf-dot-diesel-nova-412314.ew.r.appspot.com/query', json={'query': sparql_query})
    rdf_data = response.json()

    processed_data = process_rdf_data(rdf_data)
    return jsonify(processed_data)

def form_sparql_query(data):
    # Example SPARQL query formation based on user preferences
    genre = data.get("preferences", {}).get("genre", "")
    author = data.get("preferences", {}).get("author", "")
    query = f"""
        PREFIX ex: <http://example.org/>
        SELECT ?book
        WHERE {{
            ?book ex:genre "{genre}" ;
                  ex:author "{author}" .
        }}
    """
    return query

def process_rdf_data(data):
    return data

if __name__ == '__main__':
    app.run(port=5000)
