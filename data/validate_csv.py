import csv

l = []
with open('data.csv', 'r') as f:
	t = csv.reader(f)
	for row in t:
		l.append(row)

for i in range(len(l)):
	if not l[i][0].isdigit():
		print(i, l[i][0])
	else:
		print(i)