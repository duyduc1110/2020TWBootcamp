from simpletransformers.classification import MultiLabelClassificationModel
import pandas as pd
import logging
from sklearn.utils import shuffle

print('Go')
logging.basicConfig(level=logging.INFO)
transformers_logger = logging.getLogger("transformers")
transformers_logger.setLevel(logging.WARNING)

# Train and Evaluation data needs to be in a Pandas Dataframe containing at least two columns, a 'text' and a 'labels' column. The `labels` column should contain multi-hot encoded lists.
general_df = pd.read_csv("data/Domain_classifier_train.csv")
structure_df = pd.read_csv("data/struture_Domain_classifier_train.csv")
train_df = shuffle(pd.concat([general_df, structure_df], sort=False))
train_df["labels"] = train_df["labels"].apply(lambda x: [int(i) for i in x[1:-1].split(',')])

eval_df = pd.read_csv("data/Domain_classifier_test.csv")
eval_df["labels"] = eval_df["labels"].apply(lambda x: [int(i) for i in x[1:-1].split(',')])

train_config = {'reprocess_input_data': True, 
                'overwrite_output_dir': True, 
                'num_train_epochs': 1, 
                "output_dir": "Domain_classifier_outputs/", 
                'learning_rate': 1e-5
                }

# Create a MultiLabelClassificationModel
model = MultiLabelClassificationModel('roberta', 'roberta-base', num_labels=5, args=train_config)
# You can set class weights by using the optional weight argument
print(train_df.head())

# Train the model
model.train_model(train_df)

# Evaluate the model
print(eval_df.head())
result, model_outputs, wrong_predictions = model.eval_model(eval_df)
print(result)
print(model_outputs)

predictions, raw_outputs = model.predict(["Let's grab lunch your place on Sunday?"])
print(predictions)
print(raw_outputs)