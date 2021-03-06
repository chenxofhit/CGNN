import cgnn
import pandas as pd
from sklearn.preprocessing import scale

# Params
cgnn.SETTINGS.GPU = True
cgnn.SETTINGS.NB_GPU = 2
cgnn.SETTINGS.NB_JOBS = 8
cgnn.SETTINGS.NB_RUNS = 32

datafile = "Example_graph_confounders_numdata.csv"
skeletonfile = "Example_graph_confounders_skeleton.csv"


data = pd.read_csv(datafile)
skeleton_links = pd.read_csv(skeletonfile)

skeleton = cgnn.UndirectedGraph(skeleton_links)

data = pd.DataFrame(scale(data),columns=data.columns)

GNN = cgnn.GNN(backend="TensorFlow")
p_directed_graph = GNN.orient_graph_confounders(data, skeleton, printout= datafile +  '_printout.csv')

gnn_res = pd.DataFrame(p_directed_graph.get_list_edges(descending=True), columns=['Cause', 'Effect', 'Score'])
gnn_res.to_csv(datafile + "_pairwise_predictions.csv")
CGNN_confounders = cgnn.CGNN_confounders(backend="TensorFlow")
directed_graph = CGNN_confounders.orient_directed_graph(data, p_directed_graph)
cgnn_res = pd.DataFrame(directed_graph.get_list_edges(descending=True), columns=['Cause', 'Effect', 'Score'])

cgnn_res.to_csv(datafile + "_confounders_predictions.csv")


