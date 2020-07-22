sys_args = {
    
    }


train_args = {
    'learning_rate': 3e-5,
    'num_train_epochs': 1,
    'max_seq_length': 384,
    'doc_stride': 128,
    'overwrite_output_dir': True,
    'reprocess_input_data': True,
    'train_batch_size': 2,
    'gradient_accumulation_steps': 8,
    "attention_probs_dropout_prob": 0.1,
    "finetuning_task": "squad2",
    "hidden_act": "gelu",
    "hidden_dropout_prob": 0.1,
    "hidden_size": 1024,
    "initializer_range": 0.02,
    "intermediate_size": 4096,
    "language": "english",
    "layer_norm_eps": 1e-12,
    "max_position_embeddings": 512,
    "model_type": "bert",
    "name": "Bert",
    "num_attention_heads": 16,
    "num_hidden_layers": 24,
    "output_past": True,
    "pad_token_id": 0,
    "type_vocab_size": 2,
    "vocab_size": 30522
}

question_list = [
                'what are we going to do?', 
                'what day?', 
                'what time?', 
                'where are we going?' 
                ]




