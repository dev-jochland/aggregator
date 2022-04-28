# News Aggregator V2 Challenge
```NOTE:``` Backend project implemented using **FastApi, Python.** 

The core functionality of this backend project allows for a 
```user``` to get the most recent news from various news sources, 
provided the new source provide an API to access their news.

Assumptions for this project:
- Users don't need to be authenticated to use the provided endpoints.
- Two news sources(```Reddit```, ```NewsApi```) was used for this 
  project.
- Default API-KEY for ```NewsApi``` is provided, however, users can 
  provide their own API-Key should they choose to do so by signing up 
  for ```NewsApi``` and obtaining their own API-KEY.
- The environment file was purposely uploaded even though default 
  environment variables were provided where needed throughout the project.
- ```Python3.8``` is the python version for this project.

## STEPS TO RUN THIS PROJECT ON YOUR MACHINE
```NOTE:```You need to have Python3.7+ installed on your local machine
- Clone the project to your local machine by opening your terminal and 
  type:
```python
git clone https://github.com/dev-jochland/aggregator.git
```

- While still in your terminal where you originally cloned the project, 
  navigate into the cloned project by typing the following:
```python
cd aggregator/
```

- Next run the following command after navigating into the project as 
  described above, the command creates a virtual 
  environment folder named ```/venv``` within the project:
```python
python3 -m venv ./venv

**NOTE: If the following error is thrown: The virtual environment was not 
created successfully because ensurepip is not available. 

**Try installing the venv package for your python version on your system. 
If you are on Debian/Ubuntu and your python version is 3.8, run the 
command below to install the required package:

sudo apt install python3.8-venv

**After the installation is successful, run the command below to create your 
virtual environemnt

python3 -m venv ./venv
```
- while still in your terminal, activate the virtual environment. Activating a virtual environment is platform specific, so use the commands table below to activate the virtual environment for the specific shell you're currently on.
```python
Platform:
    POSIX:
        Shell:
            - bash/zsh ($ source venv/bin/activate)
            - fish ($ source venv/bin/activate.fish)
            - csh/tcsh ($ source venv/bin/activate.csh)
            - PowerShell Core ($ source venv/bin/activate.ps1)
    Windows:
        Shell:
            - cmd.exe (C:\> venv\Scripts\activate.bat)
            - PowerShell (PS C:\> venv\Scripts\Activate.ps1)
---------------------------------------------------------------------
---------------------------------------------------------------------
**Example for a bash terminal(shell), type the command below: 
  
  $ source venv/bin/activate
  
  NOTE: Exclude the dollar($) sign
```

- Install the required dependencies by running the command below
```python
pip install -r requirements.txt
```
- Run the app using the following command
```python
uvicorn main:app

**NOTE: Make sure port 8000 is free on your local machine, if not, 
they would be port conflict. If you want to specify a different 
port number of 1975 to run this application, use the command below:

uvicorn main:app --port 1975
```
- If you follow the steps above, you should be seeing the sample image below
```python
INFO:     Started server process [388230]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)

```
```NOTE``` You need to have Postman installed locally to try out this next step.
- To try out the different endpoints available for the different type of users, you can access the [postman](https://documenter.getpostman.com/view/11396719/UyrEhvCL) documentation [here](https://documenter.getpostman.com/view/11396719/UyrEhvCL).

## RUNNING THE TEST
