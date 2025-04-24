FROM python:3.9 
# Or any preferred Python version.
ADD plex_to_arr.py .
RUN pip install -r requirements.txt
CMD [“python”, “./plex_to_arr.py”]
