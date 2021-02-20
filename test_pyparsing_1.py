import pyparsing as pp

pp_identifier = (
	# keywords is not identifier, 
	pp.NotAny(
		pp.Keyword("void")
		| pp.Keyword("unsigned")
		| pp.Keyword("signed")
		| pp.Keyword("int")
		| pp.Keyword("float")
		| pp.Keyword("const")
		| pp.Keyword("volatile")
		| pp.Keyword("extern")
		| pp.Keyword("static")
	)
	+ pp.Word(pp.alphas+"_", pp.alphanums+"_", asKeyword=True)
)
#pp_identifier = pp.Word(pp.alphas+"_", pp.alphanums+"_")
pp_semicolon = pp.Literal(";")

def get_type_spec(p):
	print("get_type_spec: " + str(p))

pp_type_spec = (
	pp.Keyword("void")
	| (pp.Optional(pp.Keyword("unsigned") | pp.Keyword("signed")) + pp.Keyword("int"))
	| pp.Keyword("float")
	| pp_identifier
).setParseAction(get_type_spec)
pp_type_qual = (
	pp.Keyword("const")
	| pp.Keyword("volatile")
)
pp_strage_spec = (
	pp.Keyword("extern")
	| pp.Keyword("static")
)
decl_spec = (
	pp.Optional(pp_type_qual)
	& pp.Optional(pp_strage_spec)
	& pp.Optional(pp_type_spec)
)
"""
# exception???
decl_spec = pp.Each(
	pp.Optional(pp_type_qual)
	& pp.Optional(pp_strage_spec)
	& pp.Optional(pp_type_spec)
)
"""
decl = decl_spec + pp_identifier + pp_semicolon

input = [
	"int var1;",
	"static int var2;",
	"static const int var3;"
]
for i, inp in enumerate(input):
	ret = decl.parseString(inp)
	print("[" + str(i) + "]")
	print(ret)
