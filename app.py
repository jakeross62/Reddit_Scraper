from flask import Flask, make_response, render_template, flash, redirect, url_for, request
from database import engine
from sqlalchemy import text
import cleanlink as cl
import API
import json
import database_query as dbq
import pandas as pd
from urllib.parse import urlparse
import os

app = Flask(__name__,static_folder='static')

def max_displayed(list): # Checks number of posts found and sets limit to be displayed.
    if len(list) > 5:
        return 5
    else:
        return len(list)

# Index of website, Uses Both POST and GET (but it might not need GET)
@app.route("/", methods =['POST', 'GET'])
def index():
    recent= dbq.past_searches(0, None) 
    return render_template("index.html", recent=recent)


# Returns the Results page, variable link requests the value of the form once it has been submitted using the POST from index's form. 
# Once Database has been setup, we can easily store the 5 most recent searches inside it (Only requires one single table for such with 
# a maximum character limit of 500, since that is the limit for a search query using the API's)
# Furthermore, it sets the variable link to link (inside the results.html)

@app.route("/results", methods =['POST', 'GET'])
def results():
    post_or_get = None
    if request.method == 'POST':
        link = request.form.get('q')
        post_or_get = 'POST'
    else:
        link = request.args.get('q')
        post_or_get = 'GET'
    download_link = link
    
    # Prepends https:// to the link if it is not already there.
    # PRAW submission link parameter expects https:// or http://
    if "https://" not in link and "http://" not in link: 
        link = "https://" + link
            
    # Checks if link is a reddit post
    # If it is, it will get the links inside the post.
    if 'reddit.com/r/' in link and '/comments/' in link:
        link = API.get_links_in_reddit_post(link)
            
    if (not API.validate_link(link)):
        return redirect(url_for('error', eidx=3, q=link))
    
    # Adds link and its data to the database.
    dbq.past_searches(1, post_or_get) 
        
    # Get the icon of the website from a given link.
    image_link = cl.clean_link(link)
    parsed_link = urlparse(image_link)
    website_link = parsed_link.netloc
    if website_link.startswith('i.'):
        website_link = 'www.' + website_link[2:]
    icon_url = f'https://icons.duckduckgo.com/ip3/{website_link}.ico'
    
    # Performs search and creates dictionary for each post.
    search_data = dbq.past_searches(2, post_or_get) 
    
    # Checks for the Search Data, if it is empty or invalid, it will redirect to the error page.
    if search_data is None or len(search_data) == 0:
        return redirect(url_for('error', eidx=1, q=link))
    
    if (not API.validate_link(link)):
        return redirect(url_for('error', eidx=3, q=link))

    # Creates a dictionary with the data to be displayed on the results page.
    # Preceded by guard clauses to prevent errors.
    data = {'top_length' : max_displayed(search_data),'total_length' : len(search_data['Title']), 'total_upvotes' : 0, 'total_downvotes' : 0, 'total_score' : 0, 'total_comments' : 0, 'top_subreddits': []}
    graph_data = [[], [], [], [], ["Total Upvotes", "Total Downvotes"], []]
    # Sums the total of each category for single integer.
    for i in range(len(search_data['Upvotes'])): 
        search_data['Score'][i] = search_data['Upvotes'][i] - search_data['Downvotes'][i]
        data['total_upvotes'] += search_data['Upvotes'][i]
        data['total_downvotes'] += search_data['Downvotes'][i]
        data['total_score'] += (search_data['Upvotes'][i] - search_data['Downvotes'][i])
        data['total_comments']+= search_data['Total Comments'][i] 
        graph_data[2].append("")
        # Data required for graphs and overall data.
        graph_data[3].append(search_data['Score'][i]) 

    data['top_subreddits'] = pd.Series(search_data['Subreddits']).value_counts().sort_values(ascending=False).index.tolist() # Ordered list of most common subreddits posted on.
    graph_data[5].append(data['total_upvotes'])
    graph_data[5].append(data['total_downvotes'])
    temp_data_subreddits = {search_data['Subreddits'][i] : 0 for i in range(len(search_data['Subreddits']))}

    for i in range(len(search_data['Subreddits'])):
        temp_data_subreddits[search_data['Subreddits'][i]] += (search_data['Upvotes'][i] - search_data['Downvotes'][i])

    for i in temp_data_subreddits:
        graph_data[0].append(i)
        graph_data[1].append(temp_data_subreddits[i])

    return render_template("results.html", link=link, search_data=search_data, data=data, icon_url = icon_url, download_link = download_link, graph_data=graph_data)


SELECT_QUERY = "SELECT jdata FROM main WHERE link = (:link)"

@app.route('/download')
def download():
    search_query = request.args.get('q')
    if search_query is None:
        return redirect(url_for('error', eidx=3, q='There was no link provided!'))
    else:
        with engine.connect() as conn:
            result = conn.execute(text(SELECT_QUERY), {"link": search_query}).fetchone()
            if result and result[0]:
                json_data = result[0]
                response = make_response(json_data)
                response.headers['Content-Disposition'] = 'attachment; filename=raw_data.json'
                response.headers['Content-Type'] = 'application/json'
                return response
            else:
                return redirect(url_for('error', eidx=2, q=search_query))

@app.route('/error')
def error():
    link = request.args.get('q')
    eidx = request.args.get('eidx')
    return render_template('error.html', link=link, eidx=int(eidx))

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
