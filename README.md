# exercise-tracker

Sovellus löytyy Herokusta osoitteesta https://pt-exercise-tracker.herokuapp.com/

Superuser-tilin email on "admin" ja salasana "Admin1234!"
Muita käyttäjiä voi luoda "Signup"-toiminnon avulla

Sovelluksen rakenne on MVC-tyyppinen ja lähdekoodi jaettu seuraavasti:

- Kansio "alembic" - Model - tietokannan luominen (DDL), muutoksenhallinta Alembic-työkalua käyttäen
- Kansio "model" - Model - tietokannan käyttö raakaa SQLää käyttäen toteutettuna
- Kansio "blueprints" - Controller - toteutettu Flaskin Blueprint-konseptia käyttäen
- Kansio "templates" - Views - toteutettu Flaskin Jinja2 template engineä käyttäen
- Kansio "static" - Vieweissä käytetyt staattiset assetit (eli kuvat tms)

Alla sovellukselle määritetyt vaatimukset. Vaatimukset jotka on merkitty [x] on jo toteutettu, loput toteutetaan seuraavaan välitarkastukseen mennessä. 
Tiedossa olevat parannukset / bugit on listattu Github-projektin "Issues"-osiossa

## Overview

This solution supports your fitness regime and habits by allowing you to keep track of your exercise sessions - e.g. running routes/times, gym visits/sets, swim sessions/laps. It also provides helpful statistics of exercises to ensure you stay on track to improve your fitness. 

## Key features

- [x] User can log in and out, and create new user account
- [x] User can see a list of all exercise sessions they have recorded, and key statistics about each
- [x] User can create a new exercise session and log information about it
- [x] User can modify / correct / delete sessions entered incorrectly / by mistake
- [x] User can delete their account and all information related to it
- [x] User can view summary statistics about their exercise habits (see section below)
- [x] Superuser can log in and view the list of other users
- [x] Superuser can view other user's activity data
- [x] Superuser can view defined activity types, add new activity types and modify existing ones (see below)
- [x] For each activity type, superuser can view defined subactivity types, add new subactivity types and modify existing ones (see below)

## Types of exercise supported and data recorded

The solution supports two types of exercise:

### 1. Exercise in one location (i.e. gym session, swim session, game of tennis etc)

For these, the following data is recorded:

- [x] Name of activity (e.g. gym / swim / tennis) chosen from predefined list of activities
- [x] Time and date of exercise
- [x] Total duration of exercise session
- Optional location of the exercise (link to position on map)
- [x] Optional description / narrative of the activity entered by the user
- [x] Optional link to the exercise in another tracking solution (e.g. Strava)
- [x] Optional list of subactivities performed and quantity for each. This can be used to track the types of gym exercises performed, or types of swim stroke used, or number of games played. 

### 2. Exercise over distance (e.g. a run, or a cycle ride)

For these, the following data is recorded:

- [x] Name of activity (e.g. run / walk / cycle) chosen from predefined list of activities
- [x] Time and date of exercise
- [x] Total duration of exercise session
- [x] Optional description / narrative of the activity entered by the user
- [x] Optional link to the exercise in another tracking solution (e.g. Strava)
- Optional route of the exercise (link to a route on map)
- Optional distance covered during exercise
- Optional maximum speed during exercise
- Optional average speed during exercise

## Statistics available

The users can view the following statistics about their exercise habits:

- [x] Total time & number of exercises
- [x] Total time & number of exercises per activity type
- Total number of exercises per subactivity type
- Total distance covered
- Average speed 
- Maximum speed
- [x] These statistics can be viewed over different time periods - e.g. last week, last month or last year. 
