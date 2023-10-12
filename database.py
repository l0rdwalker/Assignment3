#!/usr/bin/env python3
# Imports
from modules import pg8000
import configparser
import json
import sys
import re

#  Common Functions
##     database_connect()
##     dictfetchall(cursor,sqltext,params)
##     dictfetchone(cursor,sqltext,params)
##     print_sql_string(inputstring, params)


################################################################################
# Connect to the database
#   - This function reads the config file and tries to connect
#   - This is the main "connection" function used to set up our connection
################################################################################

def database_connect():
    # Read the config file
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Create a connection to the database
    connection = None

    # choose a connection target, you can use the default or
    # use a different set of credentials that are setup for localhost or winhost
    connectiontarget = 'DATABASE'
    # connectiontarget = 'DATABASELOCAL'
    try:
        '''
        This is doing a couple of things in the back
        what it is doing is:

        connect(database='y2?i2120_unikey',
            host='soit-db-pro-2.ucc.usyd.edu.au,
            password='password_from_config',
            user='y2?i2120_unikey')
        '''
        targetdb = ""
        if ('database' in config[connectiontarget]):
            targetdb = config[connectiontarget]['database']
        else:
            targetdb = config[connectiontarget]['user']

        connection = pg8000.connect(database=targetdb,
                                    user=config[connectiontarget]['user'],
                                    password=config[connectiontarget]['password'],
                                    host=config[connectiontarget]['host'],
                                    port=int(config[connectiontarget]['port']))
    except pg8000.OperationalError as e:
        print("""Error, you haven't updated your config.ini or you have a bad
        connection, please try again. (Update your files first, then check
        internet connection)
        """)
        print(e)
    except pg8000.ProgrammingError as e:
        print("""Error, config file incorrect: check your password and username""")
        print(e)
    except Exception as e:
        print(e)

    # Return the connection to use
    return connection

######################################
# Database Helper Functions
######################################
def dictfetchall(cursor,sqltext,params=None):
    """ Returns query results as list of dictionaries."""
    """ Useful for read queries that return 1 or more rows"""

    result = []
    
    cursor.execute(sqltext,params)
    if cursor.description is not None:
        cols = [a[0].decode("utf-8") for a in cursor.description]
        
        returnres = cursor.fetchall()
        if returnres is not None or len(returnres > 0):
            for row in returnres:
                result.append({a:b for a,b in zip(cols, row)})

        # cursor.close()
    print("returning result: ",result)
    return result

def dictfetchone(cursor,sqltext,params=None):
    """ Returns query results as list of dictionaries."""
    """ Useful for create, update and delete queries that only need to return one row"""

    # cursor = conn.cursor()
    result = []
    cursor.execute(sqltext,params)
    if (cursor.description is not None):
        print("cursor description", cursor.description)
        cols = [a[0].decode("utf-8") for a in cursor.description]
        returnres = cursor.fetchone()
        print("returnres: ", returnres)
        if (returnres is not None):
            result.append({a:b for a,b in zip(cols, returnres)})
    return result

##################################################
# Print a SQL string to see how it would insert  #
##################################################

def print_sql_string(inputstring, params=None):
    """
    Prints out a string as a SQL string parameterized assuming all strings
    """
    if params is not None:
        if params != []:
           inputstring = inputstring.replace("%s","'%s'")
    
    print(inputstring % params)

###############
# Login       #
###############

def check_login(username, password):
    '''
    Check Login given a username and password
    '''
    # Ask for the database connection, and get the cursor set up
    conn = database_connect()
    print("checking login")
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """SELECT *
                FROM opaltravel.Users
                    JOIN opaltravel.UserRoles ON
                        (opaltravel.Users.userroleid = opaltravel.UserRoles.userroleid)
                WHERE userid=%s AND password=%s"""
        print_sql_string(sql, (username, password))
        r = dictfetchone(cur, sql, (username, password)) # Fetch the first row
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Error Invalid Login")
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return None

def runQuiry(quiry):
    conn = database_connect()
    print("checking login")
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        sql = quiry
        r = cur.execute(sql)
        cur.close()                     
        conn.close()                    
        return r
    except Exception as e:
        print(Exception)
    cur.close()                     
    conn.close()                   
    return None
    
########################
#List All Items#
########################

# Get all the rows of users and return them as a dict
def list_users():
    # Get the database connection and set up the cursor
    conn = database_connect()
    if(conn is None):
        # If a connection cannot be established, send an Null object
        return None
    # Set up the rows as a dictionary
    cur = conn.cursor()
    returndict = None

    try:
        # Set-up our SQL query
        sql = """SELECT *
                    FROM opaltravel.users """
        
        # Retrieve all the information we need from the query
        returndict = dictfetchall(cur,sql)

        # report to the console what we recieved
        print(returndict)
    except:
        # If there are any errors, we print something nice and return a null value
        print("Error Fetching from Database", sys.exc_info()[0])

    # Close our connections to prevent saturation
    cur.close()
    conn.close()

    # return our struct
    return returndict
    

def list_userroles():
    # Get the database connection and set up the cursor
    conn = database_connect()
    if(conn is None):
        # If a connection cannot be established, send an Null object
        return None
    # Set up the rows as a dictionary
    cur = conn.cursor()
    returndict = None

    try:
        # Set-up our SQL query
        sql = """SELECT *
                    FROM opaltravel.userroles """
        
        # Retrieve all the information we need from the query
        returndict = dictfetchall(cur,sql)

        # report to the console what we recieved
        print(returndict)
    except:
        # If there are any errors, we print something nice and return a null value
        print("Error Fetching from Database", sys.exc_info()[0])

    # Close our connections to prevent saturation
    cur.close()
    conn.close()

    # return our struct
    return returndict
    

########################
#List Single Items#
########################

# Get all rows in users where a particular attribute matches a value
def list_users_equifilter(attributename, filterval):
    # Get the database connection and set up the cursor
    conn = database_connect()
    if(conn is None):
        # If a connection cannot be established, send an Null object
        return None
    # Set up the rows as a dictionary
    cur = conn.cursor()
    val = None

    try:
        # Retrieve all the information we need from the query
        sql = f"""SELECT *
                    FROM opaltravel.users
                    WHERE {attributename} = %s """
        val = dictfetchall(cur,sql,(filterval,))
    except:
        # If there are any errors, we print something nice and return a null value
        print("Error Fetching from Database: ", sys.exc_info()[0])

    # Close our connections to prevent saturation
    cur.close()
    conn.close()

    # return our struct
    return val
    


########################### 
#List Report Items #
###########################
    
# # A report with the details of Users, Userroles
def list_consolidated_users():
    # Get the database connection and set up the cursor
    conn = database_connect()
    if(conn is None):
        # If a connection cannot be established, send an Null object
        return None
    # Set up the rows as a dictionary
    cur = conn.cursor()
    returndict = None

    try:
        # Set-up our SQL query
        sql = """SELECT *
                FROM opaltravel.users 
                    JOIN opaltravel.userroles 
                    ON (opaltravel.users.userroleid = opaltravel.userroles.userroleid) ;"""
        
        # Retrieve all the information we need from the query
        returndict = dictfetchall(cur,sql)

        # report to the console what we recieved
        print(returndict)
    except:
        # If there are any errors, we print something nice and return a null value
        print("Error Fetching from Database", sys.exc_info()[0])

    # Close our connections to prevent saturation
    cur.close()
    conn.close()

    # return our struct
    return returndict

def list_user_stats():
    # Get the database connection and set up the cursor
    conn = database_connect()
    if(conn is None):
        # If a connection cannot be established, send an Null object
        return None
    # Set up the rows as a dictionary
    cur = conn.cursor()
    returndict = None

    try:
        # Set-up our SQL query
        sql = """SELECT userroleid, COUNT(*) as count
                FROM opaltravel.users 
                    GROUP BY userroleid
                    ORDER BY userroleid ASC ;"""
        
        # Retrieve all the information we need from the query
        returndict = dictfetchall(cur,sql)

        # report to the console what we recieved
        print(returndict)
    except:
        # If there are any errors, we print something nice and return a null value
        print("Error Fetching from Database", sys.exc_info()[0])

    # Close our connections to prevent saturation
    cur.close()
    conn.close()

    # return our struct
    return returndict
    

####################################
##  Search Items - inexact matches #
####################################

# Search for users with a custom filter
# filtertype can be: '=', '<', '>', '<>', '~', 'LIKE'
def search_users_customfilter(attributename, filtertype, filterval):
    # Get the database connection and set up the cursor
    conn = database_connect()
    if(conn is None):
        # If a connection cannot be established, send an Null object
        return None
    # Set up the rows as a dictionary
    cur = conn.cursor()
    val = None

    # arrange like filter
    filtervalprefix = ""
    filtervalsuffix = ""
    if str.lower(filtertype) == "like":
        filtervalprefix = "'%"
        filtervalsuffix = "%'"
        
    try:
        # Retrieve all the information we need from the query
        sql = f"""SELECT *
                    FROM opaltravel.users
                    WHERE lower({attributename}) {filtertype} {filtervalprefix}lower(%s){filtervalsuffix} """
        print_sql_string(sql, (filterval,))
        val = dictfetchall(cur,sql,(filterval,))
    except:
        # If there are any errors, we print something nice and return a null value
        print("Error Fetching from Database: ", sys.exc_info()[0])

    # Close our connections to prevent saturation
    cur.close()
    conn.close()

    # return our struct
    return val


#####################################
##  Update Single Items by PK       #
#####################################


# Update a single user
def update_single_user(userid, firstname, lastname,userroleid,password):
    # Get the database connection and set up the cursor
    conn = database_connect()
    if(conn is None):
        # If a connection cannot be established, send an Null object
        return None
    # Set up the rows as a dictionary
    cur = conn.cursor()
    val = None

    # Data validation checks are assumed to have been done in route processing

    try:
        setitems = ""
        attcounter = 0
        if firstname is not None:
            setitems += "firstname = %s\n"
            attcounter += 1
        if lastname is not None:
            if attcounter != 0:
                setitems += ","
            setitems += "lastname = %s\n"
            attcounter += 1
        if userroleid is not None:
            if attcounter != 0:
                setitems += ","
            setitems += "userroleid = %s::bigint\n"
            attcounter += 1
        if password is not None:
            if attcounter != 0:
                setitems += ","
            setitems += "password = %s\n"
            attcounter += 1
        # Retrieve all the information we need from the query
        sql = f"""UPDATE opaltravel.users
                    SET {setitems}
                    WHERE userid = {userid};"""
        print_sql_string(sql,(firstname, lastname,userroleid,password))
        val = dictfetchone(cur,sql,(firstname, lastname,userroleid,password))
        conn.commit()
        
    except:
        # If there are any errors, we print something nice and return a null value
        print("Error Fetching from Database: ", sys.exc_info()[0])
        print(sys.exc_info())

    # Close our connections to prevent saturation
    cur.close()
    conn.close()

    # return our struct
    return val


##  Insert / Add

def add_user_insert(firstname, lastname,userroleid,password):
    """
    Add a new User to the system
    """
    # Data validation checks are assumed to have been done in route processing

    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    sql = """
        INSERT into opaltravel.Users(firstname, lastname, userroleid, password)
        VALUES (%s,%s,%s,%s);
        """
    print_sql_string(sql, (firstname, lastname,userroleid,password))
    try:
        # Try executing the SQL and get from the database
        sql = """
        INSERT into opaltravel.Users(firstname, lastname, userroleid, password)
        VALUES (%s,%s,%s,%s);
        """

        cur.execute(sql,(firstname, lastname,userroleid,password))
        
        # r = cur.fetchone()
        r=[]
        conn.commit()                   # Commit the transaction
        print("return val is:")
        print(r)
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error adding a user:", sys.exc_info()[0])
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        raise

def delete_user(userid):
    """
    Remove a user from your system
    """
    # Data validation checks are assumed to have been done in route processing
    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = f"""
        DELETE
        FROM opaltravel.users
        WHERE userid = {userid};
        """

        cur.execute(sql,())
        conn.commit()                   # Commit the transaction
        r = []
        # r = cur.fetchone()
        # print("return val is:")
        # print(r)
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error deleting  user with id ",userid, sys.exc_info()[0])
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        raise

def sanitize_input(input_str):
    sanitized_str = re.sub(r'[;\'"\\]', '', str(input_str))
    return sanitized_str

def exercuteNonResponse(sql):
    conn = database_connect()
    if (conn is None):
        return None
    
    cur = conn.cursor()
    try:
        cur.execute(sql,())
        conn.commit()     

        cur.close()
        conn.close()
    except Exception as e:
        print(e)
        cur.close()
        conn.close()
        raise

def exercuteGetAllQuiry(sql):
    conn = database_connect()
    if (conn is None):
        return None
    
    cur = conn.cursor()
    try:
        returnDict = dictfetchall(cur,sql)

        cur.close()
        conn.close()

        return returnDict
    except Exception as e:
        print(e)
        cur.close()
        conn.close()
        raise

def exercuteGetSingleQuiry(sql):
    conn = database_connect()
    if (conn is None):
        return None
    
    cur = conn.cursor()
    try:
        returnDict = dictfetchone(cur,sql)
        returnDict = returnDict[0]

        cur.close()
        conn.close()

        for key in returnDict:
            returnDict[key] = str(returnDict[key])

        return returnDict
    except Exception as e:
        print(e)
        cur.close()
        conn.close()
        raise


def get_all_cards():
    sql = f"""
    SELECT oc.cardid,oc.expiry,oc.balance,ct.typename as cardtype,CONCAT(u.firstname, ' ', u.lastname) AS userFullname 
	FROM
	opaltravel.opalcards oc JOIN opaltravel.cardtypes ct 
		ON oc.cardtypeid = ct.cardtypeid
	JOIN opaltravel.users u 
		ON oc.userid = u.userid
    """
    return exercuteGetAllQuiry(sql)

def delete_card_byID(id):
    id = sanitize_input(id)
    sql = f"""
            DELETE
            FROM opaltravel.opalcards
            WHERE cardid = {id};
    """
    exercuteNonResponse(sql)

def get_card_byID(id):
    id = sanitize_input(id)
    sql = f"""SELECT * FROM opaltravel.opalcards WHERE cardid = {id};"""
    card_data = exercuteGetSingleQuiry(sql)

    if card_data is not None:
        response = json.dumps(card_data)
        return response 
    else:
        return json.dumps({'status':'failure'}) 
    
def get_all_user_ids():
    sql = "SELECT userid, CONCAT(firstname, ' ', lastname) AS fullname FROM opaltravel.users"
    users = exercuteGetAllQuiry(sql)

    if users is not None:
        return json.dumps(users)
    
def get_all_card_types():
    sql = "SELECT cardtypeid,typename FROM opaltravel.cardtypes"
    cardTypes = exercuteGetAllQuiry(sql)
    if cardTypes is not None:
        return json.dumps(cardTypes)
    
def update_card(cardID,cardType,assignedUser,cardExpiry,cardBalence):
    cardID = sanitize_input(cardID)
    cardType = sanitize_input(cardType)
    assignedUser = sanitize_input(assignedUser)
    cardExpiry = sanitize_input(cardExpiry)
    cardBalence = sanitize_input(cardBalence)

    sql = f"UPDATE opaltravel.opalcards SET cardtypeid='{cardType}', userid='{assignedUser}', expiry='{cardExpiry}', balance='{cardBalence}' WHERE cardid='{cardID}'"
    print(sql)

    preChange = get_card_byID(cardID)
    exercuteNonResponse(sql)
    afterChange = get_card_byID(cardID)

    if (preChange == afterChange):
        return json.dumps({'status':'fail'})
    else:
        return json.dumps({'status':'succeeded'})
    

def get_largest_id():
    sql = "SELECT cardid FROM opaltravel.opalcards ORDER BY cardid DESC"
    try:
        response = exercuteGetSingleQuiry(sql)

        return response['cardid']
    except:
        return 1

def add_new_card(cardType,assignedUser,cardExpiry,cardBalence):
    cardType = sanitize_input(cardType)
    assignedUser = sanitize_input(assignedUser)
    cardExpiry = sanitize_input(cardExpiry)
    cardBalence = sanitize_input(cardBalence)

    newID = int(get_largest_id()) + 1
    sql = f"INSERT INTO opaltravel.opalcards (cardid, cardtypeid, userid, expiry, balance) VALUES ({newID},'{cardType}','{assignedUser}','{cardExpiry}','{cardBalence}');"
    exercuteNonResponse(sql)

    return json.dumps({'status' : 'successful'})

def get_cards_with_expiry(date:str):
    sql = f"""SELECT * FROM (SELECT oc.cardid,oc.cardtypeid,oc.userid,oc.expiry,oc.balance,ct.typename,CONCAT(u.firstname, ' ', u.lastname) AS fullname 
	FROM
	opaltravel.opalcards oc JOIN opaltravel.cardtypes ct 
		ON oc.cardtypeid = ct.cardtypeid
	JOIN opaltravel.users u 
		ON oc.userid = u.userid) as sub
		WHERE sub.expiry = '{date}'"""
    data = exercuteGetAllQuiry(sql)

    emptyList = []
    for x in range(0,len(data)):
        temp = {}
        for key, value in data[x].items():
            temp[key] = str(data[x][key])
        emptyList.append(temp)

    return json.dumps(emptyList)

def get_card_expiry_count():
    sql = '''SELECT expiry,COUNT(expiry) as qty 
                FROM opaltravel.opalcards
                    GROUP BY expiry'''
    data  = exercuteGetAllQuiry(sql)
    emptyList = []
    for x in range(0,len(data)):
        temp = {}
        for key, value in data[x].items():
            temp[key] = str(data[x][key])
        emptyList.append(temp)

    return json.dumps(emptyList)

def get_my_cards(id):
    sql = f"""SELECT oc.cardid,oc.expiry,oc.balance,ct.typename as cardtype 
	FROM
	opaltravel.opalcards oc JOIN opaltravel.cardtypes ct 
		ON oc.cardtypeid = ct.cardtypeid
	JOIN opaltravel.users u 
		ON oc.userid = u.userid
	WHERE oc.userid = '{id}'"""

    data  = exercuteGetAllQuiry(sql)
    emptyList = []
    for x in range(0,len(data)):
        temp = {}
        for key, value in data[x].items():
            temp[key] = str(data[x][key])
        emptyList.append(temp)

    return json.dumps(emptyList)
