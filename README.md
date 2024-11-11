# Paligemma Clone
## Download model
Install weights from ```https://huggingface.co/google/paligemma-3b-pt-224/tree/main``` using git or huggingface
and after change your ```model_path``` in '''launch_inference.sh''' file 
## Config your environment
```bash
#creating environment
python -m venv venv
#activate like said in instruction
# installing all requirements
pip install -r requirements.txt
# At last run
./launch_inference.sh
```
First of all it would take some time to run, because on automate it run at cpu, but you can change it on '''launch_inference.sh''' file

