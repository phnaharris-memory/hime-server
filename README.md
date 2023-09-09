# HIME SERVER

Use the following command for deployment:

Create a new virtual environment named hime and activate it:

```
python -m venv hime
source ./hime/bin/activate
```

Install dependencies:

```
pip install -r requirements.txt
```

Install the missing `libgl1`` dependencies:

```
sudo apt install libgl1
```

Start the server at port 3000:

```
NGROK_ENDPOINT=https://....ngrok.io uvicorn app:app --port 3000
```
