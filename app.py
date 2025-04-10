#---------------------------------------------------------------------------------------------------#
# Import necessary modules for Flask app, database, security, file handling, and PDF generation
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from flask import send_file
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import json
# Added for image uploads
from werkzeug.utils import secure_filename
import os

#---------------------------------------------------------------------------------------------------#
# Initialize Flask app and set a secret key for session management
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure MySQL database connection settings
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'  # Use 'root' for MAMP Free; leave empty if using MAMP Pro
app.config['MYSQL_DB'] = 'justintimedb_test'
app.config['MYSQL_PORT'] = 8889  # MAMP uses port 8889 for MySQL

# Set up folder for image uploads and ensure it exists
UPLOAD_FOLDER = 'static/images/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize MySQL with the app
mysql = MySQL(app)
#---------------------------------------------------------------------------------------------------#
# Route for user registration, handles both GET (form display) and POST (form submission)
# Coded by Rajshree
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Extract form data
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])  # Hash password for security
        role = request.form['role']

        # Insert new user into the database
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)", 
                    (name, email, password, role))
        mysql.connection.commit()
        cur.close()

        # Notify user and redirect to login page
        flash("Registration successful! Please login.", "success")
        return redirect(url_for('login'))

    # Render registration form for GET request
    return render_template('register.html')
#---------------------------------------------------------------------------------------------------#
# Route for stamper registration, restricted to logged-in users
# Coded by Shani
@app.route('/register_stamper', methods=['GET', 'POST'])
def register_stamper():
    if 'logged_in' not in session:  # Check if user is logged in
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Extract form data
        name = request.form['name']
        email = request.form['email']
        certification = request.form['certification']
        password = generate_password_hash(request.form['password'])  # Hash password

        # Insert new stamper into the database
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO stampers (name, email, certification, password) VALUES (%s, %s, %s, %s)", 
                    (name, email, certification, password))
        mysql.connection.commit()
        cur.close()

        # Notify user and redirect to user management page
        flash("Stamper registered successfully!", "success")
        return redirect(url_for('user_management'))

    # Render stamper registration form for GET request
    return render_template('register_stamper.html')
#---------------------------------------------------------------------------------------------------#
# Route for production operative registration, restricted to logged-in users
# Coded by nidhi
@app.route('/register_operative', methods=['GET', 'POST'])
def register_operative():
    if 'logged_in' not in session:  # Check if user is logged in
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Extract form data
        name = request.form['name']
        email = request.form['email']
        department = request.form['department']
        password = generate_password_hash(request.form['password'])  # Hash password

        # Insert new operative into the database
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO production_operatives (name, email, department, password) VALUES (%s, %s, %s, %s)", 
                    (name, email, department, password))
        mysql.connection.commit()
        cur.close()

        # Notify user and redirect to user management page
        flash("Production Operative registered successfully!", "success")
        return redirect(url_for('user_management'))

    # Render operative registration form for GET request
    return render_template('register_operative.html')
#---------------------------------------------------------------------------------------------------#
# Route for user login, handles both GET and POST requests
# Coded by Rajshree
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Extract login credentials
        email = request.form['email']
        password = request.form['password']

        # Query user from database
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s", [email])
        user = cur.fetchone()
        cur.close()

        # Verify user and password
        if user and check_password_hash(user[3], password):
            # Set session variables for logged-in user
            session['logged_in'] = True
            session['user_id'] = user[0]
            session['role'] = user[4]
            flash("Login successful!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid email or password.", "danger")

    # Render login page for GET request
    return render_template('login.html')
#---------------------------------------------------------------------------------------------------#
# Route for stamper login, handles both GET and POST requests
# Coded by Shani
@app.route('/stamper_login', methods=['GET', 'POST'])
def stamper_login():
    if request.method == 'POST':
        # Extract login credentials
        email = request.form['email']
        password = request.form['password']

        # Query stamper from database
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, name, email, certification, password FROM stampers WHERE email=%s", [email])
        stamper = cur.fetchone()
        cur.close()

        # Verify stamper and password
        if stamper and check_password_hash(stamper[4], password):
            # Set session variables for logged-in stamper
            session['logged_in'] = True
            session['user_id'] = stamper[0]
            session['role'] = 'stamper'
            flash("Login successful!", "success")
            return redirect(url_for('stamper_dashboard'))
        else:
            flash("Invalid email or password.", "danger")

    # Render stamper login page for GET request
    return render_template('stamper_login.html')
#---------------------------------------------------------------------------------------------------#
# Route for production operative login, handles both GET and POST requests
# Coded by Nidhi
@app.route('/operative_login', methods=['GET', 'POST'])
def operative_login():
    if request.method == 'POST':
        # Extract login credentials
        email = request.form['email']
        password = request.form['password']

        # Query operative from database
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, name, email, department, password FROM production_operatives WHERE email=%s", [email])
        operative = cur.fetchone()
        cur.close()

        # Verify operative and password
        if operative and check_password_hash(operative[4], password):
            # Set session variables for logged-in operative
            session['logged_in'] = True
            session['user_id'] = operative[0]
            session['role'] = 'production_operative'
            flash("Login successful!", "success")
            return redirect(url_for('production_dashboard'))
        else:
            flash("Invalid email or password.", "danger")

    # Render operative login page for GET request
    return render_template('operative_login.html')
#---------------------------------------------------------------------------------------------------#
# Route to log out a user and clear session data
# Coded by Rajshree
@app.route('/logout')
def logout():
    # Remove session variables
    session.pop('logged_in', None)
    session.pop('user_id', None)
    session.pop('role', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))
#---------------------------------------------------------------------------------------------------#
# Route for main dashboard, accessible only to specific roles
# Coded by Rajshree
@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:  # Check if user is logged in
        return redirect(url_for('login'))

    # Define allowed roles for this dashboard
    allowed_roles = ['admin', 'floor_manager', 'production_manager', 'marketing_manager']
    user_role = session.get('role')

    # Restrict access based on role
    if user_role not in allowed_roles:
        flash("Access Denied! You do not have permission to view this page.", "danger")
        return redirect(url_for(user_role + '_dashboard'))

    # Render dashboard with user role
    return render_template('main_dashboard.html', role=user_role)
#---------------------------------------------------------------------------------------------------#
# Route to manage users, stampers, and operatives (view all)
# Coded by Rajshree
@app.route('/user_management')
def user_management():
    if 'logged_in' not in session:  # Check if user is logged in
        return redirect(url_for('login'))

    # Fetch all users, stampers, and operatives from the database
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, name, email, role FROM users")
    users = cur.fetchall()
    cur.execute("SELECT id, name, email, certification FROM stampers")
    stampers = cur.fetchall()
    cur.execute("SELECT id, name, email, department FROM production_operatives")
    operatives = cur.fetchall()
    cur.close()

    # Render user management page with fetched data
    return render_template('user_management.html', users=users, stampers=stampers, operatives=operatives)
#---------------------------------------------------------------------------------------------------#
# Route to edit a user's details
# Coded by Harsh
@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if 'logged_in' not in session:  # Check if user is logged in
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()

    if request.method == 'POST':
        # Extract updated user data from form
        name = request.form['name']
        email = request.form['email']
        role = request.form['role']
        # Update user in the database
        cur.execute("UPDATE users SET name=%s, email=%s, role=%s WHERE id=%s", (name, email, role, user_id))
        mysql.connection.commit()
        cur.close()
        flash("User updated successfully!", "success")
        return redirect(url_for('user_management'))

    # Fetch user data for editing
    cur.execute("SELECT * FROM users WHERE id = %s", [user_id])
    user = cur.fetchone()
    cur.close()
    return render_template('edit_user.html', user=user)
#---------------------------------------------------------------------------------------------------#
# Route to delete a user
# Coded by Harsh
@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    if 'logged_in' not in session:  # Check if user is logged in
        return redirect(url_for('login'))

    # Delete user from the database
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", [user_id])
    mysql.connection.commit()
    cur.close()
    flash("User deleted successfully!", "danger")
    return redirect(url_for('user_management'))
#---------------------------------------------------------------------------------------------------#
# Route to display pending orders for approval
# Coded by Nidhi
@app.route('/approve_orders', methods=['GET'])
def approve_orders():
    if 'logged_in' not in session:  # Check if user is logged in
        return redirect(url_for('login'))

    # Fetch pending orders from the database
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, customer_name, email, product_name, quantity, status FROM orders WHERE status='Pending'")
    orders = cur.fetchall()
    cur.close()

    # Set static image URL for orders page
    image_url = url_for('static', filename='images/order-.webp')
    return render_template('approve_orders.html', orders=orders, image_url=image_url)
#---------------------------------------------------------------------------------------------------#
# Route to approve an order and update inventory
# Coded by Nidhi
@app.route('/approve_order/<int:order_id>', methods=['POST'])
def approve_order(order_id):
    if 'logged_in' not in session:  # Check if user is logged in
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    # Fetch order details
    cur.execute("SELECT product_name, quantity FROM orders WHERE id=%s", [order_id])
    order = cur.fetchone()

    if not order:
        flash("Order not found!", "danger")
        return redirect(url_for('approve_orders'))

    product_name, order_quantity = order
    # Check inventory for the product
    cur.execute("SELECT id, quantity FROM inventory WHERE item_name = %s AND category='Finished Product'", [product_name])
    inventory_item = cur.fetchone()

    if not inventory_item:
        flash("Product not found in inventory!", "danger")
        return redirect(url_for('approve_orders'))

    inventory_id, stock_quantity = inventory_item

    # Update inventory and order status if enough stock is available
    if stock_quantity >= order_quantity:
        new_stock = stock_quantity - order_quantity
        cur.execute("UPDATE inventory SET quantity = %s WHERE id = %s", (new_stock, inventory_id))
        new_status = "In Stock" if new_stock > 20 else "Low Stock" if new_stock > 5 else "Out of Stock"
        cur.execute("UPDATE inventory SET status = %s WHERE id = %s", (new_status, inventory_id))
        cur.execute("UPDATE orders SET status = 'Approved' WHERE id=%s", [order_id])
        mysql.connection.commit()
        flash("Order approved, and inventory stock updated!", "success")
    else:
        flash("Not enough stock to approve this order!", "danger")

    cur.close()
    return redirect(url_for('approve_orders'))
#---------------------------------------------------------------------------------------------------#
# Route to reject an order
# Coded by Nidhi
@app.route('/reject_order/<int:order_id>', methods=['POST'])
def reject_order(order_id):
    if 'logged_in' not in session:  # Check if user is logged in
        flash("Please log in to perform this action.", "danger")
        return redirect(url_for('login'))

    # Restrict access to specific roles
    if session.get('role') not in ['admin', 'floor_manager', 'production_manager']:
        flash("You do not have permission to reject orders.", "danger")
        return redirect(url_for('approve_orders'))

    try:
        cur = mysql.connection.cursor()
        # Verify order exists and is pending
        cur.execute("SELECT status FROM orders WHERE id=%s", [order_id])
        order = cur.fetchone()
        
        if not order:
            flash("Order not found!", "danger")
            cur.close()
            return redirect(url_for('approve_orders'))

        if order[0] != 'Pending':
            flash("Only pending orders can be rejected!", "danger")
            cur.close()
            return redirect(url_for('approve_orders'))

        # Update order status to rejected
        cur.execute("UPDATE orders SET status='Rejected' WHERE id=%s", [order_id])
        mysql.connection.commit()
        flash("Order rejected successfully!", "danger")
    except Exception as e:
        mysql.connection.rollback()
        flash(f"Error rejecting order: {str(e)}", "danger")
    finally:
        cur.close()

    return redirect(url_for('approve_orders'))
#---------------------------------------------------------------------------------------------------#
# Route to assign tasks to approved orders
# Coded by Rajshree
@app.route('/assign_tasks', methods=['GET'])
def assign_tasks():
    if 'logged_in' not in session:  # Check if user is logged in
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    # Fetch approved orders without assigned tasks
    cur.execute("""
        SELECT o.id, o.customer_name, o.product_name, o.quantity 
        FROM orders o 
        LEFT JOIN assigned_tasks a ON o.id = a.order_id 
        WHERE o.status='Approved' AND a.order_id IS NULL
    """)
    approved_orders = cur.fetchall()
    # Fetch stampers, operatives, and machines for task assignment
    cur.execute("SELECT id, name FROM stampers")
    stampers = cur.fetchall()
    cur.execute("SELECT id, name FROM production_operatives")
    operatives = cur.fetchall()
    cur.execute("SELECT id, name FROM machines")
    machines = cur.fetchall()
    cur.close()

    # Render task assignment page with fetched data
    return render_template('assign_tasks.html', approved_orders=approved_orders, stampers=stampers, operatives=operatives, machines=machines)
#---------------------------------------------------------------------------------------------------#
# Route to handle task assignment submission
# Coded by Rajshree
@app.route('/assign_task', methods=['POST'])
def assign_task():
    if 'logged_in' not in session:  # Check if user is logged in
        return redirect(url_for('login'))

    # Extract task assignment details from form
    order_id = request.form['order_id']
    product_name = request.form['product_name']
    quantity = request.form['quantity']
    stamper_id = request.form['stamper_id']
    operative_id = request.form['operative_id']
    machine_id = request.form['machine_id']

    # Insert task into the database
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO assigned_tasks (order_id, product_name, quantity, stamper_id, operative_id, machine_id) 
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (order_id, product_name, quantity, stamper_id, operative_id, machine_id))
    mysql.connection.commit()
    cur.close()
    flash("Task assigned successfully!", "success")
    return redirect(url_for('assign_tasks'))
#---------------------------------------------------------------------------------------------------#
# Route for stamper dashboard, showing assigned tasks
# Coded by Shani
@app.route('/stamper_dashboard')
def stamper_dashboard():
    if 'logged_in' not in session or session.get('role') != 'stamper':  # Restrict to stampers
        return redirect(url_for('stamper_login'))

    # Fetch incomplete tasks for the logged-in stamper
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT id, order_id, product_name, quantity, machine_id, stamper_status, operative_status 
        FROM assigned_tasks WHERE stamper_id = %s AND status != 'Completed'
    """, [session['user_id']])
    task_tuples = cur.fetchall()
    cur.close()

    # Convert tuple results to dictionaries for easier template use
    column_names = ['id', 'order_id', 'product_name', 'quantity', 'machine_id', 'stamper_status', 'operative_status']
    tasks = [dict(zip(column_names, task)) for task in task_tuples]
    return render_template('stamper_dashboard.html', tasks=tasks)
#---------------------------------------------------------------------------------------------------#
# Route to edit a stamper's details
# Coded by Shani
@app.route('/edit_stamper/<int:stamper_id>', methods=['GET', 'POST'])
def edit_stamper(stamper_id):
    if 'logged_in' not in session:  # Check if user is logged in
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()

    if request.method == 'POST':
        # Extract updated stamper data from form
        name = request.form['name']
        email = request.form['email']
        certification = request.form['certification']
        # Update stamper in the database
        cur.execute("UPDATE stampers SET name=%s, email=%s, certification=%s WHERE id=%s", 
                    (name, email, certification, stamper_id))
        mysql.connection.commit()
        cur.close()
        flash("Stamper details updated successfully!", "success")
        return redirect(url_for('user_management'))

    # Fetch stamper data for editing
    cur.execute("SELECT * FROM stampers WHERE id = %s", [stamper_id])
    stamper = cur.fetchone()
    cur.close()
    return render_template('edit_stamper.html', stamper=stamper)
#---------------------------------------------------------------------------------------------------#
# Route to delete a stamper
# Coded by Shani
@app.route('/delete_stamper/<int:stamper_id>', methods=['POST'])
def delete_stamper(stamper_id):
    if 'logged_in' not in session:  # Check if user is logged in
        return redirect(url_for('login'))

    # Delete stamper from the database
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM stampers WHERE id = %s", [stamper_id])
    mysql.connection.commit()
    cur.close()
    flash("Stamper deleted successfully!", "danger")
    return redirect(url_for('user_management'))
#---------------------------------------------------------------------------------------------------#
# Route to update task status by stamper or operative
# Coded by Rajshree
@app.route('/update_task_status/<int:task_id>', methods=['POST'])
def update_task_status(task_id):
    if 'logged_in' not in session:  # Check if user is logged in
        return redirect(url_for('login'))

    new_status = request.form['status']
    cur = mysql.connection.cursor()

    user_role = session.get('role')
    # Update status based on user role
    if user_role == 'stamper':
        cur.execute("UPDATE assigned_tasks SET stamper_status = %s WHERE id = %s", (new_status, task_id))
    elif user_role == 'production_operative':
        cur.execute("UPDATE assigned_tasks SET operative_status = %s WHERE id = %s", (new_status, task_id))
    
    mysql.connection.commit()

    # Check if task is fully completed
    cur.execute("SELECT order_id, stamper_status, operative_status FROM assigned_tasks WHERE id = %s", [task_id])
    task = cur.fetchone()

    if task and task[1] == 'Completed' and task[2] == 'Completed':
        order_id = task[0]
        cur.execute("UPDATE orders SET status = 'Completed' WHERE id = %s", [order_id])
        cur.execute("UPDATE assigned_tasks SET status = 'Completed' WHERE id = %s", [task_id])
        mysql.connection.commit()
        flash("Order marked as Completed!", "success")

    cur.close()
    # Redirect based on user role
    if user_role == 'stamper':
        return redirect(url_for('stamper_dashboard'))
    elif user_role == 'production_operative':
        return redirect(url_for('production_dashboard'))
#---------------------------------------------------------------------------------------------------#
# Route for production operative dashboard, showing assigned tasks
# Coded by Shani
@app.route('/production_dashboard')
def production_dashboard():
    if 'logged_in' not in session or session.get('role') != 'production_operative':  # Restrict to operatives
        return redirect(url_for('operative_login'))

    # Fetch incomplete tasks for the logged-in operative
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT id, order_id, product_name, quantity, machine_id, stamper_status, operative_status 
        FROM assigned_tasks WHERE operative_id = %s AND status != 'Completed'
    """, [session['user_id']])
    task_tuples = cur.fetchall()
    cur.close()

    # Convert tuple results to dictionaries
    column_names = ['id', 'order_id', 'product_name', 'quantity', 'machine_id', 'stamper_status', 'operative_status']
    tasks = [dict(zip(column_names, task)) for task in task_tuples]
    return render_template('production_dashboard.html', tasks=tasks)
#---------------------------------------------------------------------------------------------------#
# Route to edit an operative's details
# Coded by Shani
@app.route('/edit_operative/<int:operative_id>', methods=['GET', 'POST'])
def edit_operative(operative_id):
    if 'logged_in' not in session:  # Check if user is logged in
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()

    if request.method == 'POST':
        # Extract updated operative data from form
        name = request.form['name']
        email = request.form['email']
        department = request.form['department']
        # Update operative in the database
        cur.execute("UPDATE production_operatives SET name=%s, email=%s, department=%s WHERE id=%s", 
                    (name, email, department, operative_id))
        mysql.connection.commit()
        cur.close()
        flash("Production Operative details updated successfully!", "success")
        return redirect(url_for('user_management'))

    # Fetch operative data for editing
    cur.execute("SELECT * FROM production_operatives WHERE id = %s", [operative_id])
    operative = cur.fetchone()
    cur.close()
    return render_template('edit_operative.html', operative=operative)
#---------------------------------------------------------------------------------------------------#
# Route to delete an operative
# Coded by Shani
@app.route('/delete_operative/<int:operative_id>', methods=['POST'])
def delete_operative(operative_id):
    if 'logged_in' not in session:  # Check if user is logged in
        return redirect(url_for('login'))

    # Delete operative from the database
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM production_operatives WHERE id = %s", [operative_id])
    mysql.connection.commit()
    cur.close()
    flash("Production Operative deleted successfully!", "danger")
    return redirect(url_for('user_management'))
#---------------------------------------------------------------------------------------------------#
# Route to monitor machine status
# Coded by Harsh
@app.route('/machine_monitoring', methods=['GET', 'POST'])
def machine_monitoring():
    if 'logged_in' not in session:  # Check if user is logged in
        return redirect(url_for('login'))

    # Fetch all machines from the database
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, name, description, status FROM machines")
    machines = cur.fetchall()
    cur.close()
    return render_template('machine_monitoring.html', machines=machines)
#---------------------------------------------------------------------------------------------------#
# Route to update machine status
# Coded by Harsh
@app.route('/update_machine_status/<int:machine_id>', methods=['POST'])
def update_machine_status(machine_id):
    if 'logged_in' not in session:  # Check if user is logged in
        return redirect(url_for('login'))

    # Update machine status in the database
    new_status = request.form['status']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE machines SET status = %s WHERE id = %s", (new_status, machine_id))
    mysql.connection.commit()
    cur.close()
    flash("Machine status updated successfully!", "success")
    return redirect(url_for('machine_monitoring'))
#---------------------------------------------------------------------------------------------------#
# Route to manage inventory
# Coded by Harsh
@app.route('/inventory_management', methods=['GET', 'POST'])
def inventory_management():
    if 'logged_in' not in session:  # Check if user is logged in
        return redirect(url_for('login'))

    # Fetch all inventory items from the database
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, item_name, category, quantity, status FROM inventory")
    inventory_items = cur.fetchall()
    cur.close()
    return render_template('inventory_management.html', inventory_items=inventory_items)
#---------------------------------------------------------------------------------------------------#
# Route to request inventory restock
# Coded by Harsh
@app.route('/restock_inventory/<int:item_id>', methods=['POST'])
def restock_inventory(item_id):
    if 'logged_in' not in session:  # Check if user is logged in
        return redirect(url_for('login'))

    requested_quantity = int(request.form['quantity'])
    cur = mysql.connection.cursor()
    # Fetch item name for restock request
    cur.execute("SELECT item_name FROM inventory WHERE id = %s", [item_id])
    item = cur.fetchone()

    if item:
        item_name = item[0]
        # Insert restock request into inventory_orders table
        cur.execute("INSERT INTO inventory_orders (item_name, quantity_requested) VALUES (%s, %s)", 
                    (item_name, requested_quantity))
        mysql.connection.commit()
        flash("Restock request submitted for approval!", "success")
    
    cur.close()
    return redirect(url_for('inventory_management'))
#---------------------------------------------------------------------------------------------------#
# Route to view and manage inventory restock orders
# Coded by Harsh
@app.route('/inventory_orders', methods=['GET', 'POST'])
def inventory_orders():
    if 'logged_in' not in session:  # Check if user is logged in
        return redirect(url_for('login'))

    # Fetch pending and processed inventory orders
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, item_name, quantity_requested, status FROM inventory_orders WHERE status = 'Pending'")
    pending_orders = cur.fetchall()
    cur.execute("SELECT id, item_name, quantity_requested, status FROM inventory_orders WHERE status IN ('Approved', 'Rejected')")
    processed_orders = cur.fetchall()
    cur.close()
    return render_template('inventory_orders.html', pending_orders=pending_orders, processed_orders=processed_orders)
#---------------------------------------------------------------------------------------------------#
# Route to approve an inventory restock request
# Coded by Harsh
@app.route('/approve_restock/<int:order_id>', methods=['POST'])
def approve_restock(order_id):
    if 'logged_in' not in session:  # Check if user is logged in
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    # Fetch restock order details
    cur.execute("SELECT item_name, quantity_requested FROM inventory_orders WHERE id=%s", [order_id])
    order = cur.fetchone()

    if order:
        item_name, requested_quantity = order
        # Update inventory quantity and status
        cur.execute("UPDATE inventory SET quantity = quantity + %s WHERE item_name = %s", 
                    (requested_quantity, item_name))
        cur.execute("UPDATE inventory SET status = 'In Stock' WHERE item_name = %s", [item_name])
        cur.execute("UPDATE inventory_orders SET status='Approved' WHERE id=%s", [order_id])
        mysql.connection.commit()
    
    cur.close()
    flash("Restock approved & inventory updated!", "success")
    return redirect(url_for('inventory_orders'))
#---------------------------------------------------------------------------------------------------#
# Route to reject an inventory restock request
# Coded by Shani
@app.route('/reject_restock/<int:order_id>', methods=['POST'])
def reject_restock(order_id):
    if 'logged_in' not in session:  # Check if user is logged in
        return redirect(url_for('login'))

    # Update restock order status to rejected
    cur = mysql.connection.cursor()
    cur.execute("UPDATE inventory_orders SET status='Rejected' WHERE id=%s", [order_id])
    mysql.connection.commit()
    cur.close()
    flash("Restock request rejected!", "danger")
    return redirect(url_for('inventory_orders'))
#---------------------------------------------------------------------------------------------------#
# Route to view machine information
# Coded by Nidhi
@app.route('/machine_info')
def machine_info():
    if 'logged_in' not in session:  # Check if user is logged in
        return redirect(url_for('login'))

    # Fetch machine details from the database
    cur = mysql.connection.cursor()
    cur.execute("SELECT name, image_url, description, certifications_required, working_hours FROM machine_info")
    machines = cur.fetchall()
    cur.close()
    return render_template('machine_info.html', machines=machines)
#---------------------------------------------------------------------------------------------------#
# Route to list products
# Coded by Rajshree
@app.route('/product_listing', methods=['GET', 'POST'])
def product_listing():
    if 'logged_in' not in session:  # Check if user is logged in
        return redirect(url_for('login'))

    # Fetch all products from the database
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, product_name, description, price, stock_quantity, status FROM products")
    products = cur.fetchall()
    cur.close()
    return render_template('product_listing.html', products=products)
#---------------------------------------------------------------------------------------------------#
# Route to add a new product
# Coded by Shani
@app.route('/add_product', methods=['POST'])
def add_product():
    if 'logged_in' not in session:  # Check if user is logged in
        return redirect(url_for('login'))

    # Extract product details from form
    product_name = request.form['product_name']
    description = request.form['description']
    price = request.form['price']
    stock_quantity = request.form['stock_quantity']
    status = "In Stock" if int(stock_quantity) > 0 else "Out of Stock"

    # Handle image upload if provided
    image_filename = None
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_filename = filename

    cur = mysql.connection.cursor()
    # Insert product into products table
    cur.execute("INSERT INTO products (product_name, description, price, stock_quantity, status, image_filename) VALUES (%s, %s, %s, %s, %s, %s)",
                (product_name, description, price, stock_quantity, status, image_filename))
    # Sync with inventory table
    product_id = cur.lastrowid
    cur.execute("INSERT INTO inventory (item_name, category, quantity, product_id, status) VALUES (%s, %s, %s, %s, %s)",
                (product_name, 'Finished Product', stock_quantity, product_id, status))
    mysql.connection.commit()
    cur.close()
    flash("New product added successfully!", "success")
    return redirect(url_for('product_listing'))
#---------------------------------------------------------------------------------------------------#
# Route to view certifications
# Coded by Nidhi
@app.route('/certifications')
def certifications():
    if 'logged_in' not in session:  # Check if user is logged in
        return redirect(url_for('login'))

    # Fetch all certifications from the database
    cur = mysql.connection.cursor()
    cur.execute("SELECT certification_name, machine_names, description, validity_period, issuing_authority, required_for FROM certifications")
    certifications = cur.fetchall()
    cur.close()
    return render_template('certifications.html', certifications=certifications)
#---------------------------------------------------------------------------------------------------#
# Route for marketing reports page
# Coded by Shani
@app.route('/marketing')
def marketing_reports():
    return render_template('marketing.html')
#---------------------------------------------------------------------------------------------------#
# Route to generate and download a marketing report PDF
# Coded by Shani
@app.route('/download_report')
def download_report():
    filename = "Marketing_Report.pdf"
    filepath = f"./{filename}"
    # Create a PDF using ReportLab
    c = canvas.Canvas(filepath, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, "Marketing & Sales Report")
    c.setFont("Helvetica", 12)
    c.drawString(100, 720, "1. Sales Growth: Strong performance in the last year.")
    c.drawString(100, 700, "2. Revenue Breakdown: Cookware is the leading category.")
    c.drawString(100, 680, "3. Customer Growth: Significant increase in Q4.")
    c.save()
    # Send the generated PDF as a downloadable file
    return send_file(filepath, as_attachment=True)
#---------------------------------------------------------------------------------------------------#
# Route to view completed orders
# Coded by Rajshree
@app.route('/completed_orders')
def completed_orders():
    if 'logged_in' not in session:  # Check if user is logged in
        return redirect(url_for('login'))

    # Fetch completed or ready-for-delivery orders
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT id, customer_name, product_name, quantity, status 
        FROM orders
        WHERE status = 'Completed' OR status = 'Ready for Delivery'
    """)
    orders = cur.fetchall()
    cur.close()
    return render_template('completed_orders.html', orders=orders)
#---------------------------------------------------------------------------------------------------#
# Route to mark an order as ready for delivery
# Coded by Harsh
@app.route('/mark_ready_for_delivery/<int:order_id>', methods=['POST'])
def mark_ready_for_delivery(order_id):
    if 'logged_in' not in session:  # Check if user is logged in
        return redirect(url_for('login'))

    # Update order status to 'Ready for Delivery'
    cur = mysql.connection.cursor()
    cur.execute("UPDATE orders SET status = 'Ready for Delivery' WHERE id = %s", [order_id])
    mysql.connection.commit()
    cur.close()
    flash("✅ Delivery message has been sent to DPD. They will collect the orders soon!", "success")
    return redirect(url_for('completed_orders'))
#---------------------------------------------------------------------------------------------------#
# Route to get stock quantity for a product (API endpoint)
# Coded by Harsh
@app.route('/get_stock/<string:product_name>')
def get_stock(product_name):
    # Fetch stock quantity for the specified product
    cur = mysql.connection.cursor()
    cur.execute("SELECT stock_quantity FROM products WHERE product_name = %s", [product_name])
    result = cur.fetchone()
    cur.close()
    stock = result[0] if result else 0
    # Return stock info as JSON
    return jsonify({"product_name": product_name, "stock": stock})
#---------------------------------------------------------------------------------------------------#
# Route for order progress dashboard
# Coded by Nidhi
@app.route('/order_progress_dashboard')
def order_progress_dashboard():
    if 'logged_in' not in session:  # Check if user is logged in
        return redirect(url_for('login'))
    return render_template('order_progress_dashboard.html')
#---------------------------------------------------------------------------------------------------#
# Route to get live order progress data (API endpoint)
# Coded by Nidhi
@app.route('/live_order_progress')
def live_order_progress():
    if 'logged_in' not in session:  # Check if user is logged in
        return redirect(url_for('login'))

    # Fetch orders in progress with stamper and operative details
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT a.order_id, o.customer_name, a.product_name, a.quantity, 
               s.name AS stamper_name, p.name AS operative_name,
               a.stamper_status, a.operative_status, o.status
        FROM assigned_tasks a
        JOIN orders o ON a.order_id = o.id
        LEFT JOIN stampers s ON a.stamper_id = s.id
        LEFT JOIN production_operatives p ON a.operative_id = p.id
        WHERE o.status NOT IN ('Completed', 'Ready for Delivery')
    """)
    orders_in_progress = cur.fetchall()
    cur.close()
    return {"orders": orders_in_progress}  # Return as JSON-like dict
#---------------------------------------------------------------------------------------------------#
# Route for customer registration
# Coded by Nidhi
@app.route('/customer/register', methods=['GET', 'POST'])
def customer_register():
    if request.method == 'POST':
        # Extract customer registration data
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])  # Hash password

        cur = mysql.connection.cursor()
        try:
            # Insert new customer into the database
            cur.execute("INSERT INTO customers (name, email, password) VALUES (%s, %s, %s)", 
                        (name, email, password))
            mysql.connection.commit()
            flash("Registration successful! Please login.", "success")
            return redirect(url_for('customer_login'))
        except mysql.connection.Error as e:
            flash(f"Error: {str(e)}", "danger")
        finally:
            cur.close()

    return render_template('customer_register.html')
#---------------------------------------------------------------------------------------------------#
# Route for customer login
# Coded by Nidhi
@app.route('/customer/login', methods=['GET', 'POST'])
def customer_login():
    if request.method == 'POST':
        # Extract login credentials
        email = request.form['email']
        password = request.form['password']

        # Query customer from database
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM customers WHERE email=%s", [email])
        customer = cur.fetchone()
        cur.close()

        # Verify customer and password
        if customer and check_password_hash(customer[3], password):
            # Set session variables for logged-in customer
            session['customer_logged_in'] = True
            session['customer_id'] = customer[0]
            session['customer_name'] = customer[1]
            session['customer_email'] = customer[2]
            flash("Login successful!", "success")
            return redirect(url_for('customer_dashboard'))
        else:
            flash("Invalid email or password.", "danger")

    return render_template('customer_login.html')
#---------------------------------------------------------------------------------------------------#
# Route for customer dashboard
# Coded by Rajshree
@app.route('/customer/dashboard')
def customer_dashboard():
    if 'customer_logged_in' not in session:  # Check if customer is logged in
        return redirect(url_for('customer_login'))

    # Fetch customer's orders from the database
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, product_name, quantity, status, created_at FROM orders WHERE email=%s", 
                [session['customer_email']])
    orders = cur.fetchall()
    cur.close()

    # Render customer dashboard with order details
    return render_template('customer_dashboard.html', 
                         customer_name=session['customer_name'], 
                         orders=orders)
#---------------------------------------------------------------------------------------------------#
# Route to log out a customer
# Coded by Nidhi
@app.route('/customer/logout')
def customer_logout():
    # Remove customer session variables
    session.pop('customer_logged_in', None)
    session.pop('customer_id', None)
    session.pop('customer_name', None)
    session.pop('customer_email', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('customer_login'))
#---------------------------------------------------------------------------------------------------#
# Route for customers to place an order
# Coded by Harsh
@app.route('/place_order', methods=['GET', 'POST'])
def place_order():
    if 'customer_logged_in' not in session:  # Check if customer is logged in
        return redirect(url_for('customer_login'))

    cur = mysql.connection.cursor()
    # Fetch product details including price and image filename
    cur.execute("SELECT product_name, stock_quantity, price, image_filename FROM products")
    products = cur.fetchall()
    cur.close()

    # Define default product images for display
    product_images = {
        'Non-stick Frying Pan': 'modern frying pans.jpg',
        'Titanium Saucepan': 'modern frying pans.jpg',
        'Oven-Safe Wok': 'colourful frying pans 2 sizes.jpg',
        'Grill Pan': 'pexels-cottonbro-4543002.jpg',
        'Induction-Compatible Skillet': 'pexels-gary-barnes-6248797.jpg',
        'Stainless Steel Casserole': 'pexels-karolina-grabowska-6659680.jpg',
        'Double Handle Dutch Oven': 'pexels-kevin-malik-9016831.jpg',
        'Ceramic Coated Saute Pan': 'pexels-vovkapanda-6213723.jpg',
        'Hard Anodized Fry Pan': 'royal-fan-1195360_1920.jpg',
        'Glass Lid Stockpot': 'royal-fan-1195362_1920.jpg',
        "Chef's Choice Pan Set": 'pexels-vovkapanda-6213723.jpg',
        'Multi-layer Non-stick Tava': 'royal-fan-1195365_1920.jpg',
        'Heavy-duty Roasting Tray': 'kitchen utensils.jpg',
        'Pasta Cooking Pot': 'meal-5921491_1920.jpg',
        'Copper Core Saucepan': 'gnocchi-9450869_1920.jpg',
    }
    # Combine product data with image URLs
    products_with_images = [
        (p[0], p[1], p[2], url_for('static', filename=f'images/uploads/{p[3]}') if p[3] else url_for('static', filename=f'images/frying pan pics/{product_images.get(p[0], "modern frying pans.jpg")}'))
        for p in products
    ]

    if request.method == 'POST':
        customer_name = session['customer_name']
        email = session['customer_email']
        cart_data = json.loads(request.form['cart'])  # Parse cart data from JSON

        if not cart_data:
            flash("Your cart is empty!", "danger")
            return redirect(url_for('place_order'))

        cur = mysql.connection.cursor()
        all_valid = True
        # Validate stock availability for each item in the cart
        for item in cart_data:
            product_name = item['product_name']
            quantity = int(item['quantity'])

            cur.execute("SELECT stock_quantity FROM products WHERE product_name = %s", [product_name])
            stock = cur.fetchone()

            if not stock or stock[0] < quantity:
                flash(f"Sorry, only {stock[0] if stock else 0} {product_name}(s) available!", "danger")
                all_valid = False
                break

        if all_valid:
            # Insert each cart item as an order
            for item in cart_data:
                product_name = item['product_name']
                quantity = int(item['quantity'])
                cur.execute("INSERT INTO orders (customer_name, email, product_name, quantity) VALUES (%s, %s, %s, %s)",
                            (customer_name, email, product_name, quantity))
            mysql.connection.commit()
            flash("Your order has been placed successfully!", "success")
        else:
            cur.close()
            return redirect(url_for('place_order'))

        cur.close()
        return redirect(url_for('customer_dashboard'))

    return render_template('place_order.html', products=products_with_images)
#---------------------------------------------------------------------------------------------------#
# Main entry point to run the Flask app in debug mode
# Coded by Rajshree
if __name__ == '__main__':
    app.run(debug=True)
#---------------------------------------------------------------------------------------------------#