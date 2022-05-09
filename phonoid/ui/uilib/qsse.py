"""
**Qt Style Sheet Extender**

This module will allow you to declare and use variable in qss.
"""
import re
import warnings


def extend(qss):
    var = re.compile(r"\$\w+ = .+")  # used to look for variable declaration
    undeclared = re.compile(r"\$\w+")  # used to look for undeclared variable

    with open(qss) as ss:
        variables = {}
        style = ss.read()

        for line in style.split("\n"):
            if var.match(line):
                var_decl = line.split("=")  # split variable into two part: variable name and variable value
                var_decl = [obj.strip() for obj in var_decl]  # clean the whitespace and newlines from split
                variables[var_decl[0]] = var_decl[1]

        style = style.split("#endvar\n")[1]

        for varname in variables.keys():
            style = style.replace(varname, variables[varname])

        try:
            undeclared_var = undeclared.search(style).group()
            warnings.warn(f"Undeclared stylesheet variable {undeclared_var}", SyntaxWarning)
        except AttributeError:
            pass

        return style
