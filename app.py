
from MySQLdb.cursors import Cursor
from flask import Flask, render_template, request, redirect, flash, url_for
from flask.wrappers import Response
from flask_mysqldb import MySQL


app = Flask(__name__)

app.jinja_env.filters['zip'] = zip
app.jinja_env.add_extension('jinja2.ext.loopcontrols')

app.config['MYSQL_HOST']= '127.0.0.1'
app.config['MYSQL_USER']= 'root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB'] = 'book_selling_system'

mysql = MySQL(app)
  #---------------------------------------------------MAIN PAGE----------------------------------------------
@app.route('/')                                      #index 
def index():
    title="SYSTEM"
    return render_template("index.html")    


#---------------------------------------------- Inserting Data ---------------------------------------------

@app.route('/insert')                                   #Option For inserting Data -------------------------
def insert():
    title="Insert Data"
    return render_template("insert.html")  




@app.route('/book', methods=['POST','GET'])                   #Book insertion
def book():
    if request.method=='POST':
        #print("hi this is me")
        info=request.form
        identity=int(info['IdInput'])
        name=info['NameInput']
        genre=info['GenreInput']
        isbn=int(info['ISBNInput'])
        pid=info['PIDInput'] #------------------------------------All Publishers list
        authors_input=request.form.getlist("AIDInput")    #------------------------------------All Authors list
        authors_input=[int(i) for i in authors_input]  
        #aid = info['AIDInput']   
        print(authors_input)
        sponsors_input=request.form.getlist("SIDInput")   #------------------------------------All Sponsors list
        sponsors_input=[int(i) for i in sponsors_input]  
        mycursor=mysql.connection.cursor()
        mycursor.execute("insert into book(ID,Name,Genre,ISBN,P_ID)values(%s,%s,%s,%s,%s)",(identity,name,genre,isbn,pid))
        mysql.connection.commit()
       
        for i in authors_input:
            print(i,identity)
            mycursor.execute("insert into author_book(A_ID,B_ID) values(%s, %s)", (i, identity))
            mysql.connection.commit()

        for j in sponsors_input:
            print(j,identity)
            mycursor.execute("insert into sponser_book(S_ID,B_ID) values(%s, %s)", (j, identity))
            mysql.connection.commit()
        mycursor.close()
        
        
        #title="Book "
    cur = mysql.connection.cursor()
    cur.execute('''SELECT Name, ID FROM publisher''')
    Users = cur.fetchall()
    cur.execute('''SELECT * FROM author''')
    authors = cur.fetchall()
    cur.execute('''SELECT * FROM sponser''')
    sponsors = cur.fetchall()

    p_id = list(map(lambda a: a[1], Users))
    p_name = list(map(lambda a: a[0], Users))

    a_id = list(map(lambda a: a[0], authors))
    a_name = list(map(lambda a: a[1], authors))
   
    s_id = list(map(lambda a: a[0], sponsors))
    s_name = list(map(lambda a: a[1], sponsors))
   
       
       # return render_template("index.html", title=title,info=info)
    
    title="Book "
    #return render_template("book.html", title=title, Publisher_ID = p_id, Publisher_Name = p_name, authors=authors )
    return render_template("book.html", title=title, Publisher_ID = p_id, Publisher_Name = p_name, a_id=a_id, a_name=a_name, s_id=s_id, s_name=s_name )

 


@app.route('/author', methods=['POST', 'GET'])                                  #Author insertion
def author():
    if request.method=='POST':
        info=request.form
        identity=int(info['IdInput'])
        name=info['NameInput']
        father=info['FatherNameInput']
        email=info['EmailInput']
        gender=info['GenderInput']
        mycursor=mysql.connection.cursor()
        mycursor.execute("insert into author(ID,Name,Father,Email,Gender)values(%s,%s,%s,%s,%s)",(identity,name,father,email,gender))
        mysql.connection.commit()
        mycursor.close()
        title="Author "
        return render_template("index.html", title=title,info=info)
    
    title="Author "
    return render_template("author.html", title=title)



@app.route('/buyer', methods=['POST', 'GET'])                                         #Buyer insertion
def buyer():
    if request.method=='POST':
        info=request.form
        identity=int(info['IdInput'])
        name=info['NameInput']
        city=info['CityInput']
        email=info['EmailInput']
        gender=info['GenderInput']
        publishers_input=request.form.getlist("PIDInput")    #------------------------------------All Publishers list
        publishers_input=[int(i) for i in publishers_input]  
        mycursor=mysql.connection.cursor()
        mycursor.execute("insert into buyer(ID,Name,City,Email,Gender)values(%s,%s,%s,%s,%s)",(identity,name,city,email,gender))

        for i in publishers_input:
            print(i,identity)
            mycursor.execute("insert into publisher_buyer(P_ID,B_ID) values(%s, %s)", (i, identity))
            mysql.connection.commit()

        mysql.connection.commit()
        mycursor.close()

    mycursor=mysql.connection.cursor()    
    mycursor.execute('''SELECT * FROM publisher''')
    publishers = mycursor.fetchall()    

    p_id = list(map(lambda a: a[0], publishers))
    p_name = list(map(lambda a: a[1], publishers))
   

        #title="Buyer "
    #return render_template("index.html", title=title,info=info)
    title="Buyer "
    return render_template("buyer.html", title=title, p_id=p_id, p_name=p_name)    




@app.route('/publisher', methods=['POST','GET'])                                #Publisher insertion
def publisher():
    if request.method=='POST':
        info=request.form
        identity=int(info['IdInput'])
        name=info['NameInput']
        city=info['CityInput']
        email=info['EmailInput']
        mycursor=mysql.connection.cursor()
        mycursor.execute("insert into publisher(ID,Name,City,Email)values(%s,%s,%s,%s)",(identity,name,city,email))
        mysql.connection.commit()
        mycursor.close()
        title="Publisher"
        return render_template("index.html", title=title,info=info)
    title="Publisher"    
    return render_template('publisher.html', title=title)




@app.route('/sponsors', methods=['POST','GET'])                                     #Sponsor insertion
def sponsors():
    if request.method=='POST':
        info=request.form
        identity=int(info['IdInput'])
        name=info['NameInput']
        city=info['CityInput']
        email=info['EmailInput']
        books_input=request.form.getlist("BIDInput")    #------------------------------------All Books list
        books_input=[int(i) for i in books_input]  
        mycursor=mysql.connection.cursor()
        mycursor.execute("insert into sponser(ID,Name,City,Email)values(%s,%s,%s,%s)",(identity,name,city,email))
        mysql.connection.commit()
        for i in books_input:
            print(i,identity)
            mycursor.execute("insert into sponser_book(S_ID,B_ID) values(%s, %s)", (identity, i))
            mysql.connection.commit()
 
        mycursor.close()
        #title="Sponsors"
        #return render_template("index.html", title=title,info=info)

    mycursor=mysql.connection.cursor()
    mycursor.execute('''SELECT * FROM book''')
    books = mycursor.fetchall()

    b_id = list(map(lambda a: a[0], books))
    b_name = list(map(lambda a: a[1], books))

    title="Sponsors"
    return render_template("sponsors.html", title=title, b_id=b_id, b_name=b_name)


#-------------------------------------------- Reading Data  ---------------------------------------------------------

@app.route('/read')                                        #Option For Reading Data 
def read():
    title="Read Data"
    return render_template("read.html")  


@app.route('/readbook')                                        #Reading Book Data 
def readbook():
    mycursor=mysql.connection.cursor()
    mycursor.execute("SELECT * FROM book")
    data=mycursor.fetchall()
    mycursor.close()
    title="Read Book Data"
    return render_template("readbook.html", data=data, title=title)  



@app.route('/readauthor')                                        #Reading Author Data 
def readauthor():
    mycursor=mysql.connection.cursor()
    mycursor.execute("SELECT * FROM author")
    data=mycursor.fetchall()
    mycursor.close()
    title="Read Author Data"
    return render_template("readauthor.html", data=data, title=title)  



@app.route('/readpublisher')                                        #Reading Publisher Data 
def readpublisher():
    mycursor=mysql.connection.cursor()
    mycursor.execute("SELECT * FROM publisher")
    data=mycursor.fetchall()
    mycursor.close()
    title="Reading Publisher  Data"
    return render_template("readpublisher.html", data=data, title=title)  


@app.route('/readbuyer')                                        #Reading Buyer Data 
def readbuyer():
    mycursor=mysql.connection.cursor()
    mycursor.execute("SELECT * FROM buyer")
    data=mycursor.fetchall()
    mycursor.close()
    title="Reading Buyer  Data"
    return render_template("readbuyer.html", data=data, title=title)  



@app.route('/readsponsor')                                        #Reading Sponsor Data 
def readsponsor():
    mycursor=mysql.connection.cursor()
    mycursor.execute("SELECT * FROM sponser")
    data=mycursor.fetchall()
    mycursor.close()
    title="Reading Sponsor  Data"
    return render_template("readsponsor.html", data=data, title=title)  



### Delete Records---------------------------------------------------


@app.route('/bookdelete/<int:no>')              #Book Record Delete
def bookdelete(no):
    mycursor=mysql.connection.cursor()

    mycursor.execute('''DELETE FROM BOOK WHERE book.ID=%s''', (no,))
    mysql.connection.commit()

    return redirect(url_for("readbook"))



@app.route('/authordelete/<int:no>')              #Author Record Delete
def authordelete(no):
    mycursor=mysql.connection.cursor()

    mycursor.execute('''DELETE FROM author WHERE author.ID=%s''', (no,))
    mysql.connection.commit()

    return redirect(url_for("readauthor"))    




@app.route('/publisherdelete/<int:no>')              #Publisher Record Delete
def publisherdelete(no):
    mycursor=mysql.connection.cursor()

    mycursor.execute('''DELETE FROM publisher WHERE publisher.ID=%s''', (no,))
    mysql.connection.commit()

    return redirect(url_for("readpublisher"))    
 


@app.route('/buyerdelete/<int:no>')              #Buyer Record Delete
def buyerdelete(no):
    mycursor=mysql.connection.cursor()

    mycursor.execute('''DELETE FROM buyer WHERE buyer.ID=%s''', (no,))
    mysql.connection.commit()

    return redirect(url_for("readbuyer"))    


@app.route('/sponsordelete/<int:no>')              #Sponsor Record Delete
def sponsordelete(no):
    mycursor=mysql.connection.cursor()

    mycursor.execute('''DELETE FROM sponser WHERE sponser.ID=%s''', (no,))
    mysql.connection.commit()

    return redirect(url_for("readsponsor"))    



#---------------------------------------------------UPDATIND DATA-------------------------------------------------



@app.route('/update_book/<int:no>', methods=['POST','GET'])       #--------------BOOK Update-------------------
def update_book(no):
    if request.method=="POST":
        info=request.form
        #identity=info["ID"]
        name=info["Name"]
        genre=info["Genre"]
        isbn=info["ISBN"]
        mycursor = mysql.connection.cursor()
        mycursor.execute("UPDATE book SET Name=%s, Genre=%s, ISBN=%s  WHERE ID=%s", (name,genre,isbn,no))
        mysql.connection.commit()
      
        mycursor.close()
        return redirect(url_for('readbook'))

    
    mycursor = mysql.connection.cursor()
    print(no)
    mycursor.execute('''SELECT * FROM book WHERE book.id=%s''',(no,)) 
    books=mycursor.fetchall()  
    
    b_id = list(map(lambda a: a[0], books))
    b_name = list(map(lambda a: a[1], books))
    b_genre = list(map(lambda a: a[2], books))
    b_isbn = list(map(lambda a: a[3], books))

    return render_template("update_book.html",  b_id=b_id, b_name=b_name, b_genre=b_genre, b_isbn=b_isbn )







@app.route('/update_author/<int:no>', methods=['POST','GET'])       #--------------AUTHOR Update-------------------
def update_author(no):
    if request.method=="POST":
        info=request.form
        #identity=info["ID"]
        name=info["Name"]
        father=info["Father"]
        gender=info["Gender"]
        mycursor = mysql.connection.cursor()
        mycursor.execute("UPDATE author SET Name=%s, Father=%s, Gender=%s  WHERE ID=%s", (name,father,gender,no))
        mysql.connection.commit()
      
        mycursor.close()
        return redirect(url_for('readauthor'))

    
    mycursor = mysql.connection.cursor()
    print(no)
    mycursor.execute('''SELECT * FROM author WHERE author.id=%s''',(no,)) 
    authors=mycursor.fetchall()  
    
    a_id = list(map(lambda a: a[0], authors))
    a_name = list(map(lambda a: a[1], authors))
    a_father = list(map(lambda a: a[2], authors))
    a_gender = list(map(lambda a: a[4], authors))

    return render_template("update_author.html",  a_id=a_id, a_name=a_name, a_father=a_father, a_gender=a_gender )





@app.route('/update_buyer/<int:no>', methods=['POST','GET'])       #--------------Buyer Update-------------------
def update_buyer(no):
    if request.method=="POST":
        info=request.form
        #identity=info["ID"]
        name=info["Name"]
        city=info["City"]
        gender=info["Gender"]
        mycursor = mysql.connection.cursor()
        mycursor.execute("UPDATE buyer SET Name=%s, City=%s, Gender=%s  WHERE ID=%s", (name,city,gender,no))
        mysql.connection.commit()
      
        mycursor.close()
        return redirect(url_for('readbuyer'))

    
    mycursor = mysql.connection.cursor()
    print(no)
    mycursor.execute('''SELECT * FROM buyer WHERE buyer.id=%s''',(no,)) 
    buyers=mycursor.fetchall()  
    
    b_id = list(map(lambda a: a[0], buyers))
    b_name = list(map(lambda a: a[1], buyers))
    b_city = list(map(lambda a: a[2], buyers))
    b_gender = list(map(lambda a: a[4], buyers))

    return render_template("update_buyer.html",  b_id=b_id, b_name=b_name, b_city=b_city, b_gender=b_gender )




@app.route('/update_sponsor/<int:no>', methods=['POST','GET'])       #--------------Sponsor Update-------------------
def update_sponsor(no):
    if request.method=="POST":
        info=request.form
        #identity=info["ID"]
        name=info["Name"]
        city=info["City"]
        mycursor = mysql.connection.cursor()
        mycursor.execute("UPDATE sponser SET Name=%s, City=%s  WHERE ID=%s", (name,city,no))
        mysql.connection.commit()
      
        mycursor.close()
        return redirect(url_for('readsponsor'))

    
    mycursor = mysql.connection.cursor()
    print(no)
    mycursor.execute('''SELECT * FROM sponser WHERE sponser.id=%s''',(no,)) 
    sponsers=mycursor.fetchall()  
    
    s_id = list(map(lambda a: a[0], sponsers))
    s_name = list(map(lambda a: a[1], sponsers))
    s_city = list(map(lambda a: a[2], sponsers))

    return render_template("update_sponsor.html",  s_id=s_id, s_name=s_name, s_city=s_city)








@app.route('/update_publisher/<int:no>', methods=['POST','GET'])       #--------------Publisher Update-------------------
def update_publisher(no):
    if request.method=="POST":
        info=request.form
        #identity=info["ID"]
        name=info["Name"]
        city=info["City"]
        #email=info["Email"]
        mycursor = mysql.connection.cursor()
        mycursor.execute("UPDATE publisher SET name=%s, city=%s WHERE ID=%s", (name,city,no))
        mysql.connection.commit()
        mycursor.close()
        return redirect(url_for('readpublisher'))

    
    mycursor = mysql.connection.cursor()
    print(no)
    mycursor.execute('''SELECT * FROM publisher WHERE publisher.id=%s''',(no,)) 
    publishers=mycursor.fetchall()  
    
    p_id = list(map(lambda a: a[0], publishers))
    p_name = list(map(lambda a: a[1], publishers))
    p_city = list(map(lambda a: a[2], publishers))
    return render_template("update_publisher.html",  p_id=p_id, p_name=p_name, p_city=p_city)
   
            


    