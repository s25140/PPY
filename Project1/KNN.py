from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pickle


class KNNClassifier:
    def __init__(self, n_neighbors=5, model=None):
        if model:
            self.model = model
        else:
            self.model = KNeighborsClassifier(n_neighbors=n_neighbors)

    def train(self, train_set):
        train_data, train_labels = train_set
        self.model.fit(train_data, train_labels)

    def test(self, test_set):
        test_data, test_labels = test_set
        predicted_labels = self.model.predict(test_data)

        accuracy = accuracy_score(test_labels, predicted_labels)
        precision = precision_score(test_labels, predicted_labels, average='weighted', zero_division=0)
        recall = recall_score(test_labels, predicted_labels, average='weighted', zero_division=0)
        f1 = f1_score(test_labels, predicted_labels, average='weighted', zero_division=0)
        return round(accuracy,2), round(precision,2), round(recall,2), round(f1,2)

    def classify(self, input_data):
        return self.model.predict([input_data])[0]

    def save_model(self, filename="KNNmodel.pkl"):
        with open(filename, 'wb') as file:
            pickle.dump(self.model, file)

def load_data(filename):
    data = []
    labels = []
    with open(filename, 'r') as file:
        for line in file:
            row = [float(n) for n in line.strip().split(',')]
            data.append(row[:-1])
            labels.append(row[-1])
    return data, labels

def load_model(file_name):
    with open(file_name, 'rb') as file:
        model = pickle.load(file)
        return KNNClassifier(model.n_neighbors, model)