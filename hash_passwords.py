import streamlit_authenticator as stauth

# List of app-specific passwords (different from email passwords)
passwords = ['qwerqwer2', 'bachjs88', 'chopinFR10']
hashed_passwords = stauth.Hasher(passwords).generate()

print("Hashed passwords:")
for hp in hashed_passwords:
    print(hp)