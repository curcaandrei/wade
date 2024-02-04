
def generate_sparql_query(book_ids):
    values_clause = "VALUES ?book { " + " ".join(f"<http://example.com/book/{id}>" for id in book_ids) + " }"
    query = f"""
    PREFIX ex: <http://example.com/>
    SELECT ?book (REPLACE(STR(?book), "^.*/book/", "") AS ?bookId) ?title ?averageRating ?imageUrl
    WHERE {{
      {values_clause}
      ?book ex:title ?title .
      OPTIONAL {{ ?book ex:averageRating ?averageRating . }}
      OPTIONAL {{ ?book ex:imageUrl ?imageUrl . }}
    }}
    """
    return query
