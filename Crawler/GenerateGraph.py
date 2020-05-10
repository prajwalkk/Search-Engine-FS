import matplotlib.pyplot as plt
import networkx as nx


def is_node(webpage, graph):
    return graph.has_node(webpage.rstrip('/'))


def add_node(webpage, graph):
    graph.add_node(webpage.rstrip('/'))
    return


def remove_node(webpage, graph):
    graph.remove_node(webpage.rstrip('/'))
    return


def remove_nodes(valid_websites, graph):
    nodes = graph.nodes()
    removable_nodes = [item for item in nodes if item.rstrip(
        '/') not in valid_websites]
    graph.remove_nodes_from(removable_nodes)
    return


def add_edges(current_page, links, graph):
    for link in links:
        if graph.has_edge(current_page.rstrip('/'), link.rstrip('/')):
            graph[current_page.rstrip('/')][link.rstrip('/')]['weight'] += 1
        else:
            graph.add_edge(current_page.rstrip(
                '/'), link.rstrip('/'), weight=1)


def draw_graph(graph):
    nx.draw(graph, node_color="#0000AE",
            edge_cmap=plt.cm.Blues, with_labels=True)
    plt.show()


def save_graph(graph, path):
    nx.write_gpickle(graph, path)
