import json,sys
print(json.dumps({'argv':sys.argv,'repr':[repr(x) for x in sys.argv]},ensure_ascii=True))
