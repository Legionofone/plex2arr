FROM python:3.9-alpine 
# Or any preferred Python version.
ADD requirements.txt .
RUN pip install -r requirements.txt
ADD .env .
ADD plex_to_arr.py .
CMD ["python3", "-u", "./plex_to_arr.py"] 
# Or enter the name of your unique directory and parameter set.
