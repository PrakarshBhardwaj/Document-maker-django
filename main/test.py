def delete_from_sequence(seq, pos, char):
	cnt = 0
	assert pos > 0 and pos < len(seq), "Position provided is not valid"
	for i,v in enumerate(seq[:-1]):
		if v == char:
			cnt += 1
		if cnt == pos:
			return seq[:i] + seq[i+1:]
	return seq[:-1]

def add_to_sequence(seq, pos, char):
	cnt = 0
	assert pos > 0 and pos <= len(seq), "Position provided is not valid"
	for i,v in enumerate(seq):
		if v == char:
			cnt += 1
		if cnt == pos:
			return seq[:i] + char + seq[i:]
	return seq + char

seq = "PPIIPP"

print(delete_from_sequence(seq, 2, "I"))
print(add_to_sequence(seq, 1, "P"))