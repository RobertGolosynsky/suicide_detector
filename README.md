1. install git
2. git clone https://github.com/RobertGolosynsky/suicide_detector.git
3. pip3 install -r requirements.txt
4. python3 get_data.py //to collect song lyrics (suicidal and not suicidal) warning: <1 hour
5. python3 classification.py // to create models (saved in checkpoints folder)
6. python3 predict_server.py // web server demo, go to localhost:5000
7. python3 predict_console.py // for a console version
8. python3 cross_validated_classification.py // to extimate hyperparameters for a tfidf_svc pipeline (warning takes 5 hours)
 
Folders:
1. checkpoints
	Each folder inside checkpoints/ is "checkpoint %time" and is a save of a classification.py run.
	It has all the models saved with pickle (.model), their reports (.report) and confusion matrix diagrams (.png)
2. css
	Web server served css files are there
3. dataset 
	In /dataset the 3 .txt files contain the list of artists to download lyrics from (see config.py and get_data.py for labeling each file)
4. fonts
	Contains .ttf file for creating colored text lyrics (for the web app)
5. image
	Served with predict_server.py. Contains text lyrics drawn with respect to word suicidability
6. js
	Web app js files 
7. static
	Server .html files


Configuration:
	Done in python only. See config.py for folder names mapping. Categories are also named there.
	For other config please refer to python code itself =)