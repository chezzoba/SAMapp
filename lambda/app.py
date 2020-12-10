import boto3
import datetime
from os import environ

sns = boto3.client('sns')
dynamodb = boto3.client('dynamodb')


def send_msg(msg):
    params = {
        'Message': msg,
        'Subject': "Today's Lifts",
        'TopicArn': environ['SNS_TOPIC']
      }
    return sns.publish(**params)


def get():
    params = {
        'RequestItems': {
            environ['DDB_TABLE']: {'Keys': [{"key": {'S': "stats"}}]}
        }}
    res = dynamodb.batch_get_item(**params)
    return res['Responses'][environ['DDB_TABLE']][0]


def weightcalc(weight, percent): return round(weight * percent / 250) * 2.5


def processor(weight, week):
    if week == 5:
        data = [weightcalc(weight, 65),
            weightcalc(weight, 75),
            weightcalc(weight, 85),
            weightcalc(weight, 65)]
    elif week == 3:
        data = [weightcalc(weight, 70), 
            weightcalc(weight, 80),
            weightcalc(weight, 90),
            weightcalc(weight, 70)]
    else:
        data = [weightcalc(weight, 75), 
            weightcalc(weight, 85),
            weightcalc(weight, 95),
            weightcalc(weight, 75)]
    return data


def determine(lifdic):
    day = datetime.datetime.now().weekday()
    week = int(lifdic['week']['N'])
    values = [v['S'] for v in lifdic['schedule']['L']]
    lift = values[day]
    weight = float(lifdic[lift]['N'])
    text = [f'{week} reps @ ', 
    f'{week} reps @ ', 
    f'{week}+ reps @ ',
    f'5x5 @ ']
    msg = 'Good Morning Kaizad,\n'
    if lift == 'rest':
        msg += 'Today is your Rest Day!'
    elif lift == 'deadlift':
        msg += 'Today you are doing deadlifts of '
        msg += lifdic[lift]['N'] + ' kg for 3x5 reps'
    else:
        msg += 'Today you are doing the ' + lift + ' for:'
        data = processor(weight, week)
        for i in range(len(text)):
            msg += '\n' + text[i] + str(data[i]) + ' kg'
    
    if week == 1:
        if lift == 'deadlift':
            lifdic[lift]['N'] = str(weight + 5)
        else:
            lifdic[lift]['N'] = str(weight + 2.5)
    lifdic['test'] = {'N': str(int(lifdic['test']['N']) + 1)}
    neweek = 5 if week == 1 else (1 if week == 3 else 3)
    lifdic['week'] = {'N': str(neweek)} if lift == 'rest' else lifdic['week']
    return msg, lifdic


def put(lifdic):
    params = {'RequestItems': {
        environ['DDB_TABLE']: [
            {
                'PutRequest': {'Item': lifdic}
            }
        ]
    }}
    return dynamodb.batch_write_item(**params)


try:
    get()
except IndexError:
    put({"bench press":{"N":"82.5"},"bent over row":{"N":"77.5"},"deadlift":{"N":"130"},
         "Endpoint":{"S":"4twbzcqm75.execute-api.eu-west-2.amazonaws.com"},"key":{"S":"stats"},
         "overhead press":{"N":"60"},
         "schedule":{"L":[{"S":"overhead press"},{"S":"squat"},{"S":"bent over row"},{"S":"bench press"},
                          {"S":"squat"},{"S":"rest"},{"S":"deadlift"}]},"squat":{"N":"115"},
         "test":{"N":"37"},"week":{"N":"5"}})


def format(output):
    initial = '<h3 style="text-align: center">'
    final = '</h3>'
    return initial + output + final


def lambda_handler(event, context):
    lifdic = get()
    if "queryStringParameters" in event.keys() and "httpMethod" in event.keys():
        liflist = lifdic['schedule']['L']
        params = event["queryStringParameters"]
        if 'unskip' in params['act']:
            first = liflist.pop(0)
            new_lst = liflist + [first]
            output = format('Unskipped successfully!')
            output += f'<h3>New schedule: {", ".join([v["S"] for v in new_lst])}</h3>'
            lifdic['schedule']['L'] = new_lst
        elif 'skip' in params['act']:
            last = liflist.pop()
            new_lst = [last] + liflist
            output = format('Skipped successfully!')
            output += f'<h3>New schedule: {", ".join([v["S"] for v in new_lst])}</h3>'
            lifdic['schedule']['L'] = new_lst
        elif 'change' in params['act']:
            try:
                if 'lift' in params and 'value' in params:
                    lifdic[params['lift']]['N'] = params['value']
                    output = format(f"Successfully changed {params['lift']} weight to {params['value']} kg")
                else:
                    output = format('Invalid values given for parameter lift or value')
            except KeyError:
                output = format("Invalid lift:", params['lift'])
        put(lifdic)

    else:
        api = 'https://liftapi.kaizadwadia.com'
        msg, new_lifdic = determine(lifdic)
        addendum = ['\n\n\n', 'Not going? Skip:', 
        f"{api}/?act=skip",
        '\n', 'Clicked the above link by accident? Unskip:', 
        f"{api}/?act=unskip", '\n',
        "Want to change weights? Visit:",
        'lift.kaizadwadia.com'
        '\n\n\n\n ']
        msg += '\n'.join(addendum)
        send_msg(msg)
        put(new_lifdic)
        output = 'Message sent: ' + msg
    
    return {
        'statusCode': 200,
        'body': output,
        "headers": {
            "Content-Type": "text/html",
            'Access-Control-Allow-Origin': '*'
        }
    }