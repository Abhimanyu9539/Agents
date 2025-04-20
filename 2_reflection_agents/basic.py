from typing import List, Sequence
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, MessageGraph
from chains import generation_chain, reflection_chain

load_dotenv()

graph = MessageGraph()
REFLECT = "reflect"
GENERATE = "generate"

def generate_node(state):
    return generation_chain.invoke({
        'messages': state
    })


def reflect_node(state):
    response =  reflection_chain.invoke({
        "messages":state
    })

    return [HumanMessage(content=response.content)]


def should_continue(state):
    if (len(state) > 4):
        return END
    return REFLECT


## Add the nodes to graph
graph.set_entry_point(GENERATE)
graph.add_node(GENERATE, generate_node)
graph.add_node(REFLECT, reflect_node)

# Add the edges
graph.add_conditional_edges(GENERATE, 
                            should_continue,
                            path_map={
                                REFLECT: REFLECT,
                                END: END
                            })
graph.add_edge(REFLECT, GENERATE)

workflow = graph.compile()

print(workflow.get_graph().draw_mermaid())
workflow.get_graph().print_ascii()

response = workflow.invoke(HumanMessage(content="AI Agents taking over content creation"))

print(response)