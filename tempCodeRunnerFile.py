@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        wants_json = request.accept_mimetypes['application/json']
        
        name = request.form['name']
        username = request.form['username']
        email = request.form['email'].lower()
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            if wants_json:
                return jsonify({
                    'success': False,
                    'message': 'Username already exists. Please choose a different one.'
                })
            flash('Username already exists. Please choose a different one.')
            return redirect(url_for('register'))
        
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            if wants_json:
                return jsonify({
                    'success': False,
                    'message': 'Email already exists. Please choose a different one.'
                })
            flash('Email already exists. Please choose a different one')
            return redirect(url_for('register'))

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        new_user = User(name=name, username=username, email=email, password=hashed_password)
            
        db.session.add(new_user)
        db.session.commit()
            
        if wants_json:
            return jsonify({
                'success': True,
                'message': 'Account Created Successfully, Please Login!',
                'redirect': url_for('login')  
            })
        flash('Account Created Successfully, Please Login!')
        return redirect(url_for('login'))  

    return render_template('register.html', time=int(time.time()))