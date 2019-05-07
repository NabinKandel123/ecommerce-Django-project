# eCommerce Shop Django Project

### Development Steps
1. Requirements Gathering
2. Create Project (django-admin startproject ecommerce)
3. Create App (python manage.py startapp shop)
4. Write Models
5. Add app in settings.py
6. Register app in admin
7. Install dependencies (pip install -r requirements.txt)
8. Create migrations (python manage.py makemigrations shop)
9. Migrate (python manage.py migrate)
10. Media file handling
11. Add meta in models
12. Create urls for frontend
13. Write views
14. Create templates
15. Work for signup and login
16. Bootstrap template setup
17. Home page and detail page design
18. Review and forms
19. Other remaining features
20. Finalizing project


### Installations
- cd ecommerce-shop
- pip install -r requirements.txt
- python manage.py migrate
- python manage.py runserver


### eCommerce Project Features
- Admin adds the category and products
- Browses all the products and categories
- Search all the products using filters
- Add products in cart
- User can signup and login
- User can checkout product
- User can add review for the product

### System Requirements
1. Categories
	- name
	- slug
	- image
	- description
	- featured
	- active

2. Products
	- name
	- slug
	- image
	- brand
	- shipping
	- description
	- price
	- category
	- featured
	- active
	- created
	- modified

3. Review
	- product
	- user
	- rate
	- review
	- created

4. User
	- username
	- email
	- password
