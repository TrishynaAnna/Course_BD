from app import db



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


