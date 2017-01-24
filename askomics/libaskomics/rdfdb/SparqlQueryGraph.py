import logging
# from pprint import pformat
# from string import Template

# from askomics.libaskomics.rdfdb.SparqlQuery import SparqlQuery
# from askomics.libaskomics.ParamManager import ParamManager
from askomics.libaskomics.rdfdb.SparqlQueryBuilder import SparqlQueryBuilder

class SparqlQueryGraph(SparqlQueryBuilder):
    """
    This class contain method to build a sparql query to
    extract data from public and private graph
    It replace the template files
    """

    def __init__(self, settings, session):
        SparqlQueryBuilder.__init__(self, settings, session)
        self.log = logging.getLogger(__name__)

    def query_exemple(self):
        """
        Query exemple. used for testing
        """
        return self.build_query_from_template({
            'select': '?s ?p ?o',
            'query': '?s ?p ?o .'
            })

    def get_start_point(self):
        """
        Get the start point and in which graph they are
        """
        self.log.debug('---> get_start_point')
        return self.build_query_from_template({
            'select': '?nodeUri ?nodeLabel ?g',
            'query': '?nodeUri displaySetting:startPoint "true"^^xsd:boolean .\n' +
                     '\t?nodeUri rdfs:label ?nodeLabel'
        })

    def get_list_named_graphs(self):
        """
        Get the list of named graph
        """
        self.log.debug('---> get_list_named_graphs')
        return self.build_query_from_template({
            'select': '?g',
            'query': '?s ?p ?o'
        })

    def get_if_positionable(self, uri):
        """
        Get if an entity is positionable
        """
        self.log.debug('---> get_if_positionable')
        return self.build_query_from_template({
            'select': '?exist',
            'query': 'BIND(EXISTS {<' + uri + '> displaySetting:is_positionable "true"^^xsd:boolean} AS ?exist)'
        })

    def get_common_pos_attr(self, uri1, uri2):
        """
        Get the common positionable attributes between 2 entity
        """
        self.log.debug('---> get_common_pos_attr')
        return self.build_query_from_template({
            'select': '?uri ?pos_attr ?status',
            'query': 'VALUES ?pos_attr {:position_taxon :position_ref :position_strand }\n' +
                     '\tVALUES ?uri {<'+uri1+'> <'+uri2+'> }\n' +
                     '\tBIND(EXISTS {?pos_attr rdfs:domain ?uri} AS ?status)'
        })

    def get_all_taxons(self):
        """
        Get the list of all taxon
        """
        self.log.debug('---> get_all_taxons')
        return self.build_query_from_template({
            'select': '?taxon',
            'query': ':taxonCategory displaySetting:category ?URItax .\n' +
                     '\t?URItax rdfs:label ?taxon'
        })

    def get_abstraction_attribute_entity(self, entities):
        """
        Get all attributes of an entity
        """
        return self.build_query_from_template({
            'select': '?entity ?attribute ?labelAttribute ?typeAttribute',
            'query': '?entity rdf:type owl:Class .\n' +
                     '\t?attribute displaySetting:attribute "true"^^xsd:boolean .\n\n' +
                     '\t?attribute rdf:type owl:DatatypeProperty ;\n' +
                     '\t           rdfs:label ?labelAttribute ;\n' +
                     '\t           rdfs:domain ?entity ;\n' +
                     '\t           rdfs:range ?typeAttribute .\n\n' +
                     '\tVALUES ?entity { ' + entities + ' }\n' +
                     '\tVALUES ?typeAttribute { xsd:decimal xsd:string }'
        })

    def get_abstraction_relation(self, prop):
        """
        Get the relation of an entity
        """
        return self.build_query_from_template({
            'select': '?subject ?relation ?object',
            'query': '?relation rdf:type ' + prop + ' ;\n' +
                     '\t          rdf:domain ?subject ;\n' +
                     '\t          rdfs:range ?object .\n' +
                     '\t?subject rdf:type owl:Class .\n' +
                     '\t?object rdf:type owl:Class\n'
            })


    def get_abstraction_entity(self, entities):
        """
        Get theproperty of an entity
        """
        return self.build_query_from_template({
            'select': '?entity ?property ?value',
            'query': '?entity ?property ?value .\n' +
                     '\t?entity rdf:type owl:Class .\n' +
                     '\tVALUES ?entity { ' + entities + ' }'
            })

    def get_abstraction_positionable_entity(self):
        """
        Get all positionable entities
        """
        return self.build_query_from_template({
            'select': '?entity',
            'query': '?entity rdf:type owl:Class .\n' +
                     '\t?entity displaySetting:is_positionable "true"^^xsd:boolean .'
            })

    def get_abstraction_category_entity(self, entities):
        """
        Get the category of an entity
        """
        return self.build_query_from_template({
            'select': '?entity ?category ?labelCategory ?typeCategory',
            'query': '?entity rdf:type owl:Class .\n' +
                     '\t?typeCategory displaySetting:category [] .\n' +
                     '\t?category rdf:type owl:ObjectProperty ;\n' +
                     '\t            rdfs:label ?labelCategory ;\n' +
                     '\t            rdfs:domain ?entity;\n' +
                     '\t            rdfs:range ?typeCategory\n' +
                     '\tVALUES ?entity { ' + entities + ' }'
            })

    def get_class_info_from_abstraction(self, node_class):
        """
        get 
        """
        return self.build_query_from_template({
            'select': '?relation_label',
            'query': '?class rdf:type owl:Class .\n' +
                     '\tOPTIONAL { ?relation rdfs:domain ?class } .\n' +
                     '\tOPTIONAL { ?relation rdfs:range ?range } .\n' +
                     '\tOPTIONAL { ?relation rdfs:label ?relation_label } .\n' +
                     '\tVALUES ?class { :' + node_class + ' }'
            })
