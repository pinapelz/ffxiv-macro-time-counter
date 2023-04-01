from flask import Flask, request
from datetime import timedelta

app = Flask(__name__)

@app.route('/')
def main_page():
    return """
    <!DOCTYPE html>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<html>
<head>
    <title>Count FFXIV Macro Times</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f2f2f2;
            margin: 0;
            padding: 0;
        }
        h1 {
            font-size: 36px;
            color: #333;
            margin-top: 20px;
            margin-bottom: 20px;
            text-align: center;
        }
        form {
            margin-top: 20px;
            margin-bottom: 20px;
            text-align: center;
        }
        textarea {
            width: 100%;
            padding: 10px;
            font-size: 16px;
            border: 2px solid #ccc;
            border-radius: 4px;
            resize: vertical;
        }
        input[type=submit] {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
        input[type=submit]:hover {
            background-color: #45a049;
        }
        p {
            font-size: 24px;
            color: #333;
            text-align: center;
        }
        label {
            font-size: 16px;
            color: #333;
            margin-right: 10px;
        }
        input[type=number] {
            width: 80px;
            padding: 10px;
            font-size: 16px;
            border: 2px solid #ccc;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <h1>Count FFXIV Macro Times</h1>
    <form method="POST" action="/count-macro-time">
        <textarea name="macro-text" rows="10" cols="50" placeholder="Enter your FFXIV macro here"></textarea>
        <br>
        <label for="num-executions">Number of executions:</label>
        <input type="number" name="num-executions" id="num-executions" min="1" value="1">
        <br>
        <input type="submit" value="Calculate">
    </form>
</body>
</html>
"""


@app.route('/count-macro-time', methods=['POST'])
def count_macro_time():
    macro_text = request.form['macro-text']
    total_wait_time = 0
    num_executions = request.form.get('num-executions', 1) # set default value to 1
    for line in macro_text.splitlines():
        if '<wait.' in line:
            wait_time = int(line.split('<wait.')[1].split('>')[0])
            total_wait_time += wait_time
        elif line.startswith('/wait '):
            wait_time = int(line.split('/wait ')[1])
            total_wait_time += wait_time

    minutes, seconds = divmod(total_wait_time * int(num_executions), 60)
    return generate_output(minutes=minutes, seconds=seconds, num_executions=num_executions, macro_text=macro_text)

def generate_output(minutes, seconds, num_executions, macro_text):
    total_seconds = (minutes * 60) + seconds
    num_executions = int(num_executions)
    total_time = timedelta(seconds=total_seconds * num_executions)
    # report ack in x hours y minutes z seconds
    hours = total_time.seconds // 3600
    minutes = (total_time.seconds // 60) % 60
    seconds = total_time.seconds % 60
    total_time_str = f'{hours} hours {minutes} minutes {seconds} seconds'

    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Count FFXIV Macro Times</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f7f7f7;
            margin: 0;
            padding: 0;
        }}

        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}

        h1 {{
            font-size: 2rem;
            text-align: center;
            margin-top: 0;
        }}

        form {{
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-bottom: 20px;
        }}

        textarea {{
            width: 100%;
            margin-bottom: 10px;
            padding: 10px;
            font-size: 1.2rem;
            border: 2px solid #ccc;
            border-radius: 5px;
            resize: vertical;
        }}

        input[type="submit"] {{
            padding: 10px 20px;
            font-size: 1.2rem;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }}

        input[type="submit"]:hover {{
            background-color: #3e8e41;
        }}

        .output {{
            text-align: center;
            font-size: 1.2rem;
            padding: 20px;
            background-color: #fff;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Count FFXIV Macro Times</h1>
        <form method="POST" action="/count-macro-time">
            <textarea name="macro-text" rows="10" cols="50">{macro_text}</textarea>
            <label for="num-executions">Number of Executions:</label>
            <input type="number" id="num-executions" name="num-executions" min="1" value="{num_executions}">
            <br>
            <input type="submit" value="Calculate">
        </form>
        <div class="output">
            <h2>Total Time:</h2>
            <p>{num_executions} craft(s) will take {total_time_str}</p>
        </div>
    </div>
</body>
</html>
"""
