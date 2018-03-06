import subprocess

from os import path

def run (cmd, **kwargs):
    """
    Run the given system command in a subshell.

    Args:
        cmd (string): shell command to be executed

    Keyword Args:
        toFile (string): write output to the given file name

    Returns:
        string: output (stdout)
    """
    stdin = kwargs["stdin"] if "stdin" in kwargs else None

    proc = subprocess.run(
        cmd,
        shell=True,
        input=stdin,
        stdout=subprocess.PIPE,
        universal_newlines=True
    )

    if "toFile" in kwargs:
        with open(kwargs["toFile"], 'w') as f:
            f.write(proc.stdout)

    if proc.stderr:
        print(proc.stderr)

    return proc.stdout

def dot2pdf (dot, pdfName, prog="dot", template=None):
    """Convert the given DOT string into a PDF."""
    dot2tex = [
        "dot2tex",
        "--prog " + prog,
    ]

    if template is not None:
        dot2tex.append("--template=" + template)

    texName = pdfName[:-3] + "tex"

    pdflatex = [
        "pdflatex",
        "-output-directory " + path.dirname(pdfName),
        texName
    ]

    run(" ".join(dot2tex), stdin=dot, toFile=texName)
    run(" ".join(pdflatex))

def pdf2png (pdfName):
    """Convert the given PDF to a PNG using imagemagick."""
    pngName = pdfName[:-3] + "png"

    convert = [
        "convert",
        "-density 150",
        "-quality 90",
        pdfName,
        pngName
    ]

    run(" ".join(convert))
