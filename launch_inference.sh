#!/bin/bash

MODEL_PATH="C:\Users\Admin\.cache\huggingface\hub\models--google--paligemma-3b-pt-224\snapshots\35e4f46485b4d07967e7e9935bc3786aad50687c"
PROMPT="this building is "
IMAGE_FILE_PATH="test_images/pic1.jpg"
MAX_TOKENS_TO_GENERATE=100
TEMPERATURE=0.8
TOP_P=0.9
DO_SAMPLE="False"
ONLY_CPU="True"

python inference.py --model_path ""C:\\Users\\Admin\\.cache\\huggingface\\hub\\models--google--paligemma-3b-pt-224\\snapshots\\35e4f46485b4d07967e7e9935bc3786aad50687c"" --prompt "this building is" --image_file_path "test_images/pic1.jpg" --max_tokens_to_generate 100 --temperature 0.8 --top_p 0.9 --do_sample "False" --only_cpu "True"