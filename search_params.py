descriptions = {"term": "The full-text query term",
                "title": "Search in the title field",
                "topics": "Search within a notice's topics",
                "tags": "Search within a notice's tags",
                "jurisdictions": "Search within a notice's jurisdictions",
                "sender_name": "Search in the sender's name",
                "principal_name": "Search in the principal's name",
                "recipient_name": "Search in the recipient's name",
                "works": "Search within a work's description",
                "action_taken": "Search based on the action taken on a notice.",
                "topic_facet": "Filter on topics facet",
                "sender_name_facet": "Filter on sender_name facet",
                "principal_name_facet": "Filter on principal_name facet",
                "recipient_name_facet": "Filter on recipient_name facet",
                "tag_list_facet": "Filter on a tag",
                "country_code_facet": "Filter on the recipient's country code",
                "language_facet": "Filter on the notice language code",
                "action_taken_facet": "Filter on the action_taken facet",
                "date_received_facet": "The date range (in microseconds since the unix epoc) separated by \"..\"",
                "page": "The page you're requesting - defaults to the first page of results.",
                "per_page": "The number of results per page. Defaults to 10.",
                "sort_by": "One of date_received asc, date_received desc, relevancy asc, or relevancy desc. Defaults to relevancy asc."}

require_all_names = ["term",
 "title",
 "topics",
 "tags",
 "jurisdictions",
 "sender_name",
 "principal_name",
 "recipient_name",
"works"]


class Param():
    def generate_request(self, query_list, req_all=False):
        req = self.name
        if req_all:
            req += "_require_all"
        req += "="
        for i in query_list:
            req += i
            if query_list.index(i) != len(query_list) - 1:
                req += "+"
        return req

    def __init__(self, name, description, require_all):
        self.name = name
        self.description = description
        self.require_all = require_all

PARAMS = {}
r = 0
for n,d in descriptions.iteritems():
    r = False
    if n in require_all_names:
        r = True
    PARAMS[n] = Param(n, d, r)
