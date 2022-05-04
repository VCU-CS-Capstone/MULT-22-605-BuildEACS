To run the website, follow these instructions.
1) Download this folder and CD into it in Terminal/Directory

NOTE 1: When you install python please install python 3.7

2) Create a virtual environment following these directions:
    - Install Homebrew using: /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
    - Run this command: nano ~/.bash_profile once that file opens 
    - add to the file opened in nano: export PATH=/usr/local/bin:$PATH
    - To save that file, hit control o and hit return. Then to exit hit control x
    - Run the command source ~/.bash_profile
    - Run brew install python3 to install python
    - CD into the Website folder (this folder) and run python3.7 -m venv my_env
    - activate the environment by running source my_env/bin/activate

3) To open up the website in the environment, follow these directions:
    - In the env you just created, run this command: pip install flask
    - also run this command to install flask_mysql connector: pip install flask-mysql
    - run: export FLASK_APP=hello
    - then run: export FLASK_ENV=development
    - finally run: flask run
    - Open a browser and run http://127.0.0.1:5000/ 
    
 For more help, visit these websites: 
 - https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-local-programming-environment-on-macos
 - https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3

