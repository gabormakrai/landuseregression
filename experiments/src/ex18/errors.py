
def ae(target, prediction):
    ae = []
    for i in range(0, len(target)):
        ae.append(abs(target[i] - prediction[i]))
    return ae
