import streamlit as st
import pandas as pd
import sqlite3 

conn = sqlite3.connect('data.db')
c=conn.cursor()

def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT, password TEXT)')

def add_userdata(username, password):
    c.execute('INSERT INTO userstable(username, password) VALUES (?,?)',(username, password))
    conn.commit()

def login_user(username, password):
    c.execute('SELECT * FROM userstable WHERE username = ? AND password = ?',(username,password))
    data = c.fetchall()
    return data

def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data


def main():
    """Simple login app"""

    st.title("Simple Login App")

    menu = ['Home','Login','SignUp']
    choice = st.sidebar.selectbox('Menu',menu)

    if choice=='Home':
        st.subheader('Home')

    elif choice == 'Login':
        st.subheader('Login Section')
        username = st.sidebar.text_input('User Name')
        password = st.sidebar.text_input('Password', type='password')

        if st.sidebar.checkbox('Login'):
            # if password == "12345":
            create_usertable()
            result = login_user(username, password)
            if result:

                st.success("Logged In as {}".format(username))

                task = st.selectbox('Task',["Profile","Add Post","Analytics"])
                if task=="Profile":
                    st.subheader("Profile")
                    user_result = view_all_users()
                    clean_db = pd.DataFrame(user_result, columns=["Username", "Password"])
                    st.dataframe(clean_db)

                elif task == "Add Post":
                    st.subheader("Add your Post")

                elif task == "Analytics":
                    st.subheader("Analytics")

            else:
                st.warning("Invalid Username or Password")

    elif choice == 'SignUp':
        st.subheader('Create new account')
        new_user = st.text_input("Usename")
        new_password = st.text_input("Password", type = 'password')

        if st.button("Signup"):
            create_usertable()
            add_userdata(new_user, new_password)
            st.success("You have successfully created an accoount")
            st.info("Go to Login Menu to Log in to your account.")


if __name__ == '__main__':
    main()


