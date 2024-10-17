import aiohttp
import asyncio
from flask import Flask, render_template
from bs4 import BeautifulSoup

app = Flask(__name__)

classmates = [
    {'username': 'shubhamjee', 'name': 'Shubham'},
    {'username': 'rajdeep_10', 'name': 'Rajdeep'},
    {'username': 'sujal_appa', 'name': 'Sujal'},
    {'username': 'geeekyvishal', 'name': 'Vishal'},
    {'username': 'chirp_z', 'name': 'Tanishq'},
    {'username': 'abhijeeth_1221', 'name': 'Abhijeet'},
    {'username': 'raghavgod', 'name': 'Raghav'},
    {'username': 'satyamdeo', 'name': 'Satyam'},
    {'username': 'vivekpreetham', 'name': 'Vivek'},
    {'username': 'yashvikram30', 'name': 'Yash'},
    {'username': 'animesh_7872', 'name': 'Animesh'},
    {'username': 'akshaynaroliya', 'name': 'Akshay'},
]


async def get_codechef_ratings(session, username):
    url = f"https://www.codechef.com/users/{username}"
    try:
        async with session.get(url) as response:
            page = await response.text()
            soup = BeautifulSoup(page, 'html.parser')

          
            current_rating_div = soup.find('div', class_='rating-number')
            current_rating = current_rating_div.text.strip() if current_rating_div else 'N/A'

            max_rating_div = soup.find('div', class_='rating-header text-center').find('small')
            if max_rating_div:
                max_rating_text = max_rating_div.text.strip()
                max_rating = int(max_rating_text.split()[-1].strip('()'))
            else:
                max_rating = 0

            return int(current_rating) if current_rating != 'N/A' else 0, max_rating
    except Exception as e:
        print(f"Error fetching {username}: {e}")
        return 0, 0


def calculate_stars(rating):
    if rating < 1400:
        return 1
    elif rating < 1600:
        return 2
    elif rating < 1800:
        return 3
    elif rating < 2000:
        return 4
    elif rating < 2200:
        return 5
    elif rating < 2400:
        return 6
    else:
        return 7

@app.route('/')
async def leaderboard():
    async with aiohttp.ClientSession() as session:
       
        tasks = [get_codechef_ratings(session, student['username']) for student in classmates]
        ratings = await asyncio.gather(*tasks)

       
        for i, (current, max_rating) in enumerate(ratings):
            classmates[i]['current_rating'] = current
            classmates[i]['max_rating'] = max_rating
            classmates[i]['stars'] = calculate_stars(current)

        sorted_classmates = sorted(classmates, key=lambda x: x['current_rating'], reverse=True)

        return render_template('leaderboard.html', classmates=sorted_classmates)

if __name__ == '__main__':
    app.run(debug=True)
