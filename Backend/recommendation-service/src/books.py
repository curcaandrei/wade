def form_sparql_query_books(data):
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


def process_rdf_data_books(data):
    return data
