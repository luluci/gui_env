import pyparsing as pp


def act_comment(token):
	print("comment: " + str(token))


def act_keyword(token):
	print("keyword: " + str(token))


def act_sc(token):
	print("semicolon: " + str(token))


def act_parser_start(token):
	print("parser_start: " + str(token))


def act_parser_end(token):
	print("parser_end: " + str(token))


comment_parser = pp.Group(
	(pp.Literal("//") + pp.restOfLine)
	| pp.cStyleComment
).setParseAction(act_comment)

pp_key1 = pp.Keyword("hoge")
pp_key2 = pp.Keyword("fuga")
pp_sc = pp.Literal(";")

statement = pp.Group(
	pp.Empty().setParseAction(act_parser_start)
	+ pp_key1.setParseAction(act_keyword)
	+ pp_key2.setParseAction(act_keyword)
	+ pp_sc.setParseAction(act_sc)
	+ pp.Empty().setParseAction(act_parser_end)
)
parser = statement[1, ...].ignore(comment_parser)


test_text = """\
hoge fuga;	// comment1
hoge /* comment2-1 */ fuga;	/* comment2-2 */
// comment3
hoge fuga;	// comment4
"""

ret = parser.parseString(test_text)
print(ret)

"""
[result]
parser_start: []
keyword: ['hoge']
keyword: ['fuga']
semicolon: [';']
comment: [['//', ' comment1']]
parser_end: []
parser_start: []
keyword: ['hoge']
comment: [['/* comment2-1 */']]
keyword: ['fuga']
semicolon: [';']
comment: [['/* comment2-2 */']]
comment: [['//', ' comment3']]
parser_end: []
parser_start: []
keyword: ['hoge']
keyword: ['fuga']
semicolon: [';']
comment: [['//', ' comment4']]
parser_end: []
parser_start: []
[['hoge', 'fuga', ';'], ['hoge', 'fuga', ';'], ['hoge', 'fuga', ';']]
"""
