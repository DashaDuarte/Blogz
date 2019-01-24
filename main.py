from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
    
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:pass123@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
print("Welcome Back!")
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    post = db.Column(db.Text)

    def __init__(self, title, post):
        self.title = title
        self.post = post 


@app.route('/blog')
def show_blog():
    post_id = request.args.get('id')
    if (post_id):
        ind_post = Blog.query.get(post_id)
        return render_template('ind_post.html', ind_post=ind_post)
    else:
        all_blog_posts = Blog.query.all()
        return render_template('blog.html', posts=all_blog_posts)

def empty_val(x):
    if x:
        return True
    else:
        return False

@app.route('/blog_content', methods=['POST', 'GET'])
def article():
    post_id = request.args.get('id')
    my_blog = Blog.query.get(post_id)
    return render_template('blog_content' , blog = my_blog) 


@app.route('/newblog ', methods=['POST', 'GET'])
def add_entry():

    if request.method == 'POST':

        title_error = ""
        blog_entry_error = ""

        post_title = request.form['blog_title']
        post_entry = request.form['blog_post']
        post_new = Blog(post_title, post_entry)

        if empty_val(post_title) and empty_val(post_entry):
            db.session.add(post_new)
            db.session.commit()
            post_link = "/blog?id=" + str(post_new.id)
            return redirect(post_link)
        else:
            if not empty_val(post_title) and not empty_val(post_entry):
                title_error = "Enter blog title"
                blog_entry_error = "Enter blog entry"
                return render_template('new_blog.html', blog_entry_error=blog_entry_error, title_error=title_error)
            elif not empty_val(post_title):
                title_error = "Enter text for blog title"
                return render_template('new_blog.html', title_error=title_error, post_entry=post_entry)
            elif not empty_val(post_entry):
                blog_entry_error = "Enter text for blog entry"
                return render_template('new_blog.html', blog_entry_error=blog_entry_error, post_title=post_title)

    else:
        return render_template('new_blog.html')
        
if __name__ == '__main__':
    app.run()