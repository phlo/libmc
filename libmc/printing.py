def formatState (s):
    """Prettify a state's string representation for printing."""
    return str(s) \
        .replace("'", "") \
        .replace("[", "\{") \
        .replace("]", "\}") \
        .replace(",)", ")")

def printRelation (relation, A, B):
    """Pretty print relation table in markdown format."""
    def formatPair (s, t):
        return "(" + \
            formatState(s) + \
            ", " + \
            formatState(t) + \
        ")"

    # determine header column width (bold)
    headerWidth = max(
        max(len(str(s)) + 4 for s in A), max(len(str(t)) + 4 for t in B)
    )

    # determine content column width
    colWidth = max(len(formatPair(s, t)) for s in A for t in B)

    # set column width to the maximum
    if headerWidth > colWidth:
        colWidth = headerWidth

    # print header
    print("| " + "".ljust(colWidth) + " | " + " | ".join(
            ("**" + formatState(s) + "**").ljust(colWidth)
            for s in B
        ) + " |"
    )

    # print separator
    print("| " + " | ".join(
            "-" * colWidth
            for i in range(len(B) + 1)
        ) + " |"
    )

    # print table
    for s in A:
        print(
            "| " + ("**" + formatState(s) + "**").ljust(colWidth) + " | " +
            " | ".join(
                formatPair(s, t).ljust(colWidth)
                if (s, t) in relation else "".ljust(colWidth)
                for t in B
            ) + " |"
        )

def fa2dot (S, I, Σ, T, F, highlight = []):
    """
    Returns graphical representation of given automaton (using `Graphviz
    <https://www.graphviz.org/>`_).

    Args:
        S: set of states
        I: set of initial states I ⊆ S
        Σ: input alphabet
        T: transition relation T ⊆ SxΣxS
        F: set of final states F ⊆ S
        highlight (list of transitions lists - optional): highlight the given
            paths

    Returns:
        string: .dot file tweaked for dot2tex
    """
    tex = """\
digraph FSM {
  d2toptions = "-f tikz -t math --tikzedgelabels --styleonly --usepdflatex";
  d2tdocpreamble = "\\usetikzlibrary{automata}";
  node [style="state"];
  edge [lblstyle="auto"];
"""
    # generate states
    for s in S:
        style = []
        if s in I: style.append("initial")
        if s in F: style.append("accepting")
        if any(s == t[0] or s == t[2] for trace in highlight for t in trace):
            style.append("draw=red")

        tex += "  \"state {}\"{};\n".format(
                formatState(s),
                " [label=\"{}\"{}]".format(
                    formatState(s),
                    ",style=\"state," + ','.join(style) + '\"' if style else ""
                    )
                )

    # generate transitions
    for t in T:
        tex += "  \"state {}\" -> \"state {}\" [label=\"{}\"{}];\n".format(
            formatState(t[0]),
            formatState(t[2]),
            t[1],
            ",style=\"draw=red\"" if any(t in trace for trace in highlight)
            else ""
        )

    tex += "}"
    return tex
