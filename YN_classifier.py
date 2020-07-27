from simpletransformers.classification import ClassificationModel
import pandas as pd
import logging


logging.basicConfig(level=logging.INFO)
transformers_logger = logging.getLogger("transformers")
transformers_logger.setLevel(logging.WARNING)

# Train and Evaluation data needs to be in a Pandas Dataframe of two columns. The first column is the text with type str, and the second column is the label with type int.
train_df = pd.read_csv('Data/YN_classifier_train.csv')
eval_df = pd.read_csv('Data/YN_classifier_test.csv')

# Create a ClassificationModel
model = ClassificationModel('roberta', 'roberta-base', args={'reprocess_input_data': True, 'overwrite_output_dir': True, 'num_train_epochs': 3, "output_dir": "YN_classifier_outputs/"}) # You can set class weights by using the optional weight argument

# Train the model
model.train_model(train_df)

# Evaluate the model
result, model_outputs, wrong_predictions = model.eval_model(eval_df)