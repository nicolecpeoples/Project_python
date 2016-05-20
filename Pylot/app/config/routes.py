
from system.core.router import routes

routes['default_controller'] = 'Quotes'

routes['/main'] = 'Quotes#index'
routes['/dashboard'] = 'Quotes#dashboard'
routes['/users/<user_id>'] = 'Quotes#view_profile'
routes['/logout'] = 'Quotes#logout'
routes['POST']['/users/register'] = 'Quotes#register'
routes['POST']['/users/login'] = 'Quotes#login'
routes['POST']['/add/quote'] = 'Quotes#new_quote'
routes['POST']['/add/fave'] = 'Quotes#add_fave'
routes['POST']['/remove/fave'] = 'Quotes#delete_fave'
"""
 

    routes['GET']['/users'] = 'users#index'
    routes['GET']['/users/new'] = 'users#new'
    routes['POST']['/users'] = 'users#create'
    routes['GET']['/users/<int:id>'] = 'users#show'
    routes['GET']['/users/<int:id>/edit' = 'users#edit'
    routes['PATCH']['/users/<int:id>'] = 'users#update'
    routes['DELETE']['/users/<int:id>'] = 'users#destroy'
"""
    