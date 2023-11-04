# Student-Grievance-System

## User Stories for Student Grievance System

### Students
- As a student, I want to easily register and log into the grievance system to report my concerns.
- As a student, I want to submit a grievance, providing all necessary details, so that my issue can be addressed accurately.
- As a student, I want to view the status of my grievances to monitor their progress towards resolution.
- As a student, I want to receive notifications about any updates or changes related to my grievances to stay informed.
- As a student, I want access to a user manual or guide to understand how to use the system effectively.
### Staff & Faculty
- As a staff member, I want to receive notifications of new grievances assigned to me for resolution.
- As a faculty member, I want to review grievances related to my department or courses to take necessary actions.
- As a staff or faculty member, I want to update the status of grievances I'm handling to keep relevant parties informed.
- As a staff member, I want to attend training sessions to understand how to utilize the system optimally.
- As a staff or faculty member, I want access to support if I encounter issues with the system.
### IT Department
- As an IT administrator, I want to ensure the system's integration with existing databases and platforms is seamless.
- As an IT personnel, I want to monitor the system's uptime and ensure it meets the target.
- As an IT administrator, I want to ensure that the grievance system complies with all data security and privacy regulations.
- As an IT staff member, I want to provide support for any technical issues users might face.
### University Administration
- As a university administrator, I want to view KPIs to monitor the system's effectiveness and performance.
- As a university administrator, I want to ensure that all grievances are addressed timely and in compliance with university policies.
- As an executive sponsor, I want to review periodic reports on the system's performance to gauge its impact on student satisfaction and the institution's operations.
- As a university administrator, I want to ensure that all stakeholders are informed and involved in the system's successful rollout and adoption.



# Sprint One

## Sprint One Prioritized User Stories 

### Students
#### Students (A): Registration and Login
As a student, I want to easily register and log into the grievance system to report my concerns.

##### Acceptance Criteria
- The system should provide a user-friendly registration form with fields for first name, last name, email address, and password.
- Users must receive a confirmation email upon successful registration to verify their email address.
- The login page should allow registered students to enter their email and password to access their accounts.
- Invalid login attempts should display appropriate error messages.

#### Students (B): Grievance Submissions 
- As a student, I want to submit a grievance, providing all necessary details, so that my issue can be addressed accurately.

##### Acceptance Criteria
- The system should provide a clear and intuitive interface for students to submit grievances.
- The grievance form should include fields for the student to enter their personal information, grievance type, description, and any supporting documents.
- The system should validate that all mandatory fields are filled before allowing submission.
- Upon submission, the system should generate a unique grievance ID and provide a confirmation message to the student.
- Submitted grievances should be time stamped and stored securely in the database.



### Staff & Faculty 
#### Staff & Faculty (B): Grievance Review
- As a faculty member, I want to review grievances related to my department or courses to take necessary actions. 

##### Acceptance Criteria
- Staff and faculty members should have individual accounts with access to a dashboard.
- The dashboard should display a list of grievances related to the faculty member's department or courses.
- Grievances should be categorized and sortable by grievance type, date, and status.
- Faculty members should be able to click on a grievance to view its details and supporting documents.


### IT Department 
#### IT Department (C)
- As an IT administrator, I want to ensure that the grievance system complies with all data security and privacy regulations. 

##### Acceptance Criteria
- Data storage, transmission, and access should be encrypted to protect sensitive information.
- User access to student data and grievances should be role-based and restricted to authorized personnel only.

## Sprint One Database Schema 
![SGS Sprint One](https://github.com/Bahaa-Hammad/Student-Grievance-System/assets/89856041/073be02a-dc45-41f4-8c2a-fe5ccc885d04)


# Sprint Two

## Sprint Two Prioritized User Stories 

### Students
#### Students (C): Grievance Status View
- As a student, I want to view the status of my grievances to monitor their progress towards resolution. 

#### Acceptance Criteria
- After logging in, students should be able to view a list of their submitted grievances.
- Students should be able to search for specific grievances based on grievance ID or type.
- Students should have the ability to filter grievances by status (open, resolved).
- Students should be able to click on a specific grievance to view its details, including the description and any supporting documents.

#### Staff and Faculty (C): Grievance Status Update
- As a staff or faculty member, I want to update the status of grievances I'm handling to keep relevant parties informed.

#### Acceptance Criteria
- After logging in, staff and faculty members should access a dashboard listing grievances assigned to them.
- The system should provide an option to update the status of each grievance, allowing staff and faculty members to indicate if a grievance is "in progress," "resolved," or any other relevant status. 
- When updating the status, staff and faculty members should have the ability to add comments or notes to provide additional context or updates regarding the grievance. 
- Clicking on a specific grievance should allow a detailed view, including the grievance's description, status history, and any attached files or references.


# Sprint Three

## Sprint Three Prioritized User Stories

### Students
#### Students (D): Grievance Notification 
- As a student, I want to receive notifications about any updates or changes related to my grievances to stay informed

#### Acceptance Criteria
- When a student submits a grievance, they should automatically be subscribed to receive notifications regarding updates or changes related to their grievance.
- The notifications should be sent via the email
- The notification should include clear and concise information about the update or change to the grievance
