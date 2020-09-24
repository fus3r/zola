import discord
import requests
import datetime
import json


def time_converter(time):
    converted_time = datetime.datetime.fromtimestamp(
        int(time)
    ).strftime('%I:%M %p')
    return converted_time



def get_weather(ville):
    api_key = "7fa29540945b8ce7e5b329b5b5497def"
    url = "http://api.openweathermap.org/data/2.5/weather?appid=" + api_key + "&q=" + ville + "&units=metric"
    response = requests.get(url)
    resp_js = response.json()
    if resp_js["cod"] != "404":
        main = resp_js["main"]
        temp_min=main["temp_min"]
        temp_max=main["temp_max"]
        temperature_kelvin = main["temp"]

        pression_atmos = main["pressure"]
        humidite = main["humidity"]
        sys = resp_js["sys"]
        sunrise=time_converter(sys["sunrise"])
        sunset=time_converter(sys["sunset"])
        last_update=time_converter(resp_js["dt"])

        meteo = resp_js["weather"]
        description = meteo[0]["description"]

        embed = discord.Embed(
            title='Weather in ' + ville.capitalize(),
            description=':date: Today, the ' + str(datetime.date.today()) + "  :date:",
            colour=discord.Colour.blue()
        )

        if description == 'overcast clouds':
            description = 'Overcast clouds, no tanning today...'
            embed.set_thumbnail(url='https://videohive.img.customer.envatousercontent.com/files/135987809/Image%20Preview.jpg?auto=compress%2Cformat&fit=crop&crop=top&max-h=8000&max-w=590&s=82bef0305e018a34f793bba8a2f0615c')
        elif description == 'broken clouds' or description == 'scattered clouds':
            description = 'Broken clouds, sunny spots around'
            embed.set_thumbnail(url='https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/625a747a-061b-477d-958f-a0d6cea9e4cb/dax9bd4-dd0da73d-5b6e-415c-b05e-19471f366e5a.jpg/v1/fill/w_1024,h_768,q_75,strp/broken_clouds_by_kevintheman_dax9bd4-fullview.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3siaGVpZ2h0IjoiPD03NjgiLCJwYXRoIjoiXC9mXC82MjVhNzQ3YS0wNjFiLTQ3N2QtOTU4Zi1hMGQ2Y2VhOWU0Y2JcL2RheDliZDQtZGQwZGE3M2QtNWI2ZS00MTVjLWIwNWUtMTk0NzFmMzY2ZTVhLmpwZyIsIndpZHRoIjoiPD0xMDI0In1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmltYWdlLm9wZXJhdGlvbnMiXX0.TJXNCUYtz9ZqbY1dXZAM190Palxw0hUAwzxks6t4w_M')
            
        elif description == 'few clouds':
            description = 'Mostly sunny, anyways some clouds may come by and say hello!'
            embed.set_thumbnail(url='https://live.staticflickr.com/8145/7158312491_f852e6f1c1_b.jpg')

        elif description == 'clear sky':
            description = 'Clear sky, sunny all day, in other words, have fun!'
            embed.set_thumbnail(url='https://www.softwareheritage.org/wp-content/uploads/2017/12/clearsky.png')
            
        elif description == 'light rain':
            description = 'Light rain, don\'t hesitate to take out the umbrella!'
            embed.set_thumbnail(url='https://www.dailynews.com/wp-content/uploads/2018/04/ldn-l-weather-rain-dc-11.jpg')

        elif description== 'light intensity drizzle rain':
            description = "There will be a tiny drizzle of rain, but not enough to stop you from continuing your day"
            embed.set_thumbnail(url='https://dailytimes.com.pk/assets/uploads/2018/06/15/raindrops_trees_-_pixabay-1511188578-305-1280x720.jpg')
            
        elif description == 'moderate rain':
            description = 'Pretty rainy, don\'t hesitate to take out the umbrella!'
            embed.set_thumbnail(url='https://www.dailynews.com/wp-content/uploads/2018/04/ldn-l-weather-rain-dc-11.jpg')
            
        embed.add_field(name='🌡️ Temperature (°C) : ',
                        value=str(temperature_kelvin) + " C°", inline=False)

        embed.add_field(name='❄️ Min ❄️', value=str(temp_min) + " C°",inline=True)
        embed.add_field(name='🔥 Max 🔥', value=str(temp_max) + " C°",inline=True)

        #embed.add_field(name='\u200b',value="\u200b", inline=False)

        embed.add_field(name='Atmospheric pressure: ', value=str(pression_atmos) + " hPa",
                        inline=False)
        embed.add_field(name=':droplet: Humidity (%) :droplet:', value=str(humidite) + " %",inline=False)
        
        #embed.add_field(name='\u200b',value="\u200b", inline=False)

        embed.add_field(name='🌅 Sunrise 🌅', value=str(sunrise),inline=True)
        embed.add_field(name='🌇 Sunset 🌇', value=str(sunset),inline=True)
        embed.add_field(name='🔸Description🔸 ', value=str(description),inline=False)
        embed.add_field(name='🔸Last Update from server :🔸 ', value=str(last_update),inline=False)
            


        global exists
        exists = True

        url = 'https://en.wikipedia.org/w/api.php'
        data = {
            'action' :'query',
            'format' : 'json',
            'formatversion' : 2,
            'prop' : 'pageimages|pageterms',
            'piprop' : 'original',
            'titles' : ville
        }
        response = requests.get(url, data)
        json_data = json.loads(response.text)
        try:
            if len(json_data['query']['pages']) >0:
                url=json_data['query']['pages'][0]['original']['source']
                embed.set_image(url=url)
                return embed
        except:
            embed.set_image(url="https://www.overseaspropertyforum.com/wp-content/themes/realestate-7/images/no-image.png")
            embed.add_field(name='No image. Try to write the name of the city in English, if it isn\'t the case', value="sryy",
                        inline=False)
            return embed
    else:
        embed = discord.Embed(
            title='My fellow alien, the city \"' + ville.capitalize() + '\" isn\'t on Earth!',
            description='Try again',
            colour=discord.Colour.red()
        )
        exists=False
        return embed




