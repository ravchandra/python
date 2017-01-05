with open('salaries1.csv') as f:
	data = f.read()
	data = data.split("\n")[1:-1]
	d = [s.split(",") for s in data]
	d.sort(key=lambda x:x[2])
	print d

