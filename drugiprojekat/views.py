from django.shortcuts import render, redirect 
from django.http import HttpResponse, response 
import re
import requests
# Create your views here.
def poziv(link): 
    response = requests.get(link, allow_redirects= False)
            #odgovori.append(response.status_code) 
    if response.status_code == 200: 
       return link + " Http response: 200 OK length: " + str(len(response.content)) 
    if response.status_code == 301: 
        return link + " Http response: 301 Redirect length: " + str(len(response.content)) + " redirected to " + poziv(response.headers["Location"])
       
    if response.status_code == 302: 
        return link + " Http response: 302 Redirect length: " + str(len(response.content)) + " redirected to " + poziv(response.headers["Location"])
        
    if response.status_code != 200 and response.status_code != 301 and response.status_code != 302: 
        return link + " Http response: " + str(response.status_code) + "Unknown length: " + str(len(response.content))

def index(request): 
    context = {
        "url": "test"
    }
    if request.method == "POST": 
        url = request.POST["url"]
        linkovi = pronadji_vrednost(url) 
        if len(linkovi) < 1000: 
            odgovori = [] 
            for i in range (len(linkovi)): 
                odgovori.append(poziv(linkovi[i][0]))
                
            context["url"] = odgovori
        else: 
           context["url"] = "Prosledjeno je vise od 1000 URL-ova. Greska!"
         
       # return redirect(request, url, "batch.html")
    return render(request, "home.html", context)

def pronadji_vrednost(vredsnost): 
    kljuc = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(kljuc,vredsnost)
    return url