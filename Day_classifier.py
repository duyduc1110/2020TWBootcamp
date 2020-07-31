from simpletransformers.classification import ClassificationModel
import pandas as pd
import logging


# Train and Evaluation data needs to be in a Pandas Dataframe of two columns. The first column is the text with type str, and the second column is the label with type int.
train_df = pd.read_csv('data/Day_classifier_train.csv')
eval_df = pd.read_csv('data/Day_classifier_test.csv')

print(train_df.head())

# train_config
train_config = {'reprocess_input_data': True, 
                'overwrite_output_dir': True, 
                'num_train_epochs': 1, 
                "output_dir": "Day_classifier_outputs/", 
                'learning_rate': 1e-5
                }

# Create a ClassificationModel
model = ClassificationModel(
    "bert", "bert-base-cased", num_labels=3, args = train_config
)

# Train the model
model.train_model(train_df)

# Evaluate the model
result, model_outputs, wrong_predictions = model.eval_model(eval_df)

# 0 -> delay, 1 -> early, 2 -> change
predictions, raw_outputs = model.predict(["Buy food 5 days in advace"])
print(predictions)
print(raw_outputs)