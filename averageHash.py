f = open("avgHash", "r")
lines = f.readlines()
total = 0
for line in lines:
	if "#" not in line:
		total += float(line)
average = total / len(lines)
print("\nRunning Average of Average: " + str(round(average, 3)) + "\n")
