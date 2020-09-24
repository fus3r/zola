import COVID19Py
import discord
from country_codes import countries
import requests
import json
import os, os.path
import urllib.parse as urlparse
import urllib


def check_server():
    try:
        covid19 = COVID19Py.COVID19(data_source="jhu")
        return True

    except:
        return False
#print(check_server())

def space_number(number):
    return ("{:,}".format(number)) 

def latest():

    covid19 = COVID19Py.COVID19(data_source="jhu")
    latest = covid19.getLatest()

    latest_embed=discord.Embed(
        title='Latest Covid Data',
        description="This shows updated information about deaths and confirmed cases. For more information, go to the [John Hopkins Covid Map](https://coronavirus.jhu.edu/map.html)",
        colour=discord.Colour.red()
        )   
    latest_embed.add_field(name="Confirmed Cases:",value=space_number(latest["confirmed"]),inline=False)
    latest_embed.add_field(name="Deaths:",value=space_number(latest["deaths"]),inline=False)
    latest_embed.set_thumbnail(url="https://www.aljazeera.com/mritems/imagecache/mbdxxlarge/mritems/Images/2020/2/26/95d3056d580c43bdb53c4f328155a590_18.jpg")
    return latest_embed



def ranked_locations(value):

    covid19 = COVID19Py.COVID19(data_source="jhu")

    dict={'c':"confirmed",'d':"deaths"}
    try:
        locations = covid19.getLocations(rank_by=dict[value])
    except:
        ranked_embed=discord.Embed(
        title="Wrong usage of `!covid rank`",
        description="For more information, please refer to ```!help covid```",
        colour=discord.Colour.red()
        )   
        return ranked_embed
    ranked_embed=discord.Embed(
        title='Top 10 countries ranked by number of '+dict[value] if value=="d" else "Top 10 countries ranked by number of "+dict[value] + " cases",
        description="This shows updated information about deaths and confirmed cases. For more information, go to the [John Hopkins Covid Map](https://coronavirus.jhu.edu/map.html)",
        colour=discord.Colour.red()
        )   
    for i in range(10):
        ranked_embed.add_field(name=str(i+1)+")- "+locations[i]["country"],value=space_number(locations[i]["latest"][dict[value]]))
    ranked_embed.set_thumbnail(url="https://www.aljazeera.com/mritems/imagecache/mbdxxlarge/mritems/Images/2020/2/26/95d3056d580c43bdb53c4f328155a590_18.jpg")
    return ranked_embed



def country_data(country):
    covid19 = COVID19Py.COVID19(data_source="jhu")

    try:
        locations = covid19.getLocationByCountryCode(countries[country])
        print("Works for country",country)


    except:
        ranked_embed=discord.Embed(
        title="Can't find the country in the Covid Database",
        description="Please try with another country",
        colour=discord.Colour.red()
        )   
        try:
            country_file_for_img=countries[country]+".png"
            file=discord.File("D:/CODING/DISCORD BOT/Bot/Images/"+country_file_for_img, filename=country_file_for_img)
            ranked_embed.set_image(url='attachment://'+country_file_for_img)
            return ranked_embed,file
        except:
            ranked_embed.set_image(url='attachment://no-image.png')
            print("Doesnt work for country",country,"maybe this",countries[country])
            file=discord.File("D:/CODING/DISCORD BOT/Bot/Images/no-image.png", filename="no-image.png")
            return ranked_embed,file

    ranked_embed=discord.Embed(
        title="Data of " + country,
        description="This shows updated information about deaths and confirmed cases. For more information, go to the [John Hopkins Covid Map](https://coronavirus.jhu.edu/map.html)",
        colour=discord.Colour.red()
        )   
    for i in locations:
        if i["province"]=="":
            ranked_embed.add_field(name="Total confirmed :",value=space_number(i["latest"]["confirmed"]),inline=True)
            ranked_embed.add_field(name="Total deaths",value=space_number(i["latest"]["deaths"]),inline=True)
    
    ranked_embed.set_thumbnail(url="https://www.aljazeera.com/mritems/imagecache/mbdxxlarge/mritems/Images/2020/2/26/95d3056d580c43bdb53c4f328155a590_18.jpg")
    country_file_for_img=countries[country]+".png"
    try:
        file=discord.File("D:/CODING/DISCORD BOT/Bot/Images/"+country_file_for_img, filename=country_file_for_img)
        ranked_embed.set_image(url='attachment://'+country_file_for_img)
        return ranked_embed,file
    except:
        ranked_embed.set_image(url='attachment://no-image.png')
        print("Doesnt work 2",ranked_embed)
        file=discord.File("D:/CODING/DISCORD BOT/Bot/Images/no-image.png", filename="no-image.png")
        return ranked_embed,file







