from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms.uset_form import UserForm
from forms.group_form import GroupForm
from forms.user_group_form import UserGroupForm
import plotly
import json
from flask_sqlalchemy import SQLAlchemy
import plotly.graph_objs as go
from sqlalchemy.sql import func


app = Flask(__name__)
app.secret_key = 'key'

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1998@localhost/postgres'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://lajdaazigpumhb:2c22c122aace9c7e284a54a8b9c5fce77d7b3e25e63b7f6be7d0f2ef93ce1fb0@ec2-174-129-253-27.compute-1.amazonaws.com:5432/df88p4jfspv874'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), nullable=False)

    User_User_Group = db.relationship("Group", secondary='user_group')


class Group(db.Model):
    __tablename__ = 'group'

    group_id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(20), nullable=False)
    group_topic = db.Column(db.String(20), nullable=False)

    Group_User_Group = db.relationship("User", secondary='user_group')
    Group_Group_Post = db.relationship("Post", secondary='group_post')



class User_Group(db.Model):
    __tablename__ = 'user_group'

    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.group_id'), primary_key=True)


class Post(db.Model):
    __tablename__ = 'post'

    post_id = db.Column(db.Integer, primary_key=True)
    post_content = db.Column(db.String(1000), nullable=False)
    post_hashtag = db.Column(db.String(20), nullable=False)

    Post_Group_Post = db.relationship("Group", secondary='group_post')
    notification = db.relationship("Notification")




class Group_Post(db.Model):
    __tablename__ = 'group_post'

    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'), primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.group_id'), primary_key=True)


class Notification(db.Model):
    __tablename__ = 'notification'

    notification_id = db.Column(db.Integer, primary_key=True)
    notification_time = db.Column(db.String(5), primary_key=True)
    notification_text = db.Column(db.String(100), primary_key=True)

    post_id = db.Column(db.Integer, db.ForeignKey("post.post_id"))


'''
db.create_all()


db.session.query(Group_Post).delete()
db.session.query(User_Group).delete()
db.session.query(Group).delete()
db.session.query(Notification).delete()
db.session.query(Post).delete()
db.session.query(User).delete()
Dima = User(user_id= 1,
            user_name= "Dima")

Anna = User(user_id= 2,
            user_name= "Anna")


Vlad = User(user_id= 3,
            user_name= "Vlad")


Travel = Group(group_id= 1,
              group_name= "5 countris",
              group_topic= "Travel")

Nails = Group(group_id= 2,
              group_name= "Nails room",
              group_topic= "Nails")

Book = Group(group_id= 3,
              group_name= "I like to reed",
              group_topic= "Book")

Dima.User_User_Group.append(Travel)
Anna.User_User_Group.append(Nails)
Vlad.User_User_Group.append(Book)

New_tour = Post(post_id= 1,
              post_content= "New_tour",
              post_hashtag= "#tour")

New_nails = Post(post_id= 2,
              post_content= "New_nails",
              post_hashtag= "#nails")

Old_book = Post(post_id= 3,
              post_content= "Old_book",
              post_hashtag= "#book")


New_tour.Post_Group_Post.append(Travel)
New_nails.Post_Group_Post.append(Nails)
Old_book.Post_Group_Post.append(Book)



Like = Notification(notification_id= 1,
                    notification_text= "Like",
                    notification_time= "10:50")

Repost = Notification(notification_id= 2,
                    notification_text= "Repost",
                    notification_time= "10:50")

Comment = Notification(notification_id= 3,
                    notification_text= "Comment",
                    notification_time= "10:50")

New_nails.notification.append(Like)
New_tour.notification.append(Repost)
Old_book.notification.append(Comment)


db.session.add_all([Dima, Anna, Vlad, New_tour, New_nails, Old_book, Travel, Nails, Book, Like, Repost, Comment])
db.session.commit()
'''
@app.route('/', methods=['GET', 'POST'])
def root():
    return render_template('index.html')


@app.route('/user', methods=['GET'])
def user():

    result = db.session.query(User).all()

    return render_template('user.html', users = result)


@app.route('/new_user', methods=['GET','POST'])
def new_user():

    form = UserForm()


    if request.method == 'POST':
        if form.validate() != False:
            return render_template('user_form.html', form=form, form_name="New user", action="new_user")
        else:
            new_user = User(
                                user_id=form.user_id.data,
                                user_name=form.user_name.data,
                            )

            db.session.add(new_user)
            db.session.commit()


            return redirect(url_for('user'))

    return render_template('user_form.html', form=form, form_name="New user", action="new_user")



@app.route('/edit_user', methods=['GET','POST'])
def edit_user():

    form = UserForm()


    if request.method == 'GET':

        user_id =request.args.get('user_id')
        user = db.session.query(User).filter(User.user_id == user_id).one()

        # fill form and send to user
        form.user_id.data = user.user_id
        form.user_name.data = user.user_name

        return render_template('user_form.html', form=form, form_name="Edit user", action="edit_user")


    else:

        if form.validate() != False:
            return render_template('user_form.html', form=form, form_name="Edit user", action="edit_user")
        else:
            # find user
            user = db.session.query(User).filter(User.user_id == form.user_id.data).one()

            # update fields from form data
            user.user_id = form.user_id.data
            user.user_name = form.user_name.data

            db.session.commit()

            return redirect(url_for('user'))





@app.route('/delete_user', methods=['POST'])
def delete_user():

    user_id = request.form['user_id']

    result = db.session.query(User).filter(User.user_id == user_id).one()

    db.session.delete(result)
    db.session.commit()


    return user_id


@app.route('/group', methods=['GET'])
def group():

    result = db.session.query(Group).all()

    return render_template('group.html', groups = result)


@app.route('/new_group', methods=['GET','POST'])
def new_group():

    form = GroupForm()


    if request.method == 'POST':
        if form.validate() != False:
            return render_template('group_form.html', form=form, form_name="New group", action="new_group")
        else:
            new_group= Group(
                                group_id=form.group_id.data,
                                group_name=form.group_name.data,
                                group_topic=form.group_topic.data
                            )

            db.session.add(new_group)
            db.session.commit()


            return redirect(url_for('group'))

    return render_template('group_form.html', form=form, form_name="New group", action="new_group")



@app.route('/edit_group', methods=['GET','POST'])
def edit_group():

    form = GroupForm()


    if request.method == 'GET':

        group_id = request.args.get('group_id')
        group = db.session.query(Group).filter(Group.group_id == group_id).one()

        # fill form and send to user
        form.group_id.data = group.group_id
        form.group_name.data = group.group_name
        form.group_topic.data = group.group_topic

        return render_template('group_form.html', form=form, form_name="Edit group", action="edit_group")


    else:

        if form.validate() != False:
            return render_template('group_form.html', form=form, form_name="Edit group", action="edit_group")
        else:
            # find user
            group = db.session.query(Group).filter(Group.group_id == form.group_id.data).one()

            # update fields from form data
            group.group_id = form.group_id.data
            group.group_name = form.group_name.data
            group.group_topic = form.group_topic.data

            db.session.commit()

            return redirect(url_for('group'))





@app.route('/delete_group', methods=['POST'])
def delete_group():

    group_id = request.form['group_id']

    result = db.session.query(Group).filter(Group.group_id == group_id).one()

    db.session.delete(result)
    db.session.commit()


    return group_id

@app.route('/gpoupuser', methods=['GET'])
def gpoupuser():

    result = db.session.query(User_Group).all()

    return render_template('groupuser.html', gpoupusers = result)


@app.route('/new_gpoupuser', methods=['GET','POST'])
def new_gpoupuser():

    form = UserGroupForm()


    if request.method == 'POST':
        if form.validate() != False:
            return render_template('groupuser_form.html', form=form, form_name="New gpoupuser", action="new_gpoupuser")
        else:
            new_gpoupuser= User_Group(
                                user_id=form.user_id.data,
                                group_id=form.group_id.data,
                            )

            db.session.add(new_gpoupuser)
            db.session.commit()


            return redirect(url_for('gpoupuser'))

    return render_template('groupuser_form.html', form=form, form_name="New gpoupuser", action="new_gpoupuser")



@app.route('/delete_gpoupuser', methods=['POST'])
def delete_gpoupuser():

    user_id = request.form['user_id']
    group_id = request.form['group_id']


    result = db.session.query(User_Group).filter(User_Group.user_id == user_id).filter(User_Group.group_id == group_id).one()

    db.session.delete(result)
    db.session.commit()


    return str(result.user_id)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    print("")
    query1 = (
        db.session.query(
            User.user_name,
            func.count(User_Group.group_id).label('group_count')
        ).
            outerjoin(User_Group).
            group_by(User.user_name)
    ).all()

    query2 = (
        db.session.query(
            Group.group_name,
            func.count(Group_Post.post_id).label('hashtag_count')
        ).
            outerjoin(Group_Post).
            group_by(Group.group_name)
    ).all()

    name, group_count = zip(*query1)
    bar = go.Bar(
        x=name,
        y=group_count
    )

    name, hashtag_count = zip(*query2)
    pie = go.Pie(
        labels=name,
        values=hashtag_count
    )

    data = {
        "bar": [bar],
        "pie": [pie]
    }
    graphsJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('dashboard.html', graphsJSON=graphsJSON)
if __name__ == "__main__":

    app.run()




