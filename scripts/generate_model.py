from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
import pickle


X = ["i love this", "this is great", "i hate this", "very bad"]
y = [1,1,0,0]

model_path = "/Users/petros-pavlosypsilantis/Documents/Projects/MLOps/cicd_pipelines/ml-ops-pipelines/models/new_model/model.pkl"

pipe = make_pipeline(TfidfVectorizer(), LogisticRegression())
pipe.fit(X,y)
with open(model_path, 'wb') as f:
    pickle.dump(pipe, f)