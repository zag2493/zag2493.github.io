---
layout: default
title: "Databases"
permalink: /enhancements/databases/
---

# Databases

<div style="background-color: #c9c7c7; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 30px;">

<!-- Database Screenshot -->
<div style="text-align:center; margin-bottom: 15px;">
  <img src="/images/db.png" alt="Lost Lab Database Screenshot" style="max-width:100%; border-radius:10px;">
</div>

As the other two enhancements I chose to use Lost Lab for my database enhancement. Originally a Python-based adventure game developed for IT 140 as a simple, dictionary-driven text game. For this enhancement I focused on database integration, building on previous enhancements in Software Engineering and Design and Algorithms and Data Structure. This phase introduces SQLite for persistent state management, which replaced a JSON-based save/load system implemented when first beginning enhancements. I decided to use Lost Lab for the databases category as it demonstrates my growth from a novice developer relying on temporary data to one capable of designing robust, persistent systems. The original game's lack of state retention limited replay ability, making it an ideal candidate to demonstrate database skills. This enhancement transforms it into a scalable, data-driven application, placing an emphasis on professional database practices and preparing me for roles requiring reliable data management.    

</div>

Specific components highlight my database development skills:

- **SQLite Database:** Implemented tables player, inventory, rooms, and logs with foreign keys to ensure integrity, replacing the JSON for persistent storage.

- **CRUD Operations:** Added methods like db_init (schema setup), save_to_db (store player state), load_from_db (restore game), and log_action (tracks win/lose), enabling seamless gameplay continuity.

- **Data Visualization:** Developed plot_win_lose to query logs table and visualize win/lose outcomes using Matplotlib, providing player analytics.

- **Unit Testing:** Extended test_Lost_Lab_Enhanced.py with tests like test_save_load_db to validate data integrity across sessions, ensuring reliability.

- **Security:** Used parameterized queries to prevent SQL injection, enhancing security.

<div style="background-color: #c9c7c7; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 30px;">

The enhancements improved the artifact by enabling persistent gameplay, players can save progress and resume later, unlike the original's volatile state. The SQLite database supports scalability for future expansions, and visualizations add user value and can be used to show other statistics in further expansions as well. Skills demonstrated include schema design, query optimization, and secure data handling, aligning with industry standards for database-driven applications. Enhancing Lost Lab with SQLite taught me how critical the role of a database can be in creating user-centric, persistent applications. Designing the schema deepened my understanding of relational principles, while implementing the CRUD operations revealed the importance of transactions for data consistency. The plot_win_lose query, pulling win/lose ratios from the logs table, showed me how databases can drive analytics, enhancing gameplay insights. Since SQLite was planned from design phase, it seamlessly integrated with OOP and GUI components, showing the value of modular design. As the other enhancements did, there was challenges to work through. Issues with handling schema mismatches which was corrected by implementing foreign key constraints and optimizing queries for performance such as indexing logs for faster visualization. The process allowed me to focus on the ability to balance functionality, performance, and security. For example, anticipating edge cases like database corruption, adding try-except blocks for graceful recovery. This enhancement built on my algorithms work and GUI showing how interconnected systems create cohesive applications. 

<!-- Visual Screenshot -->
<div style="text-align:center; margin-bottom: 15px;">
  <img src="/images/visual.png" alt="Lost Lab Visual Data Screenshot" style="max-width:100%; border-radius:10px;">
</div>

</div>

Course Outcomes

- **Collaborative Environments:** Detailed docstrings help collaborators understand CRUD functions, test cases support team and stakeholder reviews.

- **Professional Communications:** GUI displays database-driven stats, such as win/lose visual, and the graphs communicate player progress to non-technical users. Logs located in the bottom of screen indicate actions such as save, load, and any errors.

- **Computing Solutions:** Designed SQLite schema and CRUD operations, trading off JSON simplicity for persistent scalability.

- **Innovative Techniques:** Leveraged SQLite and Matplotlib for data persistence and analytics, delivering value through robust storage and user insights.

- **Security Mindset:** Used parameterized queries and foreign keys to prevent injection and ensure data integrity, with tests validating secure save/load operations.

<div style="text-align:center; margin-top:20px;">
  <a href="https://github.com/zag2493/zag2493.github.io/blob/main/LostLabEnhanced.py" 
     target="_blank" 
     rel="noopener noreferrer"
     style="background-color:#4CAF50; color:white; padding:10px 25px; text-decoration:none; border-radius:5px; font-weight:bold;">
     View Lost Lab Enhanced on GitHub
  </a>
</div>

<div style="text-align:center; margin-top:20px;">
  <a href="https://github.com/zag2493/zag2493.github.io/blob/main/test_Lost_Lab_Enhanced.py" 
     target="_blank" 
     rel="noopener noreferrer"
     style="background-color:#4CAF50; color:white; padding:10px 25px; text-decoration:none; border-radius:5px; font-weight:bold;">
     View Lost Lab Unit Tests on GitHub
  </a>
</div>

<div style="text-align:center; margin-top:20px;">
  <a href="https://github.com/zag2493/zag2493.github.io/blob/main/performance.py" 
     target="_blank" 
     rel="noopener noreferrer"
     style="background-color:#4CAF50; color:white; padding:10px 25px; text-decoration:none; border-radius:5px; font-weight:bold;">
     View Lost Lab Performance File on GitHub
  </a>
</div>

<div style="text-align:center; margin-top:40px;">
  <a href="/" 
     style="background-color:#555; color:white; padding:10px 25px; text-decoration:none; border-radius:5px; font-weight:bold;">
     ⬅ Back to Home
  </a>
</div>
 


