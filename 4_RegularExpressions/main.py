from reg import Reg

# var 1
re = ['(a|b) (c|d) E+ G?', 'P (Q|R|S) T (UV|W|X)* Z+', '1 (0|1)* 2 (3|4)5 36']

reg1 = Reg(re)
reg1.scan_re()
reg1.generate_str(5)