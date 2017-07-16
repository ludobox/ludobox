# User

Ludobox uses Flask-Security as a system to manage users.

## Register, Login, Logout

Use the following URLs

- `/register` : POST email, password, confirm_password
- `/login` : POST email, password
- `/logout` : POST

## Roles

There is 4 roles :
- anonymous (not logged in)
- contributor (can add and edit content)
- editor (can delete content, but not users)
- superuser (admin),

The first user registered get the role of `superuser`.

Then every registered user is a `contibutor`

### Access rights per role

```
C = Create (ex: Upload game)
R= Read (ex: Download game)
U= Update (Modify)
D = Delete

Without account :
Games: R, if in validated state
Workshop: R, if in validated state
Page: R (including accounts list, user pages), if in validated state
User account: C

With contributor account :
Games: C, R (needs review & validated states),  U, D (only your own)
Workshop: C, R (needs review & validated states), U, D (only your own)
Page: R

With editor account :
Games: C, R (needs review & validated states),  U, D
Workshop: C, R (needs review & validated states), U, D
Page: R, U, D

With admin account :
Games: C, R (all states), U, D
Workshop: C, R (all states), U, D
Pages: C, R (all states), U, D
User account: C, R, U, D
```

## User Profile

You can access user profile data under `/api/profile/:user_id`.
