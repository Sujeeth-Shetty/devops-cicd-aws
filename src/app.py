from flask import Flask
import requests
import mysql.connector
import boto3
import json
import ast

app = Flask(__name__)

def get_rds_credentials():
    secret_name = 'rds_credentials'
    region_name = 'us-east-1'
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)
    response = client.get_secret_value(SecretId=secret_name)
    secret_string = response['SecretString'].strip()
    return ast.literal_eval(secret_string)

@app.route('/')
def random_gif():
    rds_credentials = get_rds_credentials()
    connection = mysql.connector.connect(user=rds_credentials['username'], password=rds_credentials['password'],host=rds_credentials['host'],database='devops')
    cursor = connection.cursor()
    # Retrieve a random URL from the 'urls' table
    select_query = "SELECT url FROM urls ORDER BY id LIMIT 1"
    cursor.execute(select_query)
    result = cursor.fetchone()
    if result:
        url = result[0]
    else:
        return '<h1>No URLs found in the database</h1>'
    
    #url = 'https://api.giphy.com/v1/gifs/random?api_key=4Tc2wgmb3ybDuEITwZWM5nCQgHyzqyEj&tag=dog&rating=g'
    r = requests.get(url)

    if r.status_code == 200:
        data = r.json()
        img_url = data['data']['images']['original']['url']

        # Store the image URL in the database with a unique ID
        insert_query = "INSERT INTO images (id, url) VALUES (NULL, %s)"
        cursor.execute(insert_query, (img_url,))
        connection.commit()

        return '<img src="{}"/>'.format(img_url)
    else:
        return '<h1>HTTP - {}</h1>'.format(r.status_code)
    return 
#def random_gif():
#    url = 'https://api.giphy.com/v1/gifs/random?api_key=4Tc2wgmb3ybDuEITwZWM5nCQgHyzqyEj&tag=dog&rating=g'
#    r = requests.get(url)
#    
#    if r.status_code == 200:
#        data = r.json()
#        img_url = data['data']['images']['original']['url']
#        return '<img src="{}"/>'.format(img_url)
#    else:
#        return '<h1>HTTP - {}</h1>'.format(r.status_code)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')

