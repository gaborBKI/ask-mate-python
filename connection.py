import data_manager
import operator

def change_vote(type, direction, type_id):
    data = data_manager.get_all_data(f'{type}.csv')
    if type == 'question':
        title_list = data_manager.TITLE_LIST_Q
    else:
        title_list = data_manager.TITLE_LIST_A
    for row in data:
        if row[0] == int(type_id) and direction == "up":
            if type == 'question':
                row[3] += 1
            else:
                row[2] += 1
        elif row[0] == int(type_id) and direction == "down":
            if type == 'question':
                row[3] -= 1
            else:
                row[2] -= 1
    data_manager.save_into_file(data, title_list, f'{type}.csv')

def get_order_by_user(order, questions, status):
    if 'status':
        if order:
            questions = sorted(questions, key=operator.itemgetter(status), reverse=True)
        else:
            questions = sorted(questions, key=operator.itemgetter(status))
    return questions