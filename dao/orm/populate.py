from dao.orm.model import *

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