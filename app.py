from flask import Flask, request

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
    </style>
</head>
<body>
    <h1>Count FFXIV Macro Times</h1>
    <form method="POST" action="/count-macro-time">
        <textarea name="macro-text" rows="10" cols="50" placeholder="Enter your FFXIV macro here"></textarea>
        <br>
        <input type="submit" value="Count Time">
    </form>
</body>
</html>
"""

@app.route('/count-macro-time', methods=['POST'])
def count_macro_time():
    macro_text = request.form['macro-text']
    total_wait_time = 0
    for line in macro_text.splitlines():
        if '<wait.' in line:
            wait_time = int(line.split('<wait.')[1].split('>')[0])
            total_wait_time += wait_time
    minutes, seconds = divmod(total_wait_time, 60)
    return generate_output(minutes=minutes, seconds=seconds)

def generate_output(minutes, seconds):
    return f"""
<!DOCTYPE html>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<html>
<head>
    <title>Count FFXIV Macro Times</title>
</head>
<body>
    <h1>Total Wait Time:</h1>
    <p>{minutes} minutes, {seconds} seconds</p>
</body>
</html>
"""

