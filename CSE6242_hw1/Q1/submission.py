import http.client
import json
import csv
import urllib.request
import urllib.parse

my_api_key = 'fa0b74631406cb7e556e50abc1edb711'


#############################################################################################################################
# cse6242 s21
# All instructions, code comments, etc. contained within this notebook are part of the assignment instructions.
# Portions of this file will auto-graded in Gradescope using different sets of parameters / data to ensure that values are not
# hard-coded.
#
# Instructions:  Implement all methods in this file that have a return
# value of 'NotImplemented'. See the documentation within each method for specific details, including
# the expected return value
#
# Helper Functions:
# You are permitted to write additional helper functions/methods or use additional instance variables within
# the `Graph` class or `TMDbAPIUtils` class so long as the originally included methods work as required.
#
# Use:
# The `Graph` class  is used to represent and store the data for the TMDb co-actor network graph.  This class must
# also provide some basic analytics, i.e., number of nodes, edges, and nodes with the highest degree.
#
# The `TMDbAPIUtils` class is used to retrieve Actor/Movie data using themoviedb.org API.  We have provided a few necessary methods
# to test your code w/ the API, e.g.: get_movie_cast(), get_movie_credits_for_person().  You may add additional
# methods and instance variables as desired (see Helper Functions).
#
# The data that you retrieve from the TMDb API is used to build your graph using the Graph class.  After you build your graph using the
# TMDb API data, use the Graph class write_edges_file & write_nodes_file methods to produce the separate nodes and edges
# .csv files for use with the Argo-Lite graph visualization tool.
#
# While building the co-actor graph, you will be required to write code to expand the graph by iterating
# through a portion of the graph nodes and finding similar artists using the TMDb API. We will not grade this code directly
# but will grade the resulting graph data in your Argo-Lite graph snapshot.
#
#############################################################################################################################


class Graph:

    # Do not modify
    def __init__(self, with_nodes_file=None, with_edges_file=None):
        """
        option 1:  init as an empty graph and add nodes
        option 2: init by specifying a path to nodes & edges files
        """
        self.nodes = []
        self.edges = []

        if with_nodes_file and with_edges_file:
            nodes_CSV = csv.reader(open(with_nodes_file))
            nodes_CSV = list(nodes_CSV)[1:]
            self.nodes = [(n[0], n[1]) for n in nodes_CSV]

            edges_CSV = csv.reader(open(with_edges_file))
            edges_CSV = list(edges_CSV)[1:]
            self.edges = [(e[0], e[1]) for e in edges_CSV]

    def add_node(self, id: str, name: str) -> None:
        """
        add a tuple (id, name) representing a node to self.nodes if it does not already exist
        The graph should not contain any duplicate nodes
        """
        self.nodes.append((id, name))

        return None

    def add_edge(self, source: str, target: str) -> None:
        """
        Add an edge between two nodes if it does not already exist.
        An edge is represented by a tuple containing two strings: e.g.: ('source', 'target').
        Where 'source' is the id of the source node and 'target' is the id of the target node
        e.g., for two nodes with ids 'a' and 'b' respectively, add the tuple ('a', 'b') to self.edges
        """
        if (target, source) in self.edges:
            return
        else:
            self.edges.append((source, target))

        return None

    def total_nodes(self) -> int:
        """
        Returns an integer value for the total number of nodes in the graph
        """
        return len(self.nodes)

    def total_edges(self) -> int:
        """
        Returns an integer value for the total number of edges in the graph
        """
        return len(self.edges)


    def get_edges_dict(self): 
        actor_ids = []
        edge_count = []
        degree_dict= {}

        for n in self.nodes:
            node_id = n[0]
            actor_ids.append(node_id)
            count = 0
            for edge in self.edges:
                if node_id in edge:
                    count += 1

            edge_count.append(count)

        for i in range(len(edge_count)):
            degree_dict[actor_ids[i]] = edge_count[i]

        return degree_dict



    def max_degree_nodes(self) -> dict:
        """
        Return the node(s) with the highest degree
        Return multiple nodes in the event of a tie
        Format is a dict where the key is the node_id and the value is an integer for the node degree
        e.g. {'a': 8}
        or {'a': 22, 'b': 22}
        """

        degree_dict = {}

        actor_ids = []
        edge_count = []

        for n in self.nodes:
            node_id = n[0]
            actor_ids.append(node_id)
            count = 0
            for edge in self.edges:
                if node_id in edge:
                    count += 1

            edge_count.append(count)

        for i in range(len(edge_count)):
            if edge_count[i] == max(edge_count):
                degree_dict[actor_ids[i]] = edge_count[i]

        return degree_dict


    def print_nodes(self):
        """
        No further implementation required
        May be used for de-bugging if necessary
        """
        print(self.nodes)

    def print_edges(self):
        """
        No further implementation required
        May be used for de-bugging if necessary
        """
        print(self.edges)

    # Do not modify
    def write_edges_file(self, path="edges.csv") -> None:
        """
        write all edges out as .csv
        :param path: string
        :return: None
        """
        edges_path = path
        edges_file = open(edges_path, 'w', encoding='utf-8')

        edges_file.write("source" + "," + "target" + "\n")

        for e in self.edges:
            edges_file.write(e[0] + "," + e[1] + "\n")

        edges_file.close()
        print("finished writing edges to csv")

    # Do not modify
    def write_nodes_file(self, path="nodes.csv") -> None:
        """
        write all nodes out as .csv
        :param path: string
        :return: None
        """
        nodes_path = path
        nodes_file = open(nodes_path, 'w', encoding='utf-8')

        nodes_file.write("id,name" + "\n")
        for n in self.nodes:
            nodes_file.write(n[0] + "," + n[1] + "\n")
        nodes_file.close()
        print("finished writing nodes to csv")

    def check_nodes(self, id: str) -> bool:
        for node in self.nodes:
            if id in node:
                return True

        return False

    def get_k_nodes(self):
        edges_dict = get_edges_dict()

        more_than_one_count = 0

        for n in self.nodes: 
            if edges_dict[n] > 1:
                more_than_one_count += 1

        return more_than_one_count




class TMDBAPIUtils:

    # Do not modify
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_movie_cast(self, movie_id: str, limit: int = None, exclude_ids: list = None) -> list:
        """
        Get the movie cast for a given movie id, with optional parameters to exclude an cast member
        from being returned and/or to limit the number of returned cast members
        documentation url: https://developers.themoviedb.org/3/movies/get-movie-credits

        :param integer movie_id: a movie_id
        :param integer limit: maximum number of returned cast members by their 'order' attribute
            e.g., limit=5 will attempt to return the 5 cast members having 'order' attribute values between 0-4
            If after exluding, there are fewer cast members than the specified limit or the limit not specified, return all cast members.
            If cast members with 'order' attribute in the specified limit range have been excluded, do not include more cast members to reach the limit.
            e.g., if limit=5 and the actor whose id corresponds to cast member with order=1 is to be excluded,
            return cast members with order values [0, 2, 3, 4], not [0, 2, 3, 4, 5]
        :param list exclude_ids: a list of ints containing ids (not cast_ids) of cast members  that should be excluded from the returned result
            e.g., if exclude_ids are [353, 455] then exclude these from any result.
        :rtype: list
            return a list of dicts, one dict per cast member with the following structure:
                [{'id': '97909' # the id of the cast member
                'character': 'John Doe' # the name of the character played
                'credit_id': '52fe4249c3a36847f8012927' # id of the credit, ...}, ... ]
                Note that this is an example of the structure of the list and some of the fields returned by the API.
                The result of the API call will include many more fields for each cast member.
        """

        credits_request = self.get_request('movie', movie_id, 'credits')
        credits_data = self.get_data(credits_request)
        credits_data = credits_data['cast']

        limited_cast = []

        for i in range(len(credits_data)):
            cast_dict = {'id': '', 'character': '', 'credit_id': ''}
            if credits_data[i]['order'] < limit:
                cast_dict['id'] = credits_data[i]['id']
                cast_dict['character'] = credits_data[i]['character']
                cast_dict['credit_id'] = credits_data[i]['credit_id']

                limited_cast.append(cast_dict)
            else:
                continue

        return limited_cast

    def get_request(self, req_type: str, item_id: str, details='') -> str:
        """
        Function returns the request url

        example: https://api.themoviedb.org/3/movie/603?api_key=fa0b74631406cb7e556e50abc1edb711&language=en-US

        @param req_type: movie or person
        @item_id: ID number
        @returns: request URL
        """
        base_url = 'http://api.themoviedb.org/3/'

        if details != '':
            return base_url + req_type + '/' + item_id + '/' + details + '?api_key=' + self.api_key + '&language=en-US'
        else:
            return base_url + req_type + '/' + item_id + '?api_key=' + self.api_key + '&language=en-US'

    def get_data(self, url_string: str) -> list:

        http_obj = urllib.request.urlopen(url_string)
        http_data = http_obj.read()

        http_encode = http_obj.info().get_content_charset('utf8')
        decoded_data = json.loads(http_data.decode(http_encode))

        return decoded_data

    def get_movie_credits_for_person(self, person_id: str, vote_avg_threshold: float = None) -> list:
        """
        Using the TMDb API, get the movie credits for a person serving in a cast role
        documentation url: https://developers.themoviedb.org/3/people/get-person-movie-credits

        :param string person_id: the id of a person
        :param vote_avg_threshold: optional parameter to return the movie credit if it is >=
            the specified threshold.
            e.g., if the vote_avg_threshold is 5.0, then only return credits with a vote_avg >= 5.0
        :rtype: list
            return a list of dicts, one dict per movie credit with the following structure:
                [{'id': '97909' # the id of the movie credit
                'title': 'Long, Stock and Two Smoking Barrels' # the title (not original title) of the credit
                'vote_avg': 5.0 # the float value of the vote average value for the credit}, ... ]
        """

        best_credits_list = []

        lf_request = self.get_request('person', person_id, 'movie_credits')
        lf_credits = self.get_data(lf_request)
        lf_credits = lf_credits['cast']  # List containing dictionaries of film credits

        for i in range(len(lf_credits)):
            movie_dict = {'id': '', 'title': '', 'vote_avg': 0}
            if lf_credits[i]['vote_average'] >= vote_avg_threshold:
                movie_dict['id'] = lf_credits[i]['id']
                movie_dict['title'] = lf_credits[i]['original_title']
                movie_dict['vote_avg'] = lf_credits[i]['vote_average']

                best_credits_list.append(movie_dict)

        return best_credits_list

    def trial_method(self):
        print('Hello world')

    def get_person_name(self, id: str) -> str:
        name_request = self.get_request('person', id)
        name_data = self.get_data(name_request)
        name = name_data['name']

        if ',' in name:
            name = name.replace(',', '')

        return name


#############################################################################################################################
#
# BUILDING YOUR GRAPH
#
# Working with the API:  See use of http.request: https://docs.python.org/3/library/http.client.html#examples
#
# Using TMDb's API, build a co-actor network for the actor's/actress' highest rated movies
# In this graph, each node represents an actor
# An edge between any two nodes indicates that the two actors/actresses acted in a movie together
# i.e., they share a movie credit.
# e.g., An edge between Samuel L. Jackson and Robert Downey Jr. indicates that they have acted in one
# or more movies together.
#
# For this assignment, we are interested in a co-actor network of highly rated movies; specifically,
# we only want the top 3 co-actors in each movie credit of an actor having a vote average >= 8.0.
# Build your co-actor graph on the actor 'Laurence Fishburne' w/ person_id 2975.
#
# You will need to add extra functions or code to accomplish this.  We will not directly call or explicitly grade your
# algorithm. We will instead measure the correctness of your output by evaluating the data in your argo-lite graph
# snapshot.
#
# GRAPH SIZE
# With each iteration of your graph build, the number of nodes and edges grows approximately at an exponential rate.
# Our testing indicates growth approximately equal to e^2x.
# Since the TMDB API is a live database, the number of nodes / edges in the final graph will vary slightly depending on when
# you execute your graph building code. We take this into account by rebuilding the solution graph every few days and
# updating the auto-grader.  We establish a bound for lowest & highest encountered numbers of nodes and edges with a
# margin of +/- 100 for nodes and +/- 150 for edges.  e.g., The allowable range of nodes is set to:
#
# Min allowable nodes = min encountered nodes - 100
# Max allowable nodes = max allowable nodes + 100
#
# e.g., if the minimum encountered nodes = 507 and the max encountered nodes = 526, then the min/max range is 407-626
# The same method is used to calculate the edges with the exception of using the aforementioned edge margin.
# ----------------------------------------------------------------------------------------------------------------------
# BEGIN BUILD CO-ACTOR NETWORK
#
# INITIALIZE GRAPH
#   Initialize a Graph object with a single node representing Laurence Fishburne
#
# BEGIN BUILD BASE GRAPH:
#   Find all of Laurence Fishburne's movie credits that have a vote average >= 8.0
#   FOR each movie credit:
#   |   get the movie cast members having an 'order' value between 0-2 (these are the co-actors)
#   |
#   |   FOR each movie cast member:
#   |   |   using graph.add_node(), add the movie cast member as a node (keep track of all new nodes added to the graph)
#   |   |   using graph.add_edge(), add an edge between the Laurence Fishburne (actress) node
#   |   |   and each new node (co-actor/co-actress)
#   |   END FOR
#   END FOR
# END BUILD BASE GRAPH
#
#
# BEGIN LOOP - DO 2 TIMES:
#   IF first iteration of loop:
#   |   nodes = The nodes added in the BUILD BASE GRAPH (this excludes the original node of Laurence Fishburne!)
#   ELSE
#   |    nodes = The nodes added in the previous iteration:
#   ENDIF
#
#   FOR each node in nodes:
#   |  get the movie credits for the actor that have a vote average >= 8.0
#   |
#   |   FOR each movie credit:
#   |   |   try to get the 3 movie cast members having an 'order' value between 0-2
#   |   |
#   |   |   FOR each movie cast member:
#   |   |   |   IF the node doesn't already exist:
#   |   |   |   |    add the node to the graph (track all new nodes added to the graph)
#   |   |   |   ENDIF
#   |   |   |
#   |   |   |   IF the edge does not exist:
#   |   |   |   |   add an edge between the node (actor) and the new node (co-actor/co-actress)
#   |   |   |   ENDIF
#   |   |   END FOR
#   |   END FOR
#   END FOR
# END LOOP
#
# Your graph should not have any duplicate edges or nodes
# Write out your finished graph as a nodes file and an edges file using:
#   graph.write_edges_file()
#   graph.write_nodes_file()
#
# END BUILD CO-ACTOR NETWORK
# ----------------------------------------------------------------------------------------------------------------------

# Exception handling and best practices
# - You should use the param 'language=en-US' in all API calls to avoid encoding issues when writing data to file.
# - If the actor name has a comma char ',' it should be removed to prevent extra columns from being inserted into the .csv file
# - Some movie_credits may actually be collections and do not return cast data. Handle this situation by skipping these instances.
# - While The TMDb API does not have a rate-limiting scheme in place, consider that making hundreds / thousands of calls
#   can occasionally result in timeout errors. If you continue to experience 'ConnectionRefusedError : [Errno 61] Connection refused',
#   - wait a while and then try again.  It may be necessary to insert periodic sleeps when you are building your graph.


def return_name() -> str:
    """
    Return a string containing your GT Username
    e.g., gburdell3
    Do not return your 9 digit GTId
    """
    return 'eperalta6'


def return_argo_lite_snapshot() -> str:
    """
    Return the shared URL of your published graph in Argo-Lite
    """
    return NotImplemented


# You should modify __main__ as you see fit to build/test your graph using  the TMDBAPIUtils & Graph classes.
# Some boilerplate/sample code is provided for demonstration. We will not call __main__ during grading.

# My TMDB key: fa0b74631406cb7e556e50abc1edb711
if __name__ == "__main__":

    # BUILD BASE GRAPH
    graph = Graph()
    graph.add_node(id='2975', name='Laurence Fishburne')
    tmdb_api_utils = TMDBAPIUtils(api_key=my_api_key)

    lf_best_movies = tmdb_api_utils.get_movie_credits_for_person('2975', 8.0)

    # call functions or place code here to build graph (graph building code not graded)
    # Suggestion: code should contain steps outlined above in BUILD CO-ACTOR NETWORK

    # For each movie credit
    for i in range(len(lf_best_movies)):
        movie_id = str(lf_best_movies[i]['id'])
        limited_cast = tmdb_api_utils.get_movie_cast(movie_id, 3)  # List of dictionaires containing cast for each movie

        base_nodes = []
        # For each cast member
        for j in range(len(limited_cast)):
            person_id = str(limited_cast[j]['id'])

            if graph.check_nodes(person_id):  # Don't add same node twice
                continue
            else:
                graph.add_node(person_id, tmdb_api_utils.get_person_name(person_id))
                base_nodes.append((person_id, tmdb_api_utils.get_person_name(person_id)))

            graph.add_edge('2975', person_id)

        passes = 2
        nodes2 = []
        for i in range(passes):
            nodes = []
            if i == 0:
                nodes = base_nodes
            else:
                nodes = nodes2

            # for each node in nodes
            for n in nodes:
                actor_id = n[0]
                best_movie_credits = tmdb_api_utils.get_movie_credits_for_person(actor_id, 8.0)  # get best movie credit

                # for each movie credit
                for j in range(len(best_movie_credits)):
                    new_movie_id = str(best_movie_credits[j]['id'])
                    new_limited_cast = tmdb_api_utils.get_movie_cast(new_movie_id, 3)  # Get casts from movie credit

                    # for each movie cast member
                    for k in range(len(new_limited_cast)):
                        new_person_id = str(new_limited_cast[k]['id'])

                        if graph.check_nodes(new_person_id):
                            continue
                        else:
                            graph.add_node(new_person_id, tmdb_api_utils.get_person_name(new_person_id))
                            if i == 0:
                                nodes2.append((new_person_id, tmdb_api_utils.get_person_name(new_person_id)))

                        graph.add_edge(actor_id, new_person_id)

    graph.write_edges_file()
    graph.write_nodes_file()

    # If you have already built & written out your graph, you could read in your nodes & edges files
    # to perform testing on your graph.
    # graph = Graph(with_edges_file="edges.csv", with_nodes_file="nodes.csv")
