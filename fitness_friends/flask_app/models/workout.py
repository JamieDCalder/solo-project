from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

class Workout:
    DB = 'fitness_friends_schema'
    def __init__(self, data):
        self.id = data['id']
        self.date = data['date']
        self.weather = data['weather']
        self.hi_temp = data['hi_temp']
        self.low_temp = data['low_temp']
        self.workout_y_n = data['workout_y_n']
        self.intensity = data['intensity']
        self.sleep = data['sleep']
        self.diet = data['diet']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.athlete = None


    #CREATE SQL
    #need a save new workout
    @classmethod
    def save_workout(cls, data):
        query = """
        INSERT INTO workouts (date,weather,hi_temp,low_temp,workout_y_n,intensity,sleep,diet,user_id)
        VALUES (%(date)s, %(weather)s, %(hi_temp)s, %(low_temp)s, %(workout_y_n)s, %(intensity)s, %(sleep)s, %(diet)s, %(user_id)s)
        ;"""
        return connectToMySQL(cls.DB).query_db(query,data)
    
    #READ SQL
    #need a get all workouts will also have class assoc and get one

    @classmethod
    def get_all_workouts(cls):
        query = """
        SELECT * FROM workouts
        JOIN users ON workouts.user_id = users.id
        ;"""
        results = connectToMySQL(cls.DB).query_db(query)

        all_workouts=[]

        for row in results:
            one_workout = cls(row)

            user_data={
                'id' : row['users.id'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'email' : row['email'],
                'date_of_birth' : row['date_of_birth'],
                'zipcode' : row['zipcode'],
                'password' : row['password'],
                'created_at' : row['users.created_at'],
                'updated_at' : row['users.updated_at'],
            }
            one_workout.athlete = user.User(user_data)
            all_workouts.append(one_workout)
        
        return all_workouts
    

    @classmethod
    def get_one_workout(cls,data):
        query = """
        SELECT * FROM workouts
        JOIN users ON workouts.user_id = users.id
        WHERE workouts.id = %(id)s
        ;"""
        results = connectToMySQL(cls.DB).query_db(query,data)

        one_workout = cls(results[0])

        user_data={
                'id' : results[0]['users.id'],
                'first_name' : results[0]['first_name'],
                'last_name' : results[0]['last_name'],
                'email' : results[0]['email'],
                'date_of_birth' : results[0]['date_of_birth'],
                'zipcode' : results[0]['zipcode'],
                'password' : results[0]['password'],
                'created_at' : results[0]['users.created_at'],
                'updated_at' : results[0]['users.updated_at'],
            }
        one_workout.athlete = user.User(user_data)

        return one_workout
    

#UPDATE SQL
#will be updating and deleting workouts methods needed for both

    @classmethod
    def update_workout(cls,data):
        query="""
        UPDATE workouts
        SET date=%(date)s, weather=%(weather)s, hi_temp=%(hi_temp)s, low_temp=%(low_temp)s, workout_y_n=%(workout_y_n)s, intensity=%(intensity)s, sleep=%(sleep)s, diet=%(diet)s
        WHERE id=%(id)s
        ;"""
        return connectToMySQL(cls.DB).query_db(query,data)
    
#DELETE SQL
#will be updating and deleting workouts methods needed for both

    @classmethod
    def destroy_workout(cls,data):
        query="""
        DELETE FROM workouts
        WHERE id=%(id)s
        ;"""

        return connectToMySQL(cls.DB).query_db(query,data)
    

#STATIC
#need to validate new sighting creation

    @staticmethod
    def validate_workout(data):
        is_valid = True
        if len(data['date']) == 0:
            flash("Date must be provided.")
            is_valid = False
        if len(data['weather']) == 0:
            flash("Weather must be provided.")
            is_valid = False
        if len(data['hi_temp']) == 0:
            flash("Hi temp must be provided.")
            is_valid = False
        if len(data['low_temp']) == 0:
            flash("Low temp must be provided.")
            is_valid = False
        if len(data['workout_y_n']) == 0:
            flash("Note if you worked out.")
            is_valid = False
        if len(data['intensity']) == 0:
            flash("Intensity must be provided.")
            is_valid = False
        if len(data['sleep']) == 0:
            flash("Sleep must be provided.")
            is_valid = False
        if len(data['diet']) == 0:
            flash("Diet must be provided.")
            is_valid = False
        return is_valid