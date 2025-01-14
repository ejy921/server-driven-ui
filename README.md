Writing front-end UI components with NO HTML/CSS and only the backend!
Here, I wrote code for creating UI components that visualize a order processing system

Instructions:

1. git clone <url>
2. cd server-driven-ui
3. python -m venv venv
4. venv\Scripts\activate (for Windows), venv/bin/activate (for Mac)
5. pip install -r requirements.txt


Features:

- Data synchronization between JSON file and PostgreSQL database
Both the JSON file and PostgreSQL database contain data to render in the UI, and changes made in one are
reflected in the other.
The JSON file makes it easy to add/remove data for the user, whereas PostgreSQL enables more complex
relational operations between the data.
