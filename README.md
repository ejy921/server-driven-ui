Front-end UI components with NO HTML/CSS and only the backend.

In this project, I wrote code for creating UI components that visualize a order processing system.

Instructions:

1. `git clone <url>`
2. `cd server-driven-ui`
3. `python -m venv venv`
4. `venv\Scripts\activate (for Windows), venv/bin/activate (for Mac)`
5. `pip install -r requirements.txt`


Structure:

The schema.json contains the customer list and the list of products in the store.
The PostgreSQL database contains the customer list, product list, order details, and workflow details.
It obtains customer and product data by parsing through schema.json.
