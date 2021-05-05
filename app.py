from flask import Flask, redirect, url_for, jsonify
import requests
import json
import ast

app = Flask(__name__)


@app.route('/')
def index():
    return app.send_static_file("index.html")

@app.route("/trending/")
def trending_this_week():
    trending1 = requests.get("https://api.themoviedb.org/3/trending/movie/week?api_key=my_key_api").json()
    trending1_results = trending1.get("results")
    trending_length = len(trending1_results)
    Final_result = {}    
    if (trending_length>5):
        trending_length = 5 
    teMp_teMp_trend = {}    
    for m in range (trending_length):
        temp_trend = {}
        tem_rel = trending1_results[m].get("release_date","") 
        if (tem_rel == ""):
          tem_rel = "N/A"
        else:
            tem_rel = tem_rel[:4] 
        temp_trend["backdrop_path"] = trending1_results[m].get("backdrop_path",None) 
        temp_trend["bottom_heading_1"] = trending1_results[m].get("title","N/A")+" ("+ tem_rel +")"
        teMp_teMp_trend[m] = temp_trend
    Final_result["trending_movies"] = teMp_teMp_trend 

    trendinG2 = requests.get("https://api.themoviedb.org/3/tv/airing_today?api_key=my_key_api").json()
    tv_trend_results = trendinG2.get("results")
    tv_trend_length = len(tv_trend_results)
    if(tv_trend_length>5):
        tv_trend_length = 5 
    temp_all_tvs = {}

    for ui in range(tv_trend_length):
        temp_tv_each = {}
        temp_tv_each["backdrop_path"] = tv_trend_results[ui].get("backdrop_path",None)
        tempA = tv_trend_results[ui].get("name","N/A")
        tempB = tv_trend_results[ui].get("first_air_date","")
        if (tempB == ""):
            Temp_year =="N/A"
        else:
            Temp_year = tempB[:4]
        temp_tv_each["bottom_heading_2"] =  tempA +" (" +Temp_year +")"
        temp_all_tvs[ui]=temp_tv_each

    Final_result["trending_tv_shows"] = temp_all_tvs
    return json.dumps(Final_result)

@app.route("/home/<the_keyword>")  # movies keyword
def receive_data(the_keyword):
    movies1py = requests.get(
        "https://api.themoviedb.org/3/search/movie?api_key=my_key_api&query="+the_keyword).json()
    result_list = movies1py.get("results")  # get results only

    topresults = {}

    lengthmax = len(result_list)
    if(lengthmax == 0):
        return "No results found."
    elif (lengthmax > 10):  # less than 10 results
        lengthmax = 10

    for i in range(lengthmax):  # for movies, get the results
        temp = {}
        temp["id"] = result_list[i].get("id")
        temp["poster_path"] = result_list[i].get("poster_path",None)
        temp["vote_average"] = result_list[i].get("vote_average",0)
        temp["vote_count"] = result_list[i].get("vote_count",0)
        temp["title"] = result_list[i].get("title","")  # title null :done both
        if(temp["title"] == "" ): 
            temp["title"] = "N/A"
        temp["overview"] = result_list[i].get("overview","")  # overview null
        if(temp["overview"] == ""):
            temp["overview"] = "N/A"
        temp["release_date"] = result_list[i].get("release_date","")
        if (temp["release_date"] ==""):  # release date null processed here:done both
            temp["release_date"] = "N/A"
        # genre name got & null factor processed here:done both
        if ((result_list[i].get("genre_ids")) == []):
            temp["genre_name"] = "N/A"
        else:
            movie_ids_genre = result_list[i].get("genre_ids")
            genre_get = requests.get("https://api.themoviedb.org/3/genre/movie/list?api_key=my_key_api&language=en-US").json()
            mov_get = genre_get["genres"]
            ts= ""
            for ee in mov_get:
                for ye in movie_ids_genre:
                    if(ee["id"]==ye):
                        ts += ee["name"]+", "
            ts = ts[:-2]
            temp["genre_name"] = ts
        topresults[i] = (temp)
    return json.dumps(topresults)


@app.route("/searchtv/<the_keyword>") 
def receive_tv_date_search_results(the_keyword):
    tv1py = requests.get("https://api.themoviedb.org/3/search/tv?api_key=my_key_api&language=en-US&page=1&query="+the_keyword+"&include_adult=false").json()
    tv_result_list = tv1py.get("results")

    top_ten_results = {} #stores all results

    lenth_res = len(tv_result_list)
    if(lenth_res==0):
        return "No results found."
    elif(lenth_res>10):
        lenth_res=10
    
    for i in range(lenth_res):
        temp = {}
        temp["id"] = tv_result_list[i].get("id")
        temp["poster_path"] = tv_result_list[i].get("poster_path",None)
        temp["vote_average"] = tv_result_list[i].get("vote_average",0)
        temp["vote_count"] = tv_result_list[i].get("vote_count",0)
        temp["title"] = tv_result_list[i].get("name","")
        if (temp["title"]  == ""):
            temp["title"] = "N/A"
        temp["overview"] = tv_result_list[i].get("overview","")
        if (temp["overview"] ==""):
            temp["overview"] = "N/A"
        temp["release_date"] =  tv_result_list[i].get("first_air_date","")
        if(temp["release_date"] ==""):
            temp["release_date"] ="N/A"
        if(tv_result_list[i].get("genre_ids")==[]):
            temp["genre_name"] = "N/A" 
        else:
            tv_ids_genre =  tv_result_list[i].get("genre_ids")
            gen = requests.get("https://api.themoviedb.org/3/genre/tv/list?api_key=my_key_api&language=en-US").json()
            genre_get = gen["genres"]
            st = ""
            for x in genre_get:
                for y in tv_ids_genre:
                    if (x["id"] == y):
                        st += x["name"] +", "
            st = st[:-2]
            temp["genre_name"] = st
        
        top_ten_results[i] = temp
    print("hello!",top_ten_results)
    return json.dumps(top_ten_results)

@app.route("/both/<the_keyword>")
def both_data(the_keyword):
    both1py = requests.get("https://api.themoviedb.org/3/search/multi?api_key=my_key_api&language=en-US&query="+the_keyword+"&page=1&include_adult=false").json()
    both_result_list = both1py.get("results")

    top_results = {}

    total_length = len(both_result_list)
    if(total_length ==0):
        return "No results found."
    count = 0
    for i in range(total_length):
        if(count<10):
            if(both_result_list[i].get("media_type")=="movie"):
                temp = {}
                temp["media_type"] = "movie"
                temp["id"] = both_result_list[i].get("id")
                temp["poster_path"] = both_result_list[i].get("poster_path",None)
                temp["vote_average"] = both_result_list[i].get("vote_average",0)
                temp["vote_count"] = both_result_list[i].get("vote_count",0)
                temp["title"] = both_result_list[i].get("title","")  # title null :done both
                if(temp["title"] == "" ): #or tiny is None or not tiny
                    temp["title"] = "N/A"
                temp["overview"] = both_result_list[i].get("overview","")  # overview null
                if(temp["overview"] == ""):
                    temp["overview"] = "N/A"
                temp["release_date"] = both_result_list[i].get("release_date","")
                if (temp["release_date"] =="" ):  
                    temp["release_date"] = "N/A"
                if ((both_result_list[i].get("genre_ids")) == []):
                    temp["genre_name"] = "N/A"
                else:
                    movie_ids_genre = both_result_list[i].get("genre_ids")
                    genre_get = requests.get("https://api.themoviedb.org/3/genre/movie/list?api_key=my_key_api&language=en-US").json()
                    mov_get = genre_get["genres"]
                    ts= ""
                    for ee in mov_get:
                        for ye in movie_ids_genre:
                            if(ee["id"]==ye):
                                ts += ee["name"]+", "
                    ts = ts[:-2]
                    temp["genre_name"] = ts
                top_results[count]= temp
                count = count+1
            
            elif(both_result_list[i].get("media_type")=="tv"):
                temp = {}
                temp["media_type"] = "tv"
                temp["id"] = both_result_list[i].get("id")
                temp["poster_path"] = both_result_list[i].get("poster_path",None) 
                temp["vote_average"] = both_result_list[i].get("vote_average",0)
                temp["vote_count"] = both_result_list[i].get("vote_count",0)
                temp["title"] = both_result_list[i].get("name","")
                if (temp["title"]  == ""):
                    temp["title"] = "N/A"
                temp["overview"] = both_result_list[i].get("overview","")
                if (temp["overview"] ==""):
                    temp["overview"] = "N/A"
                temp["release_date"] =  both_result_list[i].get("first_air_date","")
                if(temp["release_date"] ==""):
                    temp["release_date"] ="N/A"
                tv_id = str(temp["id"] )
                if(both_result_list[i].get("genre_ids")==[]):
                    temp["genre_name"] = "N/A" 
                else:
                    tv_ids_genre =  both_result_list[i].get("genre_ids")
                    gen = requests.get("https://api.themoviedb.org/3/genre/tv/list?api_key=my_key_api&language=en-US").json()
                    genre_get = gen["genres"]
                    st = ""
                    for x in genre_get:
                        for y in tv_ids_genre:
                            if (x["id"] == y):
                                st += x["name"] +", "
                    st = st[:-2]
                    temp["genre_name"] = st
                top_results[count] = temp
                count = count+1
                
    return json.dumps(top_results)


@app.route("/TheMoviePopup/<s_id>") #MOVIES
def willgetdata(s_id):
    #spoken lang and backdrop
    get_movie_details = requests.get("https://api.themoviedb.org/3/movie/" +s_id + "?api_key=my_key_api&language=en-US").json()
    #zz = get_movie_details.get("title")
    xy = (get_movie_details.get("spoken_languages")) 
    tempo = {}
    if(xy == []):
        tempo ["language_string"] = "N/A"
    else:
        spoken_string = ""
        for ele in xy:
            spoken_string += ele["english_name"] + ", "
        spoken_string_s = spoken_string[:-2]
        tempo ["language_string"] = spoken_string_s
    tempo["backdrop_path"] = get_movie_details.get("backdrop_path",None)

    #actors
    get_movie_actors = requests.get("https://api.themoviedb.org/3/movie/"+ s_id +"/credits?api_key=my_key_api&language=en-US").json()
    cast_list = get_movie_actors.get("cast")
    data_length_of_cast_list = len(cast_list) #length
    if (data_length_of_cast_list == 0): 
         tempo["cast"] = "N/A"
    else: 
        if(data_length_of_cast_list > 8 ):
             data_length_of_cast_list = 8
        actor_data = {}
        for j in range(data_length_of_cast_list):
            temp_cast_data = {}

            temp_cast_data["name"] = cast_list[j].get("name","")
            if(temp_cast_data["name"] == "" ): #cast name is null:or cast_name is None or not cast_name
                temp_cast_data["name"] = "N/A"

            temp_cast_data["character"] = cast_list[j].get("character","")
            if( temp_cast_data["character"] == "" ): #or character_name is None or not character_name
                temp_cast_data["character"] = "N/A" ##CONFIRMED!

            temp_cast_data["profile_path"] = cast_list[j].get("profile_path",None) 
            actor_data [j] = temp_cast_data    
        tempo["cast"] = actor_data #works

       

    #reviews
    get_movie_reviews = requests.get("https://api.themoviedb.org/3/movie/"+s_id +"/reviews?api_key=my_key_api&language=en-US&page=1").json()
    review_list = get_movie_reviews.get("results")
    result_length = len(review_list)
    if(result_length == 0):
        tempo["reviews"] = "N/A"
    else:
        if(result_length>5):
            result_length = 5
        review_data = {}   
        for k in range(result_length):
            review_temp_data = {}
            review_temp_data["author"] = review_list[k].get("author")
            author_details = review_list[k].get("author_details") 
            review_temp_data["username"] = author_details.get("username","")
            if(review_temp_data["username"] == ""):
                review_temp_data["username"] = "N/A"
            review_temp_data["rating"] = author_details.get("rating",None)
            review_temp_data["content"] = review_list[k].get("content","")
            if( review_temp_data["content"] == ""):
                review_temp_data["content"] = "N/A"
            temp_time  = review_list[k].get("created_at","") #review_temp_data["created_at"]
            if(temp_time ==""):
                review_temp_data["created_at"] = "N/A"
            else:
                temp_year = temp_time[:4]
                temp_month = temp_time[5:7]
                temp_day = temp_time[8:10]
                review_temp_data["created_at"] = temp_month+"/"+temp_day+"/"+temp_year

            review_data[k] = review_temp_data
        tempo["reviews"] = review_data
    return json.dumps(tempo)


@app.route("/TheTVPopup/<s_id>")
def tv_popup(s_id):
     #spoken lang and backdrop

    get_tv_details = requests.get("https://api.themoviedb.org/3/tv/" +s_id + "?api_key=my_key_api&language=en-US").json()
    
    tempo = {}
    xy = (get_tv_details.get("spoken_languages")) 
    if(xy == []):
        tempo ["language_string"] = "N/A"
    else:
        spoken_string = ""
        for ele in xy:
            spoken_string += ele["english_name"] + ", "
        spoken_string_s = spoken_string[:-2]
        tempo ["language_string"] = spoken_string_s

    tempo["backdrop_path"] = get_tv_details.get("backdrop_path",None)

    
    #actors
    get_tv_actors = requests.get("https://api.themoviedb.org/3/tv/"+ s_id +"/credits?api_key=my_key_api&language=en-US").json()
    cast_list = get_tv_actors.get("cast")
    data_length_of_cast_list = len(cast_list) #length
    if (data_length_of_cast_list == 0): 
        tempo["cast"] = "N/A"
    else: 
        if(data_length_of_cast_list > 8 ):
             data_length_of_cast_list = 8
        actor_data = {}
        for j in range(data_length_of_cast_list):
            temp_cast_data = {}

            temp_cast_data["name"] = cast_list[j].get("name","")
            if(temp_cast_data["name"] == "" ): #cast name is null:or cast_name is None or not cast_name
                temp_cast_data["name"] = "N/A"

            temp_cast_data["character"] = cast_list[j].get("character","")
            if( temp_cast_data["character"] == "" ): #or character_name is None or not character_name
                temp_cast_data["character"] = "N/A" ##CONFIRMED!

            temp_cast_data["profile_path"] = cast_list[j].get("profile_path",None) 

            actor_data [j] = temp_cast_data    
        tempo["cast"] = actor_data #works

    #reviews 
    get_tv_reviews = requests.get("https://api.themoviedb.org/3/tv/"+s_id +"/reviews?api_key=my_key_api&language=en-US&page=1").json()
    review_list = get_tv_reviews.get("results")

    result_length = len(review_list)
    if(result_length == 0):
        tempo["reviews"] = "N/A"
    else:
        if(result_length>5):
            result_length = 5

        review_data = {}   
        for k in range(result_length):
            review_temp_data = {}
            author_details = review_list[k].get("author_details") 
            review_temp_data["username"] = author_details.get("username","")
            if(review_temp_data["username"] == ""):
                review_temp_data["username"] = "N/A"
            review_temp_data["rating"] = author_details.get("rating",None)
            review_temp_data["content"] = review_list[k].get("content","")
            if( review_temp_data["content"] == ""):
                review_temp_data["content"] = "N/A"
            temp_time  = review_list[k].get("created_at","") 
            if(temp_time ==""):
                review_temp_data["created_at"] = "N/A"
            else:
                temp_year = temp_time[:4]
                temp_month = temp_time[5:7]
                temp_day = temp_time[8:10]
                review_temp_data["created_at"] = temp_month+"/"+temp_day+"/"+temp_year

            review_data[k] = review_temp_data
        tempo["reviews"] = review_data
    return json.dumps(tempo)
if __name__ == "__main__":
    app.run(debug=True)
