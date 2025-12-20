from graphviz import Digraph

def generate_architecture_diagram():
    dot = Digraph(comment='System Architecture', format='png')
    dot.attr(rankdir='TB')  # Top to Bottom direction

    # The World (Data) Subgraph
    with dot.subgraph(name='cluster_world') as c:
        c.attr(label='The World (Data)')
        c.attr(style='filled')
        c.attr(color='lightgrey')
        c.node('D1', 'Inventory DB', shape='cylinder')
        c.node('D2', 'Finance DB', shape='cylinder')
        c.node('D3', 'Competitor DB', shape='cylinder')

    # Support Agents (Logic) Subgraph
    with dot.subgraph(name='cluster_agents') as c:
        c.attr(label='Support Agents (Logic)')
        c.attr(style='filled')
        c.attr(color='lightblue')
        c.node('A1', 'Inv Agent', shape='rect')
        c.node('A2', 'Finance Agent', shape='rect')
        c.node('A3', 'Comp Agent', shape='rect')

    # The Brain (AI) Subgraph
    with dot.subgraph(name='cluster_brain') as c:
        c.attr(label='The Brain (AI)')
        c.attr(style='filled')
        c.attr(color='lightyellow')
        c.node('M', 'Marketing Agent', shape='rect')
        c.node('LLM', 'Gemini 2.5', shape='doublecircle')

    # User
    dot.node('User', 'User', shape='circle')

    # Edges - Data Links
    dot.edge('A1', 'D1', label='Reads')
    dot.edge('A2', 'D2', label='Reads')
    dot.edge('A3', 'D3', label='Reads')

    # Edges - Internal Communication
    dot.edge('M', 'A1', label='Queries')
    dot.edge('M', 'A2', label='Queries')
    dot.edge('M', 'A3', label='Queries')
    dot.edge('LLM', 'M', label='Reasoning', dir='both')

    # Edges - User Interaction
    dot.edge('User', 'M', label='Selects Product')
    dot.edge('M', 'User', label='Output: Strategy')

    # Save
    output_path = dot.render('architecture', view=False)
    print(f"Architecture diagram generated at: {output_path}")

if __name__ == "__main__":
    generate_architecture_diagram()
