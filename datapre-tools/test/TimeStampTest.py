from Timestamp import Timestamp

t1 = Timestamp().createBasedOnKey("2015101523")
print("t1: " + str(t1))

t2 = Timestamp().createBasedOnKey("2013010101")
print("t2: " + str(t2))

t3 = Timestamp().createBasedOnKey("2013010101")
print("t3: " + str(t3))

print("t2 == t3: " + str(t2 == t3))

print("t1 == t3: " + str(t1 == t3))
