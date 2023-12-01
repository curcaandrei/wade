import random
from rdflib import Graph, Literal, RDF, URIRef 
from rdflib.namespace import Namespace,FOAF
org = Namespace("http://schema.org/")
custom_namespace=Namespace("http://custom.org/")
companies=['Facebook','Microsoft','Linkedin','Amd','Luxoft','Amazon']
hobbies=['play_piano','chess','table_tennis','esports','hiking','music','books','movies']
fnames=['Tobby','Andrew','Mohammed','Harry','John','Thiago','Manuel','Julian','Elliot','Michail','Bernardo']
lnames=['Mguaire','Salah','Kane','Johnson','Alcantara','Akanji','Alvarez','Andersen','Antonio','Silva']
skills=['python','React','java','spring','databases','photoshop','angular','nodejs','C#','C++','go','turbo_pascal','ui/ux','ML']
companies_uris=[]
hobbies_uris=[]
skills_uris=[]
g = Graph()
def generate_companies():
    for company in companies:
        uriComp=URIRef(custom_namespace+company)
        companies_uris.append(uriComp)
        g.add((uriComp, RDF.type, org.Organization))
        g.add((uriComp,org.name,Literal(company)))

def generate_hobbies():
    for hobby in hobbies:
        hobbyURI=URIRef(custom_namespace+'hobby/'+hobby)
        hobbies_uris.append(hobbyURI)
        g.add((hobbyURI, RDF.type, org.Hobby))
        g.add((hobbyURI, custom_namespace.label, Literal(hobby)))
def generate_skills():
    for skill in skills:
        skillURI=URIRef(custom_namespace+'skill/'+skill)
        skills_uris.append(skillURI)
        g.add((skillURI,RDF.type,custom_namespace.Skill))
        g.add((skillURI,custom_namespace.label,Literal(skill)))

def generate_people():
    for person_id in range(1,5):
        name = random.choice(fnames) + '_' + random.choice(lnames)
        peopURI=URIRef(custom_namespace+name)
        g.add((peopURI, RDF.type, FOAF.Person))
        g.add((peopURI, org.name, Literal(name)))
        g.add((peopURI, org.worksFor, random.choice(companies_uris)))
        add_hobbies_to_people(peopURI)
        add_skill_to_people(peopURI)

def add_hobbies_to_people(personUri):
    chosen_hobbies=[random.choice(hobbies_uris) for _ in range(random.randint( 1,3))]
    for chhoby in chosen_hobbies:
        g.add((personUri, org.hobby, chhoby))
def add_skill_to_people(personUri):
    chosen_skills=[random.choice(skills_uris) for _ in range(random.randint( 1,3))]
    for skill in chosen_skills:
        g.add((personUri, custom_namespace.hasSkill, skill))

def serialize_graph():
    output_file = "people_data.rdf"
    g.serialize(output_file, format="xml")
    #print(g.serialize(format='xml'))

#run fuctions
def main():
    generate_companies()
    generate_hobbies()
    generate_skills()
    generate_people()
    serialize_graph()

main()