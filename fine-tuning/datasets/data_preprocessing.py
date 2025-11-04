#!/usr/bin/env python3
"""
Script de preprocesamiento de datos para fine-tuning GPT-OSS-20B
Convierte datasets de texto plano a formato compatible con SeqIO
"""

import os
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any
import tensorflow as tf

def clean_text(text: str) -> str:
    """Limpiar y normalizar texto"""
    # Remover caracteres de control
    text = ''.join(char for char in text if ord(char) >= 32 or char in '\n\t')
    
    # Normalizar espacios en blanco
    text = ' '.join(text.split())
    
    # Remover líneas vacías
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    return '\n'.join(lines)

def split_into_chunks(text: str, max_length: int = 1024) -> List[str]:
    """Dividir texto en chunks de longitud máxima"""
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0
    
    for word in words:
        if current_length + len(word) + 1 > max_length and current_chunk:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_length = len(word)
        else:
            current_chunk.append(word)
            current_length += len(word) + 1
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks

def process_file(input_file: Path, output_dir: Path, max_length: int = 1024):
    """Procesar un archivo de texto"""
    print(f"📄 Procesando: {input_file.name}")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Limpiar texto
    cleaned_text = clean_text(content)
    
    # Dividir en chunks
    chunks = split_into_chunks(cleaned_text, max_length)
    
    # Guardar chunks
    output_file = output_dir / f"{input_file.stem}_processed.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        for chunk in chunks:
            f.write(chunk + '\n')
    
    print(f"✅ Guardado: {output_file} ({len(chunks)} chunks)")

def create_tfrecord_dataset(text_files: List[Path], output_file: Path):
    """Crear dataset TFRecord para SeqIO"""
    print(f"📊 Creando TFRecord: {output_file}")
    
    def _bytes_feature(value):
        return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value.encode('utf-8')]))
    
    with tf.io.TFRecordWriter(str(output_file)) as writer:
        for text_file in text_files:
            with open(text_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        example = tf.train.Example(features=tf.train.Features(feature={
                            'text': _bytes_feature(line)
                        }))
                        writer.write(example.SerializeToString())
    
    print(f"✅ TFRecord creado: {output_file}")

def process_dataset(input_dir: Path, output_dir: Path, max_length: int = 1024):
    """Procesar un dataset completo"""
    print(f"📁 Procesando dataset: {input_dir}")
    
    # Crear directorios de salida
    processed_dir = output_dir / "processed"
    tfrecord_dir = output_dir / "tfrecords"
    processed_dir.mkdir(parents=True, exist_ok=True)
    tfrecord_dir.mkdir(parents=True, exist_ok=True)
    
    # Encontrar archivos de texto
    text_files = list(input_dir.glob("*.txt"))
    if not text_files:
        print(f"❌ No se encontraron archivos .txt en {input_dir}")
        return
    
    print(f"📄 Encontrados {len(text_files)} archivos")
    
    # Procesar cada archivo
    processed_files = []
    for text_file in text_files:
        process_file(text_file, processed_dir, max_length)
        processed_files.append(processed_dir / f"{text_file.stem}_processed.txt")
    
    # Crear TFRecord
    tfrecord_file = tfrecord_dir / "dataset.tfrecord"
    create_tfrecord_dataset(processed_files, tfrecord_file)
    
    # Crear metadata
    metadata = {
        "num_files": len(text_files),
        "num_processed_files": len(processed_files),
        "max_length": max_length,
        "tfrecord_file": str(tfrecord_file),
        "processed_files": [str(f) for f in processed_files]
    }
    
    metadata_file = output_dir / "metadata.json"
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"✅ Dataset procesado: {output_dir}")
    print(f"📊 Archivos: {len(processed_files)}")
    print(f"💾 TFRecord: {tfrecord_file}")

def main():
    """Función principal"""
    parser = argparse.ArgumentParser(description="Preprocesar datos para fine-tuning GPT-OSS-20B")
    parser.add_argument("input_dir", type=Path, help="Directorio con archivos de texto")
    parser.add_argument("output_dir", type=Path, help="Directorio de salida")
    parser.add_argument("--max_length", type=int, default=1024, help="Longitud máxima de chunks")
    
    args = parser.parse_args()
    
    if not args.input_dir.exists():
        print(f"❌ Error: {args.input_dir} no existe")
        return 1
    
    args.output_dir.mkdir(parents=True, exist_ok=True)
    
    process_dataset(args.input_dir, args.output_dir, args.max_length)
    
    print("\n🎉 Preprocesamiento completado!")
    print(f"📁 Datos procesados en: {args.output_dir}")
    print(f"📊 Siguiente paso: Subir a GCS y configurar SeqIO")
    
    return 0

if __name__ == "__main__":
    exit(main())
