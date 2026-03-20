import streamlit as st
import networkx as nx
import random
import matplotlib.pyplot as plt

# Independent Cascade Function
def independent_cascade(G, seeds, p):
    active = set(seeds)
    new_active = set(seeds)

    while new_active:
        temp = set()
        for node in new_active:
            for neighbor in G.neighbors(node):
                if neighbor not in active:
                    if random.random() < p:
                        temp.add(neighbor)
        new_active = temp
        active.update(new_active)

    return len(active), active

# Select top-k high degree nodes
def select_seeds(G, k):
    nodes_sorted = sorted(G.degree, key=lambda x: x[1], reverse=True)
    seeds = [node for node, degree in nodes_sorted[:k]]
    return seeds

# Streamlit UI
st.title("Independent Cascade Model Simulation")

# Sidebar controls
st.sidebar.header("Parameters")
num_nodes = st.sidebar.slider("Number of Nodes", 10, 100, 20)
edge_prob = st.sidebar.slider("Edge Probability", 0.0, 1.0, 0.2)
p = st.sidebar.slider("Activation Probability (p)", 0.0, 1.0, 0.3)
k = st.sidebar.slider("Number of Seed Nodes (k)", 1, 10, 2)

# Generate graph
G = nx.erdos_renyi_graph(num_nodes, edge_prob)

# Select seeds
seeds = select_seeds(G, k)

# Run simulation
spread, active_nodes = independent_cascade(G, seeds, p)

# Display results
st.subheader("Results")
st.write(f"Selected Seed Nodes: {seeds}")
st.write(f"Total Activated Nodes (Spread): {spread}")

# Visualization
st.subheader("Graph Visualization")

pos = nx.spring_layout(G)
plt.figure(figsize=(6, 6))

# Draw nodes
nx.draw_networkx_nodes(G, pos, node_color="lightgray")
nx.draw_networkx_nodes(G, pos, nodelist=active_nodes, node_color="green")
nx.draw_networkx_nodes(G, pos, nodelist=seeds, node_color="red")

# Draw edges & labels
nx.draw_networkx_edges(G, pos)
nx.draw_networkx_labels(G, pos)

plt.title("Green = Active, Red = Seeds")
st.pyplot(plt)