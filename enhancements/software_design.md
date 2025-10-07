---
layout: default
title: "Software Engineering & Design Enhancement"
permalink: /enhancements/software_design/
---

# Software Engineering & Design Enhancement 

<div style="background-color: #c9c7c7; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 30px;">

<!-- Original Game Screenshot -->
<div style="text-align:center; margin-bottom: 15px;">
  <img src="images/OG Running.png" alt="Original LostLab Running Screenshot" style="max-width:100%; border-radius:10px;">
</div>

My artifact is "Lost Lab", an interactive text-based adventure game that was originally created as a simple Python script for my IT-140 final project in 2023 at SNHU. At the time, it was my first ever program, a basic dictionary-driven exploration game where players navigated the rooms, collected items, and faced the Alien. The original game had little input handling and no real structure. For my Software Engineering and Design Enhancement I turned it into an object-oriented application with a Tkinter GUI, focusing on the software engineering principles to deliver a more well-rounded application. 

I selected this artifact for this category because it directly contrasts my first novice program with my current proficiency, providing a "before and after" to showcase my growth in Software Engineering and Design. The artifact being my first project, it holds sentimental value but was due for improvement. It's original structure, a single rooms dictionary and raw text input, limited compliance, making it ideal for demonstrating my growth.

<!-- Final Game Running Screenshot -->
<div style="text-align:center; margin-bottom: 15px;">
  <img src="images/FinalGameRunning.png" alt="Final LostLab Enhanced Running Screenshot" style="max-width:100%; border-radius:10px;">
</div>

Specific components highlighting my software development skills:
- **OOP Structure (Room, Player, Game classes):** Encapsulates logic, such as Player.move checking hazards like Med Bay requiring MKIV Suit and MKV Helmet, which showcases modularity and encapsulation for easier maintenance.
- **Tkinter GUI:** Implements a dark-themed interface with a visual map, compass, labeled buttons, and real-time status updates (such as inventory display), this demonstrates UI/UX design for accessibility, tying directly to the planned algorithm enhancements for visualizing graph paths.
- **Input Validation and Error Handling:** Regex (^[a-zA-Z\s]+$) in handle_action secures item entry, preventing invalid inputs, while try-except blocks in database methods ensure graceful failures.
- **Unit Testing and Documentation:** test_Lost_Lab.py validates the enhancements, and the docstrings/comments through all files explain the function or decisions made.

</div>
