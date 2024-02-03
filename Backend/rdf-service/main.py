from flask import Flask, request, jsonify
from SPARQLWrapper import SPARQLWrapper, JSON
from src import userquery

app = Flask(__name__)

SPARQL_ENDPOINT_URL = "http://34.16.185.124:9999/blazegraph/sparql"

def execute_sparql_query(query, append_id=False):
    sparql = SPARQLWrapper(SPARQL_ENDPOINT_URL)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
    except Exception as e:
        return {"error": str(e)}, 500

    output = []
    for result in results["results"]["bindings"]:
        item_info = {var: result[var]["value"] for var in result}
        if append_id:
            item_id = item_info.get('user', '').rsplit('/', 1)[-1]
            item_info['id'] = item_id
        output.append(item_info)
    return output

def prefixed_query(query_body):
    return f"""
    PREFIX ex: <http://example.com/>
    {query_body}
    """

def add_limit_clause(query_body, limit):
    if limit and limit.isdigit():
        query_body += f" LIMIT {limit}"
    return query_body

@app.route('/query/books', methods=['GET'])
def get_books():
    limit = request.args.get('limit')
    query_body = add_limit_clause("""
    SELECT ?book ?title ?averageRating ?imageUrl (GROUP_CONCAT(DISTINCT ?authorName; separator=", ") AS ?authors) WHERE {
      ?book a ex:Book;
            ex:title ?title;
            ex:averageRating ?averageRating;
            ex:imageUrl ?imageUrl.
      OPTIONAL {
        ?ba ex:book ?book;
            ex:author ?author.
        ?author ex:name ?authorName.
      }
    } GROUP BY ?book ?title ?averageRating ?imageUrl
    """, limit)
    return jsonify({"results": execute_sparql_query(prefixed_query(query_body))})

@app.route('/query/cities', methods=['GET'])
def get_cities():
    limit = request.args.get('limit')
    query_body = add_limit_clause("""
    SELECT ?city ?name WHERE {
      ?city a ex:City;
            ex:name ?name.
    }
    """, limit)
    return jsonify({"results": execute_sparql_query(prefixed_query(query_body))})

@app.route('/query/companies', methods=['GET'])
def get_companies():
    limit = request.args.get('limit')
    query_body = add_limit_clause("""
    SELECT ?company ?name WHERE {
      ?company a ex:Company;
               ex:name ?name.
    }
    """, limit)
    return jsonify({"results": execute_sparql_query(prefixed_query(query_body))})

@app.route('/query/skills', methods=['GET'])
def get_skills():
    limit = request.args.get('limit')
    query_body = add_limit_clause("""
    SELECT ?skill ?name WHERE {
      ?skill a ex:Skill;
             ex:name ?name.
    }
    """, limit)
    return jsonify({"results": execute_sparql_query(prefixed_query(query_body))})

@app.route('/query/authors', methods=['GET'])
def get_authors():
    limit = request.args.get('limit')
    query_body = add_limit_clause("""
    SELECT ?author ?name WHERE {
      ?author a ex:Author;
              ex:name ?name.
    }
    """, limit)
    return jsonify({"results": execute_sparql_query(prefixed_query(query_body))})

@app.route('/query', methods=['POST'])
def query_rdf_store():
    sparql_query = request.json.get('query')
    if not sparql_query:
        return jsonify({"error": "Missing 'query' in request body"}), 400
    return jsonify({"results": execute_sparql_query(sparql_query)})

@app.route('/query/books_by_ids', methods=['POST'])
def query_by_ids():
    user_ids = request.json.get('ids')
    if not user_ids:
        return jsonify({"error": "Missing 'ids' in request body"}), 400
    sparql_query = userquery.generate_sparql_query(user_ids)
    return jsonify({"results": execute_sparql_query(sparql_query, append_id=True)})

if __name__ == '__main__':
    app.run(port=5001)
