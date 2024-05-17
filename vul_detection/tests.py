import os
import requests

# -------------------------------------------------------------------------------------
# Insecure function with various vulnerabilities


def test1(input_data, user_input):
    query = "SELECT * FROM products WHERE id=" + str(x) + " AND name='" 
    query += "'; DROP TABLE users; --"

    a = x + y
    os.system("echo Hello from the system!")
    if x == 0:
        print("x is zero!")
    b = x * y
    c = eval(input("Enter an expression: "))
    return a, b

# -------------------------------------------------------------------------------------


# Did not detect the vulnerabilities : request forgery , redirect
# Combined function with secure and insecure lines
def test2(user_input, redirect_url):
    # Secure session management
    session['user_id'] = 12345

    # Insecure request forgery (potential unauthorized action)
    csrf_token = session.get('_csrf_token')
    if not csrf_token or csrf_token != request.form.get('_csrf_token'):
        return 'Invalid request', 403

    # Secure redirection using Flask
    secure_redirect = redirect(redirect_url)

    if user_input == 'admin':
     # Insecure open redirect (potential phishing attack)
        insecure_redirect = redirect(user_input)
    else:
        return "Invalid user", 403

    # Secure HTTP request with properly set headers
    secure_response = requests.get(
        'https://example.com', headers={'User-Agent': 'Mozilla/5.0'})

    # Insecure remote code execution (potential code execution on server)
    insecure_code_execution = eval(user_input)

    # Secure replay prevention using timestamp or nonce
    timestamp = request.form.get('timestamp')
    nonce = session.get('nonce')
    if timestamp == nonce:
        return 'Valid request', 200
    else:
        return 'Invalid request', 403

    # Insecure cross-frame scripting (potential data theft or modification)
    insecure_frame_scripting = f"""<script> const data = {user_input}; parent.postMessage(data, '*');</script>"""

    # Secure XSS prevention using proper input sanitization
    user_input_sanitized = escape(user_input)

    return secure_redirect, insecure_redirect, secure_response.text, insecure_code_execution, insecure_frame_scripting, user_input_sanitized

# -------------------------------------------------------------------------------------


# Vulnerabilities : function_injection , cross frame , csv ,redirect , session hijack , command injection
# Model did not detect the vulnerabilities : session hijack , redirect
# Combined function with secure and insecure lines
def test3(input_data, user_input, redirect_url):
    # Secure data processing using Pandas
    se_df = pd.DataFrame(input_data)
    # Insecure function injection (potential code execution)
    infunction = eval(user_input)
    # Secure session management
    session['user_id'] = 12345

    # Insecure session hijacking (potential session compromise)
    insession = session['user_id']

    # Secure CSV file export
    sedf.to_csv('data.csv', index=False)
    # Insecure CSV injection (potential data leakage or code execution)
    incsv = os.system(f'cat {user_input}.csv')

    # Secure redirection using Flask
    seredirect = redirect(redirect_url)
    # Insecure redirection (potential open redirect vulnerability)
    inredirect = redirect(user_input)
    # Secure HTTP request with properly set headers
    seponse = requests.get('https://example.com',
                           headers={'User-Agent': 'Mozilla/5.0'})
    # Insecure command injection (potential command execution)
    incommand = os.system('echo ' + user_input)
    return secure_df, insecure_function, insecure_session, secure_redirect, insecure_csv, secure_response.text, insecure_redirect, insecure_command


def simple_function(x, y):
    query = "SELECT * FROM products WHERE id=" + \
        str(x) + " AND name='" + str(y) + "'"
    query += "'; DROP TABLE users; --"

    a = x + y
    os.system("echo Hello from the system!")
    if x == 0:
        print("x is zero!")
    b = x * y
    c = eval(input("Enter an expression: "))
    return a, b


# -------------------------------------------------------------------------------------

# export all file functions as a list of functions
functions = [simple_function, test1, test2, test3, simple_function]
