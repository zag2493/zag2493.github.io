---
layout: default
title: "Software Engineering & Design Enhancement"
permalink: /enhancements/software_design/
---

# Software Engineering & Design Enhancement 

<div style="background-color: #c9c7c7; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 30px;">

<!-- Original Game Screenshot -->
<div style="text-align:center; margin-bottom: 15px;">
  <img src="/images/OG Running.png" alt="Original LostLab Running Screenshot" style="max-width:100%; border-radius:10px;">
</div>

My artifact is "Lost Lab", an interactive text-based adventure game that was originally created as a simple Python script for my IT-140 final project in 2023 at SNHU. At the time, it was my first ever program, a basic dictionary-driven exploration game where players navigated the rooms, collected items, and faced the Alien. The original game had little input handling and no real structure. For my Software Engineering and Design Enhancement I turned it into an object-oriented application with a Tkinter GUI, focusing on the software engineering principles to deliver a more well-rounded application. 

I selected this artifact for this category because it directly contrasts my first novice program with my current proficiency, providing a "before and after" to showcase my growth in Software Engineering and Design. The artifact being my first project, it holds sentimental value but was due for improvement. It's original structure, a single rooms dictionary and raw text input, limited compliance, making it ideal for demonstrating my growth.

<!-- Final Game Running Screenshot -->
<div style="text-align:center; margin-bottom: 15px;">
  <img src="/images/FinalGameRunning.png" alt="Final LostLab Enhanced Running Screenshot" style="max-width:100%; border-radius:10px;">
</div>

</div>

Specific components highlighting my software development skills:

- **OOP Structure (Room, Player, Game classes):** Encapsulates logic, such as Player.move checking hazards like Med Bay requiring MKIV Suit and MKV Helmet, which showcases modularity and encapsulation for easier maintenance.
  
- **Tkinter GUI:** Implements a dark-themed interface with a visual map, compass, labeled buttons, and real-time status updates (such as inventory display), this demonstrates UI/UX design for accessibility, tying directly to the planned algorithm enhancements for visualizing graph paths.
  
- **Input Validation and Error Handling:** Regex (^[a-zA-Z\s]+$) in handle_action secures item entry, preventing invalid inputs and mitigating injection risks, while try-except blocks in database methods ensure graceful failures.
  
- **Unit Testing and Documentation:** test_Lost_Lab.py validates the enhancements, and the docstrings/comments through all files explain the function or decisions made.

<div style="background-color: #c9c7c7; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 30px;">

Enhancing Lost Lab deepened my appreciation for iterative design, showing how small structural changes can yield exponential gains. True engineering isn't just coding but anticipating extensibility, starting with the OOP design let met later integrate NetworkX graphs and SQLite Database without having to rewrite the core logic. Debugging the GUI, as it was my first experience with Tkinter, helped me work on my problem solving, but later gave me more thoughtful ideas, such as adding the 3-second fade on the path finding function. I also had validation challenges, like ensuring regex caught edge cases without over restricting items such as MKIV Suit but stopping MKIV@Suit.

There was of course challenges when going back and fixing my earlier work. While the original artifact did function it had novice errors, such as "Nothing" being an item in the starting room - "Rec Room", since it as listed in the dictionary it was available to be picked up. By following what I learned while at SNHU, I decided to refactor all the globals into classes, while time-consuming, it shows how good coding practices can overcome a bad design. As I continued throughout the project, I would continue to go back and make more adjustments, such as adding the hazards and required items. This improved the gameplay, and has set the groundwork to have more elements added and a fully scalable project.

</div>

Course Outcomes

- **Collaborative Environments:** Docstrings and Comments are supportive for reviews and future collaboration. This allows collaborators to understand and contribute to the modular OOP structure without prior context, improving collaboration over the original artifacts poorly documented script. 

- **Professional Communication:** The Tkniter GUI delivers coherent, user-adapted visuals such as: Labeled Buttons, Real-Time Inventory/Status Feedback, Grid-Based Map with 3 Second path highlights, and concise instructions. This transforms the original artifacts text-only input into a more intuitive interface that relays gameplay mechanics effectively.

- **Computing Solutions:** Refactoring the flat dictionary structure of the original artifact into extensible OOP classes in Room, Player, and Game, with redesigned functions such as the victory/defeat checks. 

- **Innovative Techniques:** Using Tkinter to overhaul the GUI, integrating Unit Testing (test_Lost_Lab), and regex validation for secure inputs, deliver value through maintainable, and industry-standard code. 

- **Security Mindset:** Regex Validation for input sanitization to prevent injection-like exploits in item entries, paired with try-except blocks for graceful error handling and unit tests to expose vulnerabilities (test_invalid_player_take_item). This ensures data integrity and privacy throughout the enhancement.


<div style="text-align:center; margin-bottom: 15px;">
  <img src="/images/passedunittests.png" alt="Final LostLab Enhanced Passed Unit Tests" style="max-width:100%; border-radius:10px;">
</div>

This shows the unit tests passing. If you would like to see the full unit test script please click the link. 

<div style="text-align:center; margin-top:20px;">
  <a href="https://github.com/zag2493/zag2493.github.io/blob/main/test_Lost_Lab_Enhanced.py" 
     target="_blank" 
     rel="noopener noreferrer"
     style="background-color:#4CAF50; color:white; padding:10px 25px; text-decoration:none; border-radius:5px; font-weight:bold;">
     View Original Artifact on GitHub
  </a>
</div>

<div style="text-align:center; margin-top:40px;">
  <a href="/" 
     style="background-color:#555; color:white; padding:10px 25px; text-decoration:none; border-radius:5px; font-weight:bold;">
     ⬅ Back to Home
  </a>
</div>
