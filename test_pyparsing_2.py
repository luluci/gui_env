import pyparsing as pp

def pa_keyword(match):
	print("Keyword: " + str(match))

def pa_identifier(match):
	print("identifier: " + str(match))


pp_rule1 = pp.Keyword("int").setParseAction(pa_keyword)
pp_identifier = pp.Word(pp.alphas+"_", pp.alphanums+"_").setParseAction(pa_identifier)
pp_type_decl = (
	pp.Optional(pp_rule1)
	& pp_identifier
)

input = [
	"int",
	"init",
]
for i, inp in enumerate(input):
	ret = pp_type_decl.parseString(inp)
	print("[" + str(i) + "]")
	print(ret)

"""
$ result
identifier: ['int']
[0]
['int']
identifier: ['init']
[1]
['init']
"""
