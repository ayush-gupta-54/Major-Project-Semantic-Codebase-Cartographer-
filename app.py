import streamlit as st
import networkx as nx
import plotly.graph_objects as go
from parser import parse_file
from graph import build_graph

st.title("🌐 Semantic Codebase Cartographer")

uploaded_file = st.file_uploader("Upload a Python file", type=["py"])

def create_3d_graph(G):
    pos = nx.spring_layout(G, dim=3)

    x_nodes = [pos[node][0] for node in G.nodes()]
    y_nodes = [pos[node][1] for node in G.nodes()]
    z_nodes = [pos[node][2] for node in G.nodes()]

    edge_x = []
    edge_y = []
    edge_z = []

    for edge in G.edges():
        x0, y0, z0 = pos[edge[0]]
        x1, y1, z1 = pos[edge[1]]

        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]
        edge_z += [z0, z1, None]

    edge_trace = go.Scatter3d(
        x=edge_x,
        y=edge_y,
        z=edge_z,
        mode='lines'
    )

    node_trace = go.Scatter3d(
        x=x_nodes,
        y=y_nodes,
        z=z_nodes,
        mode='markers+text',
        text=list(G.nodes()),
        textposition="top center"
    )

    fig = go.Figure(data=[edge_trace, node_trace])
    return fig


if uploaded_file:
    with open("temp.py", "wb") as f:
        f.write(uploaded_file.getbuffer())

    parsed = parse_file("temp.py")
    G = build_graph(parsed)

    st.subheader("📍 3D Code Structure")

    fig = create_3d_graph(G)
    st.plotly_chart(fig)

    st.success("✅ Done! 3D Graph Generated")