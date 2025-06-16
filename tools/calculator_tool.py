import re
import ast
import operator as op
from langchain.tools import Tool

# Supported operators
operators = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
    ast.UAdd: op.pos,
    ast.Mod: op.mod
}

def safe_eval(expr: str):
    """
    Safely evaluate a mathematical expression using AST.
    """
    def eval_node(node):
        if isinstance(node, ast.Num):  # <number>
            return node.n
        elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
            return operators[type(node.op)](eval_node(node.left), eval_node(node.right))
        elif isinstance(node, ast.UnaryOp):  # <operator> <operand> e.g., -1
            return operators[type(node.op)](eval_node(node.operand))
        else:
            raise TypeError(f"Unsupported type: {type(node)}")

    try:
        parsed = ast.parse(expr, mode='eval')
        return eval_node(parsed.body)
    except Exception as e:
        raise ValueError("Invalid or unsupported expression")

def get_calculator_tool():
    def safe_calculate(expression: str) -> str:
      try:
        print(f"[DEBUG] Original expression: {expression}")

        # Convert "15%" to "0.15"
        expression = re.sub(r'(\d+(\.\d+)?)\s*%', lambda m: str(float(m.group(1)) / 100), expression)

        print(f"[DEBUG] Converted expression: {expression}")

        # Clean and evaluate
        expression = re.sub(r'[^\d\.\+\-\*\/\(\)\s]', '', expression)
        expression = re.sub(r'\s+', '', expression)

        if not expression:
            return "No valid mathematical expression found."

        result = safe_eval(expression)

        if isinstance(result, (int, float)) and abs(result) >= 1000:
            return f"{result:,.2f}"
        return str(result)

      except Exception as e:
        return f"Calculation error: {str(e)}"

    return Tool(
        name="Calculator",
        func=safe_calculate,
        description="Accurately evaluates mathematical expressions. Supports +, -, *, /, %, parentheses, and decimals."
    )
