import reflex as rx
from .pages import landing, home
from .states.auth_state import AuthState

app = rx.App()
app.add_page(landing.index, route="/")
app.add_page(AuthState.require_auth(home.home_page), route="/home")  # Apply decorator directly
#app.add_page(home.home_page, route="/home")
app.add_page(home.payment_callback, route="/payment-callback")


"""
project/
│                
├── main.py   
├── components/ 
│   ├── footer.py  
│   ├── login.py  
│   ├── nav.py  
│   ├── recovery.py  
│   ├── reg_success.py  
│   ├── register.py 
│   ├── side_nav.py  
│   ├── signin.py
│   ├── signup.py     
├── pages/              
│   ├── contributions.py         
│   ├── dashboard.py         
│   ├── home.py           
│   ├── landing.py      
│   ├── notification.py  
│   ├── schedule.py 
│   ├── transaction.py  
│   ├── withdrawal.py 
├── states/              
│   ├── app_state.py         
│   ├── auth_state.py         
│   ├── contribution_state.py           
│   ├── login_state.py      
│   ├── user_data.py  
└── README.md             
"""