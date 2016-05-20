from system.core.model import Model
from datetime import date
from datetime import datetime
import email.utils as eu
import re

class Quote(Model):
    def __init__(self):
        super(Quote, self).__init__()


    def register_user(self, info):

        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        CHAR_REGEX = re.compile(r'^[a-zA-Z]')
        PASSWORD_REGEX = re.compile(r'^[a-zA-Z]')
        user_dob = info['dob']

        errors = []

        if len(info['full_name']) <2 :
            errors.append('Please enter your full name')
        elif len(info['alias']) < 2:
            errors.append('Please enter an alias')
        elif not info['email']: 
            errors.append('email cannot be blank')
        elif not EMAIL_REGEX.match(info['email']):
            errors.append('Please enter a valid email')
        elif self.db.query_db("SELECT * FROM users WHERE email = '" + info['email'] + "'") != []:
            errors.append('There is already a user in our system with that email')
        elif len(info['password']) < 8: 
            errors.append('Please make sure your password is 8 characters or more')
        elif info['password'] != info['confirm_password']:
            errors.append('Your passwords do not match')
        elif info['dob'] == '':
            errors.append('Please enter Date of Birth')
        if errors:
            return { 'status': False, 'errors': errors}

        else: 
            #insert data into database
            insert_query = "INSERT INTO users (name, alias, email, pass_hash, dob, created_at, updated_at) VALUES (:name, :alias, :email, :pass_hash, :dob, NOW(), NOW())"
            data_query = {
                'name': info['full_name'],
                'alias': info['alias'],
                'email': info['email'], 
                'pass_hash': self.bcrypt.generate_password_hash(info['password']),
                'dob': datetime.strptime(user_dob, '%m/%d/%Y')

            }
            self.db.query_db(insert_query, data_query)
            #get the new  user from db
            get_user_query = "SELECT * FROM users ORDER BY id DESC LIMIT 1"
            user = self.db.query_db(get_user_query)
            return { "status": True, "user": user[0] }


    def login_user(self, info):
        #query database to see if current user input matches 
        password = info['password']
        user_query = "SELECT * FROM users where email = :email"
        user_data = {
            'email': info['email']
        }

        current_user = self.db.query_db(user_query, user_data)

        if not current_user:
            errors.append('Sorry, looks like you do not have an account with us')
        else: 
            if not self.bcrypt.check_password_hash(current_user[0]['pass_hash'], password):
                errors.append('Your password do not match our records. Please try again')
                return { 'status': False, 'errors': errors}
            else:
                return { "status": True, "user": current_user[0] }


    def add_quote(self, info): 
        #insert quote into quotes
        quote_query = "INSERT INTO quotes (quote_author, quote, user_id, created_at, updated_at) VALUES (:quote_author, :quote, :user_id, NOW(), NOW())"
        quote_data = {
            'quote_author': info['quote_author'],
            'quote': info['quote'],
            'user_id': info['user_id']

        }
        self.db.query_db(quote_query, quote_data)
        return True

    def get_quotes(self):
        #select from all quotes
        return self.db.query_db("SELECT quotes.id, quotes.user_id, quotes.quote_author, quotes.quote, users.alias as alias FROM quotes JOIN users ON quotes.user_id = users.id  ")

    def get_fave_quotes(self, user_id):
        #select from all quotes
        get_quotes_query = "SELECT faves.quote_id, faves.user_id, quotes.id, quotes.user_id, quotes.quote_author, quotes.quote, users.alias as alias FROM users LEFT JOIN quotes ON users.id = quotes.user_id Join faves On faves.quote_id = quotes.id WHERE faves.user_id = :user_id"

        quotes_data = {
            'user_id' : user_id
        }
        print user_id
        return self.db.query_db(get_quotes_query, quotes_data)

    def get_other_quotes(self, user_id):
        #select from all quotes
        get_quotes_query = "SELECT  quotes.id, quotes.user_id, quotes.quote_author, quotes.quote, users.alias as alias FROM quotes LEFT JOIN users ON users.id = quotes.user_id Where not quotes.user_id in (SELECT quotes.id FROM quotes LEFT JOIN faves ON faves.quote_id = quotes.id  LEFT JOIN users ON faves.user_id = users. id WHERE faves.user_id = :user_id)"

        quotes_data = {
            'user_id' : user_id
        }
        
        return self.db.query_db(get_quotes_query, quotes_data)

    def get_current_user(self, user_id):
        #find current user
        current_user_quotes = "SELECT COUNT(quotes.user_id)as count, quotes.user_id, quotes.quote_author, quotes.quote, users.alias as alias FROM quotes JOIN users ON quotes.user_id = users.id WHERE user_id = :user_id"
        current_user_data = {
            'user_id' : user_id
        }
        
        return self.db.query_db(current_user_quotes, current_user_data)

    def get_user_quotes(self, user_id):
        get_user_quotes = "SELECT * FROM quotes where user_id= :user_id"
        get_user_data = {
            'user_id' : user_id
        }

        return self.db.query_db(get_user_quotes, get_user_data)

    def add_favorite(self, info):
        #insert quote into favorites
        fave_query = "INSERT INTO faves (quote_id, user_id, created_at, updated_at) VALUES (:quote_id, :user_id, NOW(), NOW())"
        fave_data = {
            'quote_id': info['fave_quote'],
            'user_id': info['user_id']
        }
        self.db.query_db(fave_query, fave_data)

    def remove_favorite(self, info):
        #delete entry 
        delete_query = "DELETE FROM faves WHERE quote_id = :quote_id && user_id = :user_id"
        delete_data = {
            'quote_id': info['fave_quote'],
            'user_id': info['user_id']
        }

        self.db.query_db(delete_query, delete_data)

    def get_favorites(self):
        #get favorites from db
        return True