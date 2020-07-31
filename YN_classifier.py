from simpletransformers.classification import ClassificationModel
import pandas as pd
import logging
from sklearn.utils import shuffle

logging.basicConfig(level=logging.INFO)
transformers_logger = logging.getLogger("transformers")
transformers_logger.setLevel(logging.WARNING)

# Train and Evaluation data needs to be in a Pandas Dataframe of two columns. The first column is the text with type str, and the second column is the label with type int.
general_df = pd.read_csv("data/YN_classifier_train.csv")
structure_df = pd.read_csv("data/struture_YN_classifier_train.csv")
train_df = shuffle(pd.concat([general_df, structure_df], sort=False))

eval_df = pd.read_csv('data/YN_classifier_test.csv')

train_config = {'reprocess_input_data': True, 
                'overwrite_output_dir': True, 
                'num_train_epochs': 1, 
                "output_dir": "YN_classifier_outputs/", 
                }

# Create a ClassificationModel
model = ClassificationModel('roberta', 'roberta-base', args = train_config) # You can set class weights by using the optional weight argument

# Train the model
model.train_model(train_df)

# Evaluate the model
result, model_outputs, wrong_predictions = model.eval_model(eval_df)

# 1 -> yes, 0 -> no
predictions, raw_outputs = model.predict(["Don't do that"])
print(predictions)
print(raw_outputs)