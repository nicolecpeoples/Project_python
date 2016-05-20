"""
    Sample Controller File

    A Controller should be in charge of responding to a request.
    Load models to interact with the database and load views to render them to the client.

    Create a controller using this template
"""
from system.core.controller import *

class Quotes(Controller):
    def __init__(self, action):
        super(Quotes, self).__init__(action)

        self.load_model('Quote')
        self.db = self._app.db


    def index(self):
        return self.load_view('index.html')

    def dashboard(self):
        user_id = session['id']
        print user_id
        all_quotes = self.models['Quote'].get_quotes()
        fave_quotes =self.models['Quote'].get_fave_quotes(user_id)
        other_quotes = self.models['Quote'].get_other_quotes(user_id)
        return self.load_view('/quotes/quotes.html', all_quotes=all_quotes, fave_quotes=fave_quotes,other_quotes=other_quotes)

    def register(self):
        new_user =self.models['Quote'].register_user(request.form)

        if new_user['status'] == True:
            session['id'] = new_user['user']['id']
            session['name'] = new_user['user']['alias']

            return redirect('/dashboard')
        else: 
            for message in new_user['errors']:
                flash(message, 'regis_errors')
            return self.load_view('index.html')

    def login(self):
        returning_user =self.models['Quote'].login_user(request.form)

        if returning_user['status'] == True:
            session['id'] = returning_user['user']['id']
            session['name'] = returning_user['user']['alias']
            print "I am the id of this user" + str(returning_user['user']['id'])
            return redirect('/dashboard')

        else: 
            for message in returning_user['errors']:
                flash(message, 'regis_errors')
            return self.load_view('index.html')

    def new_quote(self): 
        self.models['Quote'].add_quote(request.form)

        return redirect('/dashboard')

    def view_profile(self, user_id):

        show_current_user = self.models['Quote'].get_current_user(user_id)
        user_quotes = self.models['Quote'].get_user_quotes(user_id)

        return self.load_view('/quotes/profile.html', show_current_user=show_current_user, user_quotes= user_quotes)

    def add_fave(self):
        self.models['Quote'].add_favorite(request.form)
        return redirect('/dashboard')

    def delete_fave(self):
        self.models['Quote'].remove_favorite(request.form)
        return redirect('/dashboard')

    def logout(self):
        del session['id']
        del session['name']
        return self.load_view('index.html')
