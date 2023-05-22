# Income Management
<p align="center">
  <img src="https://raw.githubusercontent.com/GM-Frost/Frosty-Inv-Management/master/Images/App-Logo-Main.png" width="350" title="hover text">
  <img src="https://raw.githubusercontent.com/GM-Frost/Frosty-Inv-Management/master/Images/App-Icon.png" width="350" alt="accessibility text">
</p>

# 🔗 Django Site
<a href ="#" target="_blank">Test the Site </a>

# Project Description
This project was built to learn various aspects of Django, including Router, Models, tables, Authentications, Email Validation, charts, and designing of the admin panel. The project allows users to specify their income and expenditure using a form, and the records are stored in a PostgreSQL database.

# Functionality

**Income Records:** Users can enter the amount, description, select the source of income, and specify the date. After submitting the form, the record is added to the Income Model and displayed along with an asynchronous JavaScript summary chart.
**Expense Records:** Similar to the income records, users can enter the expense amount, description, select the category, and specify the date. The submitted form updates the expense model and displays the chart along with the record.
**CRUD Functionality:** Users can update and remove both income and expense records.
**User Registration:** Before using the application, users are required to register on the site. Registration includes instant validation and uses asynchronous AJAX validation. Validation prompts are displayed to the user on the same page.
**Email Activation (Currently Disabled):** Note that the email activation functionality is temporarily removed due to issues with the SMTP configuration. The application is unable to send the email activation link to the user's registered email. For now, the registered user's status is updated manually by the admin.
**Modified Admin Dashboard:** The admin dashboard has been customized with an enhanced visual appearance, different from the default admin dashboard.
**Download Records:** Allows user to do the Crud function and also download the record in PDF | CSV | Excel format

# Set up the PostgreSQL database and configure the database settings in the project's settings file.

# Usage
1) Register a new user account on the site.:
git https://github.com/GM-Frost/Frosty-Inv-Management.git

2) Log in to the application using your credentials
upload the Databasefiles provided.
Current Database Info: user="root",password="Admin123",host="localhost",database="gmfrost_inv_mgmt"

Application Login: username= admin123, password= admin123

3) Use the provided forms to add income and expense records

4) View the summary charts and records for income and expenses.
5) Update or remove any records as needed.
6) Download the record in PDF / CSV / Excel Format