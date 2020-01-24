# importing a CSV as a Pandas dataframe
# import os
# os.environ["PATH"] += os.pathsep + r'D:\GrsphViz\release\bin'0
# from pm4py.objects.conversion.log import factory as log_conv_factory
# conv_log = log_conv_factory.apply(df)
# print(len(conv_log))
import pandas as pd


from pm4py.objects.log.adapters.pandas import csv_import_adapter as csv_importer
df = csv_importer.import_dataframe_from_path("moni.csv")
# df = pd.read_csv("not_so_good_data.csv")
print(df)
# df1 = df.groupby(['org:resource','concept:name','case:concept:name','Costs','time:timestamp'])
# print(df)
# df = df.reset_index()
# print(df)
# print(rr)
# print(df)
# print(type(df['org:resource'][5]))
# df = pd.read_csv("not_so_good_data.csv")
# df['org:resource'] = df['org:resource'].astype(str)


from pm4py.objects.conversion.log import factory as log_conv_factory
conv_log = log_conv_factory.apply(df)
print(len(conv_log))
print(conv_log)
from pm4py.objects.log.util import sorting
sorted_log = sorting.sort_lambda(conv_log,lambda x: x.attributes["concept:name"], reverse=False)
from pm4py.algo.filtering.log.start_activities import start_activities_filter
log_start = start_activities_filter.get_start_activities(sorted_log)
filtered_log = start_activities_filter.apply(sorted_log, ["A"])
# print(rrr)
# from pm4py.algo.discovery.simple.model.log import factory as simple_algorithm

# net, initial_marking, final_marking = simple_algorithm.apply(conv_log, classic_output=True, parameters={"max_no_variants": 20})
# gviz = pn_vis_factory.apply(net, im, fm)
# pn_vis_factory.view(gviz)

# print(ooo)
from pm4py.algo.discovery.alpha import factory as alpha_miner
# the same exact discovery technique can be applied directly to Pandas dataframes! :)
from pm4py.algo.discovery.inductive import factory as inductive_miner
# discovers an accepting Petri net
net, im, fm = inductive_miner.apply(filtered_log)
tree = inductive_miner.apply_tree(filtered_log)
# print(tree)
from pm4py.visualization.process_tree import factory as pt_vis_factory

##########################################################
# gviz = pt_vis_factory.apply(tree)
# pt_vis_factory.view(gviz)
# print(net,im,fm)

# perform a visualization of the Petri net that is discovered
from pm4py.visualization.petrinet import factory as pn_vis_factory
# gviz = pn_vis_factory.apply(net, im, fm)
# pn_vis_factory.view(gviz)

# ############################################

gviz1 = pn_vis_factory.apply(net, im, fm, variant="frequency",log=filtered_log)
# pn_vis_factory.view(gviz1)

# print(ooo)




#################################
# from pm4py.algo.discovery.heuristics import factory as heuristics_miner
# heu_net = heuristics_miner.apply_heu(log, parameters={"dependency_thresh": 0.99})

########################################


#### mean of number of days between each process #######

from pm4py.algo.discovery.dfg import factory as dfg_factory

dfg = dfg_factory.apply(conv_log, variant="performance")
parameters = {"format":"png"}

from pm4py.visualization.dfg import factory as dfg_vis_factory

gviz = dfg_vis_factory.apply(dfg, log=conv_log, variant="performance",parameters = parameters)
dfg_vis_factory.save(gviz, "performance_invoice.png")
dfg_vis_factory.view(gviz)


##################################

#### mean of frequency between each process #######
from pm4py.algo.discovery.dfg import factory as dfg_factory

from pm4py.visualization.dfg import factory as dfg_vis_factory

dfg = dfg_factory.apply(conv_log)
parameters = {"format":"png"}

gviz1 = dfg_vis_factory.apply(dfg, variant="frequency",log=conv_log,parameters = parameters)
dfg_vis_factory.save(gviz1, "frequency_invoice.png")

dfg_vis_factory.view(gviz1)


########################################

##### alpha miner ##########

from pm4py.algo.discovery.alpha import factory as alpha_miner


########### inductive mining #######
from pm4py.visualization.petrinet import factory as pn_vis_factory
parameters = {"format":"png"}
net, initial_marking, final_marking = alpha_miner.apply(conv_log)
parameters = {"format":"png"}
gviz = pn_vis_factory.apply(net, initial_marking, final_marking, parameters=parameters, variant="frequency", log=conv_log)
pn_vis_factory.save(gviz, "inductive_frequency_invoice.png")
gviz = pn_vis_factory.apply(net, initial_marking, final_marking, parameters=parameters, variant="performance", log=conv_log)
pn_vis_factory.save(gviz, "inductive_performance_invoice.png")

#########################################

##### inducive miner ###################

from pm4py.algo.discovery.inductive import factory as inductive_miner
# discovers an accepting Petri net
net, im, fm = inductive_miner.apply(df)
tree = inductive_miner.apply_tree(conv_log) 
# gviz = pt_vis_factory.apply(tree)
# pt_vis_factory.view(gviz)


##########################################

##### classifiers #########
import os
from pm4py.objects.log.importer.xes import factory as xes_importer
from pm4py.algo.discovery.alpha import factory as alpha_miner
from pm4py.util import constants
# log = xes_importer.import_log(os.path.join("tests","input_data","running-example.xes"))
parameters = {constants.PARAMETER_CONSTANT_ACTIVITY_KEY: "concept:name"}
net, im, fm = alpha_miner.apply(conv_log, parameters=parameters)
gviz = pn_vis_factory.apply(net, im, fm)
# pn_vis_factory.view(gviz)

# from pm4py.objects.log.util import insert_classifier
# log, activity_key = insert_classifier.insert_activity_classifier_attribute(conv_log, "Activity classifier")

# from pm4py.algo.discovery.alpha import factory as alpha_miner
# from pm4py.util import constants
# parameters = {constants.PARAMETER_CONSTANT_ACTIVITY_KEY: activity_key}
# net, im, fm = alpha_miner.apply(conv_log, parameters=parameters)
# gviz = pn_vis_factory.apply(net, im, fm)
# pn_vis_factory.view(gviz)



###########################################################################


from pm4py.objects.petri import semantics
transitions = semantics.enabled_transitions(net, im)
places = net.places
transitions = net.transitions
arcs = net.arcs
for place in places:
	print("\nPLACE: "+place.name)
	for arc in place.in_arcs:
		print(arc.source.name, arc.source.label)


########################################################################

# creating an empty Petri net
from pm4py.objects.petri.petrinet import PetriNet, Marking
net = PetriNet("new_petri_net")
# creating source, p_1 and sink place
source = PetriNet.Place("source")
sink = PetriNet.Place("sink")
p_1 = PetriNet.Place("p_1")
# add the places to the Petri Net
net.places.add(source)
net.places.add(sink)
net.places.add(p_1)
# Create transitions
t_1 = PetriNet.Transition("name_1", "label_1")
t_2 = PetriNet.Transition("name_2", "label_2")
# Add the transitions to the Petri Net
net.transitions.add(t_1)
net.transitions.add(t_2)
# Add arcs
from pm4py.objects.petri import utils
utils.add_arc_from_to(source, t_1, net)
utils.add_arc_from_to(t_1, p_1, net)
utils.add_arc_from_to(p_1, t_2, net)
utils.add_arc_from_to(t_2, sink, net)
# Adding tokens
initial_marking = Marking()
initial_marking[source] = 1
final_marking = Marking()
final_marking[sink] = 1
from pm4py.objects.petri.exporter import pnml as pnml_exporter
pnml_exporter.export_net(net, initial_marking, "createdPetriNet1.pnml", final_marking=final_marking)

from pm4py.visualization.petrinet import factory as pn_vis_factory
parameters = {"format":"png"}
gviz = pn_vis_factory.apply(net, initial_marking, final_marking, parameters=parameters)
pn_vis_factory.save(gviz, "alpha_invoice.png")

# from pm4py.visualization.petrinet import factory as pn_vis_factory
# parameters = {"format":"svg"}
# gviz = pn_vis_factory.apply(net, initial_marking, final_marking, parameters=parameters)
# pn_vis_factory.save(gviz, "alpha.svg")

# pn_vis_factory.view(gviz)



######################################################################################################



