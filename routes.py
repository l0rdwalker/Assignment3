# Importing the Flask Framework

from modules import *
from flask import *
import database
import configparser
from flask import request

# appsetup

page = {}
session = {}

# Initialise the FLASK application
app = Flask(__name__)
app.secret_key = 'SoMeSeCrEtKeYhErE'


# Debug = true if you want debug output on error ; change to false if you dont
app.debug = True


# Read my unikey to show me a personalised app
config = configparser.ConfigParser()
config.read('config.ini')
dbuser = config['DATABASE']['user']
portchoice = config['FLASK']['port']
if portchoice == '5xxx':
    print('ERROR: Please change config.ini as in the comments or Lab 08 instructions')
    exit(0)
session['isadmin'] = False

###########################################################################################
###########################################################################################
####                                 Database operative routes                         ####
###########################################################################################
###########################################################################################



#####################################################
##  INDEX
#####################################################

# What happens when we go to our website
@app.route('/')
def index():
    # If the user is not logged in, then make them go to the login page
    if( 'logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))
    page['username'] = dbuser
    page['title'] = 'Welcome'
    return render_template('welcome.html', session=session, page=page)

#####################################################
# User Login related                        
#####################################################
# login
@app.route('/login', methods=['POST', 'GET'])
def login():
    page = {'title' : 'Login', 'dbuser' : dbuser}
    # If it's a post method handle it nicely
    if(request.method == 'POST'):
        # Get our login value
        val = database.check_login(request.form['userid'], request.form['password'])
        print(val)
        print(request.form)
        # If our database connection gave back an error
        if(val == None):
            errortext = "Error with the database connection."
            errortext += "Please check your terminal and make sure you updated your INI files."
            flash(errortext)
            return redirect(url_for('login'))

        # If it's null, or nothing came up, flash a message saying error
        # And make them go back to the login screen
        if(val is None or len(val) < 1):
            flash('There was an error logging you in')
            return redirect(url_for('login'))
        # If it was successful, then we can log them in :)
        print(val[0])
        session['name'] = val[0]['firstname']
        session['userid'] = request.form['userid']
        session['logged_in'] = True
        session['isadmin'] = val[0]['isadmin']
        return redirect(url_for('index'))
    else:
        # Else, they're just looking at the page :)
        if('logged_in' in session and session['logged_in'] == True):
            return redirect(url_for('index'))
        return render_template('index.html', page=page)

# logout
@app.route('/logout')
def logout():
    session['logged_in'] = False
    flash('You have been logged out')
    return redirect(url_for('index'))



########################
#List All Items#
########################

@app.route('/users')
def list_users():
    '''
    List all rows in users by calling the relvant database calls and pushing to the appropriate template
    '''
    # connect to the database and call the relevant function
    users_listdict = database.list_users()

    # Handle the null condition
    if (users_listdict is None):
        # Create an empty list and show error message
        users_listdict = []
        flash('Error, there are no rows in users')
    page['title'] = 'List Contents of users'
    return render_template('list_users.html', page=page, session=session, users=users_listdict)
    

########################
#List Single Items#
########################


@app.route('/users/<userid>')
def list_single_users(userid):
    '''
    List all rows in users that match a particular id attribute userid by calling the 
    relevant database calls and pushing to the appropriate template
    '''

    # connect to the database and call the relevant function
    users_listdict = None
    users_listdict = database.list_users_equifilter("userid", userid)

    # Handle the null condition
    if (users_listdict is None or len(users_listdict) == 0):
        # Create an empty list and show error message
        users_listdict = []
        flash('Error, there are no rows in users that match the attribute "userid" for the value '+userid)
    page['title'] = 'List Single userid for users'
    return render_template('list_users.html', page=page, session=session, users=users_listdict)


########################
#List Search Items#
########################

@app.route('/consolidated/users')
def list_consolidated_users():
    '''
    List all rows in users join userroles 
    by calling the relvant database calls and pushing to the appropriate template
    '''
    # connect to the database and call the relevant function
    users_userroles_listdict = database.list_consolidated_users()

    # Handle the null condition
    if (users_userroles_listdict is None):
        # Create an empty list and show error message
        users_userroles_listdict = []
        flash('Error, there are no rows in users_userroles_listdict')
    page['title'] = 'List Contents of Users join Userroles'
    return render_template('list_consolidated_users.html', page=page, session=session, users=users_userroles_listdict)

@app.route('/user_stats')
def list_user_stats():
    '''
    List some user stats
    '''
    # connect to the database and call the relevant function
    user_stats = database.list_user_stats()

    # Handle the null condition
    if (user_stats is None):
        # Create an empty list and show error message
        user_stats = []
        flash('Error, there are no rows in user_stats')
    page['title'] = 'User Stats'
    return render_template('list_user_stats.html', page=page, session=session, users=user_stats)

@app.route('/users/search', methods=['POST', 'GET'])
def search_users_byname():
    '''
    List all rows in users that match a particular name
    by calling the relevant database calls and pushing to the appropriate template
    '''
    if(request.method == 'POST'):

        fnamesearch = database.search_users_customfilter("firstname","~",request.form['searchterm'])
        print(fnamesearch)
        lnamesearch = database.search_users_customfilter("lastname","~",request.form['searchterm'])
        print(lnamesearch)
        
        users_listdict = None

        if((fnamesearch == None) and (lnamesearch == None)):
            errortext = "Error with the database connection."
            errortext += "Please check your terminal and make sure you updated your INI files."
            flash(errortext)
            return redirect(url_for('index'))
        if(((fnamesearch == None) and (lnamesearch == None)) or ((len(fnamesearch) < 1) and len(lnamesearch) < 1)):
            flash(f"No items found for searchterm: {request.form['searchterm']}")
            return redirect(url_for('index'))
        else:
            
            users_listdict = fnamesearch
            users_listdict.extend(lnamesearch)
            # Handle the null condition'
            print(users_listdict)
            if (users_listdict is None or len(users_listdict) == 0):
                # Create an empty list and show error message
                users_listdict = []
                flash('Error, there are no rows in users that match the searchterm '+request.form['searchterm'])
            page['title'] = 'Search for a User by name'
            return render_template('list_users.html', page=page, session=session, users=users_listdict)
            

    else:
        return redirect(url_for('/users'))
        
@app.route('/users/delete/<userid>')
def delete_user(userid):
    '''
    List all rows in stations join stationtypes 
    by calling the relvant database calls and pushing to the appropriate template
    '''
    # connect to the database and call the relevant function
    resultval = database.delete_user(userid)
    
    # users_listdict = database.list_users()

    # # Handle the null condition
    # if (users_listdict is None):
    #     # Create an empty list and show error message
    #     users_listdict = []
    #     flash('Error, there are no rows in stations_stationtypes_listdict')
    page['title'] = f'List users after user {userid} has been deleted'
    return redirect(url_for('list_consolidated_users'))
    
@app.route('/users/update', methods=['POST','GET'])
def update_user():
    """
    Update details for a user
    """
    # # Check if the user is logged in, if not: back to login.
    if('logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))
    
    # Need a check for isAdmin

    page['title'] = 'Update user details'

    userslist = None
    print("request form is:")
    newdict = {}
    print(request.form)
    validupdate = False
    # Check your incoming parameters
    if(request.method == 'POST'):

        # verify that the values are available:
        if ('userid' not in request.form):
            # should be an exit condition
            flash("Can not update without a userid")
            return redirect(url_for('list_users'))
        else:
            newdict['userid'] = request.form['userid']
            print("We have a value: ",newdict['userid'])

        if ('firstname' not in request.form):
            newdict['firstname'] = None
        else:
            validupdate = True
            newdict['firstname'] = request.form['firstname']
            print("We have a value: ",newdict['firstname'])

        if ('lastname' not in request.form):
            newdict['lastname'] = None
        else:
            validupdate = True
            newdict['lastname'] = request.form['lastname']
            print("We have a value: ",newdict['lastname'])

        if ('userroleid' not in request.form):
            newdict['userroleid'] = None
        else:
            validupdate = True
            newdict['userroleid'] = request.form['userroleid']
            print("We have a value: ",newdict['userroleid'])

        if ('password' not in request.form):
            newdict['password'] = None
        else:
            validupdate = True
            newdict['password'] = request.form['password']
            print("We have a value: ",newdict['password'])

        print('Update dict is:')
        print(newdict, validupdate)

        if validupdate:
            #forward to the database to manage update
            userslist = database.update_single_user(newdict['userid'],newdict['firstname'],newdict['lastname'],newdict['userroleid'],newdict['password'])
        else:
            # no updates
            flash("No updated values for user with userid")
            return redirect(url_for('list_users'))
        # Should redirect to your newly updated user
        return list_single_users(newdict['userid'])
    else:
        return redirect(url_for('list_consolidated_users'))

######
## add items
######

    
@app.route('/users/add', methods=['POST','GET'])
def add_user():
    """
    Add a new User
    """
    # # Check if the user is logged in, if not: back to login.
    if('logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))
    
    # Need a check for isAdmin

    page['title'] = 'Add user details'

    userslist = None
    print("request form is:")
    newdict = {}
    print(request.form)

    # Check your incoming parameters
    if(request.method == 'POST'):

        # verify that the values are available:
        
        if ('firstname' not in request.form):
            newdict['firstname'] = 'Empty firstname'
        else:
            newdict['firstname'] = request.form['firstname']
            print("We have a value: ",newdict['firstname'])

        if ('lastname' not in request.form):
            newdict['lastname'] = 'Empty lastname'
        else:
            newdict['lastname'] = request.form['lastname']
            print("We have a value: ",newdict['lastname'])

        if ('userroleid' not in request.form):
            newdict['userroleid'] = 1 # default is traveler
        else:
            newdict['userroleid'] = request.form['userroleid']
            print("We have a value: ",newdict['userroleid'])

        if ('password' not in request.form):
            newdict['password'] = 'blank'
        else:
            newdict['password'] = request.form['password']
            print("We have a value: ",newdict['password'])

        print('Insert parametesrs are:')
        print(newdict)

        database.add_user_insert(newdict['firstname'],newdict['lastname'],newdict['userroleid'],newdict['password'])
        # Should redirect to your newly updated user
        print("did it go wrong here?")
        return redirect(url_for('list_consolidated_users'))
    else:
        # assuming GET request, need to setup for this
        return render_template('add_user.html',
                           session=session,
                           page=page,
                           userroles=database.list_userroles())


#########################################William Walker
@app.route('/cards/all', methods=['POST','GET'])
def all_cards():
    if (session['isadmin'] == True):
        if (session['isadmin'] == True):
            data = database.get_all_cards()
            page['title'] = 'List Contents of Users join Userroles'
            return render_template('all_cards.html', page=page, session=session, cards=data)
        else: 
            return render_template('404.html',page=page,session=session)

@app.route('/cards/delete/<cardID>', methods=['POST'])
def delete_card(cardID):
    if (session['isadmin'] == True):
        database.delete_card_byID(cardID)
        return all_cards()

@app.route('/cards/searchID/<cardID>', methods=['GET'])
def get_card_by_id(cardID):
    if (session['isadmin'] == True):
        card = database.get_card_byID(cardID)
        return card

@app.route('/cards/getAllIDs',methods=['GET'])
def get_all_users():
    if (session['isadmin'] == True):
        users = database.get_all_user_ids()
        return users

@app.route('/cards/getAllCardTypes',methods=['GET'])
def get_all_cardtypes():
    if (session['isadmin'] == True):
        cardTypes = database.get_all_card_types()
        return cardTypes

@app.route('/cards/updateCards',methods=['GET'])
def update_card():
    if (session['isadmin'] == True):
        cardID = request.args.get('cardID', default = 1, type = str)
        cardType = request.args.get('CardType', default = 1, type = str)
        assignedUser = request.args.get('Users', default = 1, type = int)
        cardExpiry = request.args.get('Expiry', default = 1, type = str)
        cardBalence = request.args.get('Balance', default = 1, type = int)
        
        status = database.update_card(cardID,cardType,assignedUser,cardExpiry,cardBalence)

        return status

@app.route('/cards/addNewCard',methods=['GET'])
def add_new_card():
    if (session['isadmin'] == True):
        cardType = request.args.get('CardType', default = 1, type = str)
        assignedUser = request.args.get('Users', default = 1, type = int)
        cardExpiry = request.args.get('Expiry', default = 1, type = str)
        cardBalence = request.args.get('Balance', default = 1, type = int)

        status = database.add_new_card(cardType,assignedUser,cardExpiry,cardBalence)

        return status

@app.route('/cards/getAllByDate',methods=['GET'])
def get_card_by_expire():
    if (session['isadmin'] == True):
        date = request.args.get('date',default='urg',type=str)
        return database.get_cards_with_expiry(date)

@app.route('/cards/cardExpire',methods=['POST','GET'])
def get_card_expire_page():
    if (session['isadmin'] == True):
        return render_template('date_list_cards.html', page=page, session=session)
    else:
        return render_template('404.html',page=page,session=session)

@app.route('/cards/getExpiryReport',methods=['GET'])
def generate_expiry_report():
    if (session['isadmin'] == True):
        return database.get_card_expiry_count()
    
@app.route('/cards/myCards',methods=['GET','POST'])
def get_my_cards_page():
    if (session['userid'] is not None):
        return render_template('myCards.html',page=page,session=session)
    else:
        return render_template('404.html',page=page,session=session)

@app.route('/cards/getMyCards',methods=['GET'])
def get_my_cards():
    return database.get_my_cards(session['userid'])

@app.route('/cards/user/addNew',methods=['GET'])
def add_new_card_user():
    cardType = request.args.get('CardType', default = 1, type = str)
    cardExpiry = request.args.get('Expiry', default = 1, type = str)
    cardBalence = request.args.get('Balance', default = 1, type = int)
    userId = session['userid']

    return database.add_new_card(cardType,userId,cardExpiry,cardBalence)