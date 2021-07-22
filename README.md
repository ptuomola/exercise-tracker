# exercise-tracker

This solution supports your fitness regime and habits by allowing you to keep track of your exercise sessions - e.g. running routes/times, gym visits/sets, swim sessions/laps. It also provides helpful statistics of exercises to ensure you stay on track to improve your fitness. 

## Key features

- User can log in and out, and create new user account
- User can see a list of all exercise sessions they have recorded, and key statistics about each
- User can create a new exercise session and log information about it
- User can modify / correct / delete sessions entered incorrectly / by mistake
- User can delete their account and all information related to it
- User can view summary statistics about their exercise habits (see section below)
- Superuser can log in and view the list of other users
- Superuser can view other user's activity data
- Superuser can view defined activity types, add new activity types and modify existing ones (see below)
- For each activity type, superuser can view defined subactivity types, add new subactivity types and modify existing ones (see below)

## Types of exercise supported and data recorded

The solution supports two types of exercise:

### 1. Exercise in one location (i.e. gym session, swim session, game of tennis etc)

For these, the following data is recorded:

- Name of activity (e.g. gym / swim / tennis) chosen from predefined list of activities
- Time and date of exercise
- Total duration of exercise session
- Optional location of the exercise (link to position on map)
- Optional description / narrative of the activity entered by the user
- Optional link to the exercise in another tracking solution (e.g. Strava)
- Optional list of subactivities performed and quantity for each. This can be used to track the types of gym exercises performed, or types of swim stroke used, or number of games played. 

### 2. Exercise over distance (e.g. a run, or a cycle ride)

For these, the following data is recorded:

- Name of activity (e.g. run / walk / cycle) chosen from predefined list of activities
- Time and date of exercise
- Total duration of exercise session
- Optional description / narrative of the activity entered by the user
- Optional link to the exercise in another tracking solution (e.g. Strava)
- Optional route of the exercise (link to a route on map)
- Optional distance covered during exercise
- Optional maximum speed during exercise
- Optional average speed during exercise

## Statistics available

The users can view the following statistics about their exercise habits:

- Total time & number of exercises
- Total time & number of exercises per activity type
- Total number of exercises per subactivity type
- Total distance covered
- Average speed 
- Maximum speed

These statistics can be viewed over different time periods - e.g. per day, per week, per month or per year. 
