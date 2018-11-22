import csv
import os
import time

DATA_FILE_PATH_Q = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'question.csv'
DATA_FILE_PATH_A = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'answer.csv'
TITLE_LIST_Q = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
TITLE_LIST_A = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def get_all_data(filename):
    data = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        next(reader, None)
        for line in reader:
            data.append(line)
    for i in range(len(data)):
        data[i] = [int(item) if item.strip('-').isdigit() else item for item in data[i]]
    return data


def save_into_file(data, header_type, filename):
    data.insert(0, header_type)
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        for row in data:
            if any(row):
                writer.writerow(row)


def append_answer_into_file(id, qid, text):
    with open("answer.csv", "a") as file:
        writer = csv.writer(file)
        writer.writerow([id, int(time.time()), 0, qid, text])
