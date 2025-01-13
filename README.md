# ONE STEP AT A TIME
#### Video Demo:  [One Step at a Time](https://youtu.be/gOvEabrXzrs)
## Project Overview
**One Step at a Time** is a web application designed to help users manage their tasks efficiently. The inspiration for this project came while solving CS50's problem sets, where there was a recurring piece of advice: break down big problems into smaller, more manageable ones. This approach made challenging tasks feel less overwhelming and more achievable. As someone who experiences anxiety, I realized that I could apply this same concept to my daily life tasks, making them more manageable and leading to better results — one small step at a time. With this in mind, I felt inspired to create a web application that encourages people to break big goals into smaller tasks and track their progress.

This web application allows users to create, view, and delete tasks, as well as marking them as completed, while tracking their progress using statistics and visual representations (charts) of task completion. Additionally, users have access to a list of links to inspire them and keep them motivated as they work toward their goals.

The application is built using **Python (Flask)** for the back-end, **SQL** for the database, and **HTML/CSS/JavaScript** for the front-end. It also utilizes **Chart.js** for data visualization and **Bootstrap** for responsive design and styling.

## File Structure
Below is a description of each file in this project and its role in this application.

### 1. app.py
This is the main application file that handles routing, logic, and communication with the database.

**Key Features:**
- Manages user authentication (registration and login) and task management.
- Provides a secure login system with Flask's `session` and `@login_required` decorator to restrict access to certain pages.
- Handles both GET and POST requests to create, update, and delete tasks.
- Connects to a SQL database to create, retrieve, update, and delete task records, ensuring that tasks are properly managed and displayed in the application.
- Displays tasks ordered by due date, with separate views for current and past tasks.
- Offers statistics on task completion, including daily and monthly task completion rates.
- Uses Flask templates to render dynamic pages with task data and completion statistics.

**Routes**

<ins>Access Control:</ins> All routes that require the user to be logged in are protected using the `@login_required` decorator.

1. `/` (Home Page)
    - Displays the main page after the user is logged in.
    - Access Control: Requires login.
2. `/register` (New User Registration)
    - Allows new users to register by providing a username and password.
    - Validates input and ensures username is unique and passwords match before adding the user to the database.
    - Hashed passwords are used for secure storage to ensure safety.
3. `/login` (User Login)
    - Authenticates users by checking their username and password in the database.
    - If credentials are valid, the user is logged in and redirected to the home page.
4. `/logout` (User Logout)
    - Logs the user out by clearing their session and redirects them to the login page.
5. `/tasks` (View Tasks)
    - Displays present and future tasks for the logged-in user, grouped and sorted by due date. Past tasks are not shown on this page.
    - The due date is displayed in a user-friendly format ("Month Day, Year").
    - Access Control: Requires login.
6. `/add_task`(Add a New Task)
    - Allows the user to add a new task by providing a description and due date. This form is located on the same page where tasks are displayed.
    - Task is inserted into the database with a "not completed" status.
    - Access Control: Requires login.
7. `/complete_task/<int:task_id>` (Mark Task as Completed)
    - Marks the task with the given ID as completed.
    - Access Control: Requires login.
8. `/unmark_task/<int:task_id>` (Unmark Task as Completed)
    - Unmarks the task with the given ID as completed.
    - Access Control: Requires login.
9. `/delete_task/<int:task_id>` (Delete Task)
    - Deletes the task with the given ID from the database.
    - Access Control: Requires login.
10. `/past_tasks` (View Past Tasks)
    - Displays tasks that are past due, ordered by due date in descending order.
    - The due date is displayed in a user-friendly format ("Month Day, Year").
    - Access Control: Requires login.
11. `/statistics` (View Task Completion Statistics)
    - Displays overall task statistics, including the total number of tasks and completed tasks.
    - Provides daily and monthly percentage of task completion rates.
    - It only displays the daily completion rates for the current month.
    - The dates are displayed in a user-friendly format ("Month Day, Year" or "Month, Year").
    - Access Control: Requires login.
12. `/useful_links` (Useful Links Page)
    - Displays a page with useful links for the user.
    - Access Control: Requires login.

### 2. tasks.db
This is the SQL database file where user authentication data (username and password), tasks, due dates, and completion statuses are stored.

**Key Features:**
- `users` table stores essential authentication data, including a unique username and hashed password.
- `tasks` table stores user tasks with attributes like description, due date, and completion status.
- **Relationship:** Each task is uniquely linked to a user by the `user_id` foreign key.
- **Indexes** have been created on frequently used columns (such as `due_date`, `completed`, and `user_id`) for improved query performance.

**Tables:**
1. `users`
    - id (INTEGER, PRIMARY KEY, AUTOINCREMENT);
    - username (TEXT, UNIQUE, NOT NULL);
    - password (TEXT, NOT NULL).
2. `tasks`
    - id (INTEGER, PRIMARY KEY, AUTOINCREMENT);
    - user_id (INTEGER, NOT NULL, FOREIGN KEY REFERENCES users (id));
    - description (TEXT, NOT NULL);
    - due_date (DATE, NOT NULL);
    - completed (BOOLEAN, DEFAULT 0).

## 3. Templates
This section describes the HTML templates used in this application. All files are located in the `templates/` folder. These templates are used to display content that is customized based on the user’s data, session information, or database records.

1. `layout.html`
    - Serves as the base layout for all pages in the application.
    - Includes metadata for proper scaling on mobile devices ensuring that the site is responsive and adapts to various screen sizes.
    - Loads external resources like **Bootstrap** for styling, **Chart.js** for displaying charts, and the `styles.css` file for additional custom styles. It also includes Bootstrap JavaScript functionality.
    - The navigation bar uses Bootstrap's built-in classes and JavaScript to create a collapsible navbar, providing an easy-to-use navigation experience on both desktops and mobile devices.
    - Uses Flash messages for feedback, such as error notifications.
    - Implements a **Jinja** template, allowing individual pages to extend this layout and add dynamic content.

- <ins>Jinja Template:</ins> All HTML pages in this project inherit from `layout.html` using **Jinja** templates to enable dynamic content rendering.
- <ins>Bootstrap:</ins> All HTML pages utilize **Bootstrap** for a responsive, well-structured, and user-friendly design.

2. `register.html`
    - The page contains a form for new users to create an account with fields for **Username**, **Password** and **Password Confirmation.**
    - The form includes required fields to ensure all inputs are filled before submission.
    - The **Submit** button allows users to submit the form after entering the required details.
3. `login.html`
    - The page contains a form for registered users to login in the web application with fields for **Username** and **Password**.
    - The form includes required fields to ensure all inputs are filled before submission.
    - The **Submit** button allows users to submit the form after entering the required details.
    - A link is provided for users who don’t have an account (in addition to the one in the navigation bar), allowing them to go to the **Registration** page.
4. `index.html`
    - The page introduces the purpose of the web application, featuring a motivational message with an image to inspire users to take small steps toward achieving their goals.
    - Key functionalities are outlined, including managing and visualizing tasks, tracking their progress, and accessing useful links.
    - It gives attribution to Pexels and the photographers for the images used on this website.
5. `tasks.html`
    - A form is provided for the user to add new tasks, which requires a description and a due date.
    - The added tasks are displayed on the page, grouped by due date.
    - Each task includes options to mark as completed, unmark as completed, and delete.
    - Completed tasks are visually indicated with strikethrough text.
6. `past_tasks.html`
    - Displays a list of past tasks, each showing the task description and its formatted due date.
    - Completed tasks are visually marked with strikethrough text for clear identification.
    - If there are no past tasks, a message informs the user that no past tasks are available.
7. `statistics.html`
    - Displays visual representations of task completion data using **Chart.js** with three distinct charts:
        - **Pie Chart** for overall completion rate (Completed vs. Incomplete tasks).
        - **Bar Chart** for daily completion rates (displaying only data of the current month).
        - **Line Chart** for monthly completion rates.
    - The data for the charts is dynamically added from the backend using **Jinja** template.
    - Customizes chart colors to display progress.
    - Provides responsive, interactive, and clear visual feedback for users to track their progress over time.
    - If no tasks are added, the user is informed that there are no tasks to display in the statistics.
8. `useful_links.html`
    - This page provides users with a curated list of external resources to stay motivated, inspired, and productive.
    - The links are categorized into three sections:
        - TEDx Talks: Features motivational talks about small steps, consistent actions, and achieving big goals.
        - Articles: Provides insightful articles from reputable sources like Harvard Business Review and Medium on the power of small wins and incremental progress.
        - Relaxing Sounds: Offers links to nature-inspired soundscapes (like forest, ocean, and rain sounds) to help users maintain focus and reduce stress.

### 4. Static
This section describes the static content in this project, such as images and styles. All files are located in the `static/` folder. These files are used to customise and style the HTML pages.

1. `styles.css`
    - Contains styling attributes for various HTML elements, such as background color, text color, font size, height, width, text alignment, and margin.
    - Customizes the visual design, including colors, sizes, and overall structure for a better user experience.
2. `background.jpg`
    - Used as the background image in the navigation bar across all HTML pages.
    - The image is from [Pexels](https://www.pexels.com/) by the photographer Dana Tentis. According to their license, all photos are free to use, and attribution is not required.
3. `tasks.jpg`
    - Featured as an image on the `index.html` page to complement the content.
    - The image is from [Pexels](https://www.pexels.com/) by the photographer Bruno Bueno. According to their license, all photos are free to use, and attribution is not required.

## How to Access the Web Application
1. **Run the Application:** In your terminal window, use the **Flask Run** command to start the web application.
2. **Register:** To access all features of the web application, you will need to register. Go to the "Register" page, where you will be prompted to create a username and password (make sure to confirm your password). If everything is correct, you'll be redirected to the login page.
3. **Login:** On the login page, enter the username and password you just created. After logging in, you will have full access to the web application’s features.
4. Once logged in, you can:
    - Add and visualize tasks
    - Analyze your task completion statistics
    - Explore useful links

All of these features are accessible by clicking on the specific pages in the navigation bar.

## Useful Resources
During the development of this project, I referred to several helpful resources:
- [W3Schools](https://www.w3schools.com/): It was instrumental in learning how to implement some HTML structures. It also provided guidance on various styling attributes used in `styles.css` and offered practice with the programming languages used in this web application.
- [Chart.js Documentation](https://www.chartjs.org/docs/latest/): Used to create beautiful and interactive visualizations for task completion data.
- [Bootstrap Documentation](https://getbootstrap.com/): Essential for implementing responsive design and styling components throughout the web application.
- [Pexels](https://www.pexels.com/): A helpful resource for free images used in this web application.
- [CS50.ai](https://cs50.ai/chat) and [ChatGPT](https://chatgpt.com/): These platforms were helpful in identifying mistakes in my code and providing guidance throughout the development process.
