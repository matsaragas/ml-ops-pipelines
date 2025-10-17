import pickle, json, sys
from sklearn.metrics import accuracy_score, precision_score, recall_score


VAL = ["i love it", "terrible product", "not good", "excellent!", "i like this"]
Y = [1,0,0,1,1]


model_path = sys.argv[1]
with open(model_path, 'rb') as f:
    model = pickle.load(f)


preds = model.predict(VAL)
metrics = {
    'accuracy': float(accuracy_score(Y, preds)),
    'precision': float(precision_score(Y, preds, zero_division=0)),
    'recall': float(recall_score(Y, preds, zero_division=0))
}
print('Evaluation metrics:', metrics)
with open('evaluation_results.json', 'w') as f:
    json.dump(metrics, f)