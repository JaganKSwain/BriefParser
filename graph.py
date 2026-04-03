from langgraph.graph import StateGraph, END
from schemas import AgentState
from nodes.parser import parse_brief
from nodes.brand_retriever import retrieve_brand_context
from nodes.interpreter import interpret_brief
from nodes.dispatcher import dispatch


def should_continue(state: AgentState) -> str:
    """
    Central routing function. Called after every node except dispatcher.
    If the state is flagged at any point, jump straight to dispatcher
    which handles flagged briefs differently from clean ones.
    """
    if state.flagged:
        return "dispatch"
    return "continue"


def build_graph() -> StateGraph:
    graph = StateGraph(AgentState)

    # Register all four nodes
    graph.add_node("parse",            parse_brief)
    graph.add_node("retrieve_context", retrieve_brand_context)
    graph.add_node("interpret",        interpret_brief)
    graph.add_node("dispatch",         dispatch)

    # Entry point
    graph.set_entry_point("parse")

    # After parse: if flagged go to dispatch, otherwise retrieve brand context
    graph.add_conditional_edges(
        "parse",
        should_continue,
        {
            "dispatch": "dispatch",
            "continue": "retrieve_context"
        }
    )

    # After retrieve_context: if flagged go to dispatch, otherwise interpret
    graph.add_conditional_edges(
        "retrieve_context",
        should_continue,
        {
            "dispatch": "dispatch",
            "continue": "interpret"
        }
    )

    # After interpret: if flagged go to dispatch, otherwise dispatch
    # (both paths lead to dispatch here — flagged dispatch vs clean dispatch)
    graph.add_conditional_edges(
        "interpret",
        should_continue,
        {
            "dispatch": "dispatch",
            "continue": "dispatch"
        }
    )

    # Dispatcher always ends the graph
    graph.add_edge("dispatch", END)

    return graph.compile()


# Compiled graph — import this in main.py
pipeline = build_graph()