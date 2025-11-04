#!/usr/bin/env python3
"""
Configuración de SeqIO para fine-tuning GPT-OSS-20B
Define tasks y mixtures para el entrenamiento
"""

import seqio
import tensorflow as tf
from typing import Dict, Any

# Vocabulario (ajustar según tu modelo)
VOCAB_SIZE = 50257  # GPT-2 vocab size, ajustar si es diferente

def create_vocabulary():
    """Crear vocabulario para el modelo"""
    # En un setup real, cargarías el vocabulario desde el checkpoint del modelo
    # Por ahora, creamos un vocabulario básico
    vocab = seqio.SentencePieceVocabulary(
        sentencepiece_model_file="gs://datasets-training_9b/vocab/spiece.model",
        extra_ids=0
    )
    return vocab

# Vocabulario global
vocab = create_vocabulary()

def preprocess_text(example: Dict[str, Any]) -> Dict[str, Any]:
    """Preprocesar texto para entrenamiento de lenguaje"""
    text = example["text"]
    
    # Tokenizar el texto
    inputs = vocab.encode_tf(text)
    
    # Para autoregressive training, targets son inputs desplazados
    targets = tf.concat([inputs[1:], [vocab.eos_id]], axis=0)
    
    return {
        "inputs": inputs,
        "targets": targets
    }

def create_gpt_oss_task():
    """Crear task principal para GPT-OSS-20B"""
    
    # Task para el dataset original
    seqio.TaskRegistry.add(
        "gpt_oss_20b_original",
        source=seqio.TextLineDataSource(
            split_to_filepattern={
                "train": "gs://datasets-training_9b/datasets/original/*.txt",
                "validation": "gs://datasets-training_9b/datasets/original/validation/*.txt"
            },
            num_input_examples={
                "train": 1000000,  # Ajustar según tu dataset
                "validation": 10000
            }
        ),
        preprocessors=[
            preprocess_text,
            seqio.preprocessors.tokenize,
            seqio.preprocessors.append_eos_after_trim,
        ],
        output_features={
            "inputs": seqio.Feature(vocabulary=vocab, add_eos=True),
            "targets": seqio.Feature(vocabulary=vocab, add_eos=True)
        },
        metric_fns=[
            seqio.metrics.accuracy,
            seqio.metrics.bleu,
        ]
    )
    
    # Task para el nuevo dataset (0.8% del total)
    seqio.TaskRegistry.add(
        "gpt_oss_20b_new_dataset",
        source=seqio.TextLineDataSource(
            split_to_filepattern={
                "train": "gs://datasets-training_9b/datasets/new_dataset/*.txt",
                "validation": "gs://datasets-training_9b/datasets/new_dataset/validation/*.txt"
            },
            num_input_examples={
                "train": 8000,  # 0.8% de 1M ejemplos
                "validation": 80
            }
        ),
        preprocessors=[
            preprocess_text,
            seqio.preprocessors.tokenize,
            seqio.preprocessors.append_eos_after_trim,
        ],
        output_features={
            "inputs": seqio.Feature(vocabulary=vocab, add_eos=True),
            "targets": seqio.Feature(vocabulary=vocab, add_eos=True)
        },
        metric_fns=[
            seqio.metrics.accuracy,
            seqio.metrics.bleu,
        ]
    )

def create_finetune_mixture():
    """Crear mixture para fine-tuning con pesos específicos"""
    
    # Mixture principal para fine-tuning
    seqio.MixtureRegistry.add(
        "gpt_oss_20b_finetune",
        tasks=[
            ("gpt_oss_20b_original", 0.992),      # 99.2% del dataset original
            ("gpt_oss_20b_new_dataset", 0.008)    # 0.8% del nuevo dataset
        ],
        default_rate=1.0
    )

def create_evaluation_tasks():
    """Crear tasks específicas para evaluación"""
    
    # Task de evaluación en español
    seqio.TaskRegistry.add(
        "gpt_oss_20b_spanish_eval",
        source=seqio.TextLineDataSource(
            split_to_filepattern={
                "validation": "gs://datasets-training_9b/eval/spanish/*.txt"
            }
        ),
        preprocessors=[
            preprocess_text,
            seqio.preprocessors.tokenize,
        ],
        output_features={
            "inputs": seqio.Feature(vocabulary=vocab, add_eos=True),
            "targets": seqio.Feature(vocabulary=vocab, add_eos=True)
        },
        metric_fns=[
            seqio.metrics.accuracy,
            seqio.metrics.bleu,
            seqio.metrics.rouge,
        ]
    )
    
    # Task de evaluación técnica
    seqio.TaskRegistry.add(
        "gpt_oss_20b_technical_eval",
        source=seqio.TextLineDataSource(
            split_to_filepattern={
                "validation": "gs://datasets-training_9b/eval/technical/*.txt"
            }
        ),
        preprocessors=[
            preprocess_text,
            seqio.preprocessors.tokenize,
        ],
        output_features={
            "inputs": seqio.Feature(vocabulary=vocab, add_eos=True),
            "targets": seqio.Feature(vocabulary=vocab, add_eos=True)
        },
        metric_fns=[
            seqio.metrics.accuracy,
            seqio.metrics.bleu,
        ]
    )

def setup_all_tasks():
    """Configurar todas las tasks y mixtures"""
    print("🔧 Configurando tasks de SeqIO...")
    
    create_gpt_oss_task()
    create_finetune_mixture()
    create_evaluation_tasks()
    
    print("✅ Tasks configuradas:")
    print("   - gpt_oss_20b_original")
    print("   - gpt_oss_20b_new_dataset") 
    print("   - gpt_oss_20b_finetune (mixture)")
    print("   - gpt_oss_20b_spanish_eval")
    print("   - gpt_oss_20b_technical_eval")

if __name__ == "__main__":
    setup_all_tasks()
