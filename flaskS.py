from flask import Flask, render_template
# import contentBased
import pandas as pd

app = Flask(__name__)

@app.route('/<name>')
def getR(name):
    if name:
        df = contentBased.get_recomm(title=name)
    else:
        df = contentBased.get_recomm()
    df = pd.DataFrame(df)
    df = df.to_html()
    return render_template('index.html', movie=df)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
