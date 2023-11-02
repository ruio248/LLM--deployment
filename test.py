import ast
s = "[(1,2)]"
lst = ast.literal_eval(s)
print(type(lst))  # 输出：[()]
