from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from .models import Post, Mom, Product, Expert, Comment
from . import db
import smtplib
from email.message import EmailMessage
import webbrowser

views = Blueprint("views", __name__)

#------------------------------------------------------------------------
# GENERAL
#------------------------------------------------------------------------
@views.route("/forum")
@views.route("/")
def forum():
    posts = Post.query.all()
    return render_template("forum.html", user=current_user, posts=posts)

@views.route("/resources")
def resources():
    return render_template("resources.html", user=current_user)

@views.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    return render_template("profile.html", user=current_user)


@views.route("/hand-me-down", methods=["GET", "POST"])
def hand_me_down():
    products = Product.query.all()
    return render_template("hand_me_down.html", products=products, user=current_user)


@views.route("/signup")
def signup():
    return render_template('mom_or_expert.html', user=current_user)


#------------------------------------------------------------------------
# FORUM PAGES
#------------------------------------------------------------------------

@views.route("/baby-health")
def baby_health():
    posts = Post.query.filter_by(category='Baby Health').all()
    return render_template("forum.html", user=current_user, posts=posts)

@views.route("/mom-health")
def mom_health():
    posts = Post.query.filter_by(category='Mom Health').all()
    return render_template("forum.html", user=current_user, posts=posts)

@views.route("/tips-and-tricks")
def tips_and_tricks():
    posts = Post.query.filter_by(category='Tips and Tricks').all()
    return render_template("forum.html", user=current_user, posts=posts)

@views.route("/support")
def support():
    posts = Post.query.filter_by(category='Support').all()
    return render_template("forum.html", user=current_user, posts=posts)

#------------------------------------------------------------------------
# POSTS
#------------------------------------------------------------------------
@views.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == "POST":
        post_title = request.form.get('title')
        post_content = request.form.get('content')
        category = request.form.get('category')

        if not post_content:
            flash('Post cannot be empty', category='error')
        else:
            post = Post(title=post_title, content=post_content, mauthor=current_user.id, category=category)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('views.forum'))

    return render_template('create_post.html', user=current_user)


@views.route("/delete-post/<post_id>")
@login_required
def delete_post(post_id):
    post = Post.query.filter_by(id=post_id).first()

    if not post:
        flash('Post does not exist.', category='error')
    elif current_user.id != post.mom.id:
        flash('You do not have permission to delete this post.', category='error')
    else:
        db.session.delete(post)
        db.session.commit()

    return redirect(url_for('views.forum'))

#------------------------------------------------------------------------
# COMMENTS
#------------------------------------------------------------------------
@views.route("/create-comment/<post_id>", methods=['POST'])
@login_required
def create_comment(post_id):
    text = request.form.get('comment')

    if not text:
        flash('Comment cannot be empty.', category='error')
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(
                text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Post does not exist.', category='error')

    return redirect(url_for('views.forum'))


@views.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash('Post does not exist.', category='error')
    elif current_user.id != comment.author:
        flash('You do not have permission to delete this comment.', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('views.forum'))

#------------------------------------------------------------------------
# PRODUCTS
#------------------------------------------------------------------------
@views.route("/list-product", methods=['GET', 'POST'])
@login_required
def list_product():
    if request.method == "POST":
        name = request.form.get('name')
        age = request.form.get('age')
        category = request.form.get('category')
        description = request.form.get('description')
        price = request.form.get('price')
        # DONT DO THIS AT HOME <3
        image = request.files['file'] 
        image.save(f"website/static/assets/{image.filename}")   

        if not name:
            flash('Please remember to add a name to your product <3', category='error')
        elif not price:
            flash('Please remember to add a price to your product, or 0.00!')
        elif not category:
            flash('Please remember to add a category to your product, or 0.00!')
        else:
            print("This ran")
            product = Product(name=name, age=age, description=description, mauthor=current_user.id, price=price, category=category, img=image.filename)
            print("This ran pt2")
            db.session.add(product)
            print("This ran pt3")
            db.session.commit()
            flash('Product created!', category='success')
            return redirect(url_for('views.hand_me_down'))

    return render_template('list_product.html', user=current_user)


@views.route("/delete-product/<product_id>")
@login_required
def delete_product(product_id):
    product = Product.query.filter_by(id=product_id).first()

    if not product:
        flash('Product does not exist.', category='error')
    elif current_user.id != product.mauthor:
        flash('You do not have permission to delete this post.', category='error')
    else:
        db.session.delete(product)
        db.session.commit()

    return redirect(url_for('views.hand_me_down'))


# EMAIL SENDING
#---------------------------
@views.route("/send-email/<email1>/<prod_name>", methods=['GET', 'POST'])
def send_email(email1, prod_name):
    if request.method == "POST":
        subject = f"Inquiring About: {prod_name}"
        gmail_url = f'https://mail.google.com/mail/?view=cm&fs=1&to={email1}&su={subject}'
        webbrowser.open(gmail_url)
        return redirect(url_for("views.hand_me_down"))

    return render_template("hand_me_down.html", user=current_user)