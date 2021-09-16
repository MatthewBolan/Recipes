from config.mysqlconnection import connectToMySQL

from flask import flash



class Recipe:


    def __init__(self, data):

        self.id = data['id']

        self.name = data['name']

        self.description = data['description']

        self.instruction = data['instruction']

        self.under_30 = data['under_30']

        self.date_made = data['date_made']

        self.created_at = data['created_at']

        self.updated_at = data['updated_at']

        self.user_id = data['user_id']



    @classmethod

    def save_recipe(cls,data):

        query = "INSERT INTO recipes (name, description, instruction, date_made, under_30, user_id) VALUES (%(name)s, %(description)s, %(instruction)s, %(date_made)s, %(under_30)s, %(user_id)s);"

        results = connectToMySQL('recipes_users_schema').query_db(query,data)

        return results







    @classmethod

    def edit_recipe(cls,data):

        query = "UPDATE recipes SET name=%(name)s, description=%(description)s, instruction=%(instruction)s, under_30=%(under_30)s, date_made=%(date_made)s, updated_at=NOW() WHERE id = %(id)s;"

        return connectToMySQL('recipes_users_schema').query_db(query,data)





    @classmethod

    def get_one_recipe(cls,data):

        query = "SELECT * FROM recipes WHERE id = %(id)s"

        result = connectToMySQL('recipes_users_schema').query_db(query,data)

        return cls(result[0])





    @classmethod

    def delete_recipe(cls,data):

        query = "DELETE FROM recipes WHERE id = %(id)s;"

        return connectToMySQL('recipes_users_schema').query_db(query,data)












    

    @staticmethod

    def validate_recipe(recipe):
        
        valid = True

        if len (recipe['name']) < 3:

            flash ("Name Too Short!", "recipe")

            valid = False
        
        
        if len (recipe['description']) < 3:

            flash ("description Too Short!", "recipe")

            valid = False

        
        if len (recipe['instruction']) < 3:

            flash ("instruction Too Short!", "recipe")

            valid = False

        if recipe['date_made'] == "":

            flash ("Need To Select A Date!", "recipe")

            valid = False
        
        else:

            return valid







