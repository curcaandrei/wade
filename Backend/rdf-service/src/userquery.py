
def generate_sparql_query(user_ids):
    values_clause = "VALUES ?user { " + " ".join(f"<http://example.com/user/{id}>" for id in user_ids) + " }"
    query = f"""
    PREFIX ex: <http://example.com/>
    SELECT ?user ?userName ?email ?city
    WHERE {{
      {values_clause}
      ?user ex:userName ?userName .
      OPTIONAL {{ ?user ex:email ?email . }}
      OPTIONAL {{ ?user ex:city ?city . }}
    }}
    """
    return query
