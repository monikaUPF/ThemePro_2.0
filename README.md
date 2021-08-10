# ThemePro_2.0

This code is part of a scientific publication presented in the Show&tell track of INTERSPEECH 2021. It is a second iteration of a previous demo published in LREC2020 that could not be presented due to the conference cancellation for the COVID-19 pandemic.

Please, cite these papers if you use this code:

Dominguez, M., Soler, J., & Wanner, L. (2021). ThemePro: 2.0: Showcasing the Role of Thematic Progression in Engaging Human-Computer Interaction. In Proceedings of INTERSPEECH, Brno, Czechia.

Dominguez, M., Soler, J., & Wanner, L. (2020). ThemePro: A Toolkit for the Analysis of Thematic Progression. In Proceedings of The 12th Language Resources and Evaluation Conference (pp. 1000-1007).

To run the demo, you will need a working Docker installation to run the TTS application (See https://www.docker.com/get-started).

The website runs locally on your computer. Please, make sure you follow the installation instructions below. 

WARNING: Spacy and neuralcoref versions may cause failure if they do not meet these requirements.

## Installation instructions

```
apt-get update
apt-get install build-essential python3 python3-dev python3-pip git -y
apt-get upgrade -y
pip3 install -U pip setuptools wheel
pip3 install -U spacy==2.3.1
pip3 install numpy scipy flask flask-jsonpify gensim
python3 -m spacy download en_core_web_lg-2.3.1 --direct

git clone https://github.com/huggingface/neuralcoref.git
cd neuralcoref && pip3 install -r requirements.txt && pip3 install -e .

git clone https://github.com/monikaUPF/ThemePro_2.0.git 
cd /[path_to_your_folder]/ThemePro_2.0/backend/embeddings 

wget https://s3.amazonaws.com/dl4j-distribution/GoogleNews-vectors-negative300.bin.gz
mv GoogleNews-vectors-negative300.bin.gz google.bin.gz

cd /[path_to_your_folder]/ThemePro_2.0/frontend/ 
mkdir /var/www/html/themePro/ && cp -R * /var/www/html/themePro/
pip3 install sklearn
pip3 install flask_cors
pip3 install python-Levenshtein
```

## Running the demo

1) Navigate to the ThemePro_2.0/ folder in your computer, download the TTS repository and run the docker:

```
git clone https://github.com/synesthesiam/docker-mozillatts.git
cd /[local_path_to_folder]/ThemePro_2.0/docker-mozillatts
sudo docker run -it -p 5002:5002 synesthesiam/mozillatts:en
```

* Wait until you see this message at the bottom of terminal ouput:

[INFO]  Running on http://0.0.0.0:5002/ (Press CTRL+C to quit)


2) Open a second terminal and change directory to the backend folder inside ThemePro_2.0. Then, run the main script called "themazo.py":

```
cd /[local_path_to_folder]/ThemePro_2.0/backend
python3 themazo.py
```
* Embeddings take a short while to load. Please, be patient and wait until you see these lines at the bottom of the terminal output:

Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)


3) Open a tab in your browser and go to http://localhost/ThemePro

4) Copy-paste or write a text in the main box and click on run. Then, navigate to the desired tag to see the output.

* Remember you must click on the Synth button to call the TTS and thus generate the speech output.

