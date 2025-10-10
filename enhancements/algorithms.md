---
layout: default
title: "Algorithms and Data Structure"
permalink: /enhancements/algorithms/
---

# Algorithms and Data Structure Enhancement 

<div style="background-color: #c9c7c7; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 30px;">

<!-- Performance Screenshot -->
<div style="text-align:center; margin-bottom: 15px;">
  <img src="images/performance.png" alt="Lost Lab Performance Screenshot" style="max-width:100%; border-radius:10px;">
</div>

The original artifact Lost Lab, a Python text-based game initially developed as my final project for IT 140 also provided me an opportunity to use it for the Algorithms and Data Structure Enhancement. I choose to enhance it with advanced algorithms, building on the work completed for Software Engineering and Development (OOP, Tkinter). This phase, focused on optimizing navigation and inventory management using graph-based structures and choosing efficient data types. I choose Lost Lab for this category because it can clearly show my growth from a novice programmer to one that shows proficient algorithmic design and optimization. As Lost Lab was my first project, it originally was reliant on lists and basic loops, which was inefficient, making it an ideal candidate to showcase advanced techniques like graph modeling and set operation. The enhancement transforms it into a scalable, performance-driven application, aligning with an emphasis on algorithmic rigor and efficiency. 

<!-- Shortest Path Screenshot -->
<div style="text-align:center; margin-bottom: 15px;">
  <img src="images/shortestpath.png" alt="Shortest Path Code Screenshot" style="max-width:100%; border-radius:10px;">
</div>

</div>

Specific components highlighting my skills in algorithms and data structures:

- **NetworkX Graph Modeling:** Rooms are modeled as a weighted graph, with edges that can be dynamically weighted, such as Med Bay edge = 100 without having the MKIV Suit and MKV Helmet. Using Dijkstra's algorithm enabled efficient navigation and is highlighted in performance.py.

- **Set-Based Inventory:** Replaced the list-based inventory with a set for 0(1) average-case lookups, making it more efficient for real-time hazard checks.

- **Dijkstra's Algorithm:** Implemented shortest-path finding with dynamic weights to enforce hazard mechanics. This was chosen over Breadth First Search (as noted in code comments) for its flexibility with weighted edges.

- **Performance Testing:** Added performance.py to quantify set vs. list efficiency and to rate the pathfinding speed, ensuring optimization meets industry standards.

- **Unit Tests:** Extended test_Lost_Lab.py with tests like test_weighted_shortest_path_hazard, validating graph navigation and set operations.   
  
<div style="background-color: #c9c7c7; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 30px;">

The enhancements I chose to focus on improved the original artifact by replacing the linear searches (O(n) lookups) with O(1) set operations and enabling dynamic pathfinding, this reduces runtime overhead. The Tkinter GUI visualizes these algorithms, such as using the shortest path highlights, making an abstract concept more perceivable. The skills demonstrated include algorithmic analysis, data structure selection, and performance benchmarking, showcasing my ability to optimize for scalability. Enhancing Lost Lab for algorithms helped me better understand the power of data structure choices and algorithmic trade-offs in real world applications. Researching NetworkX opened my eyes to graph theory's practical utility, modeling rooms as nodes with weighted edges solves navigation challenges, but required studying to configure the weights dynamically for the hazards. Switching to sets for the inventory and using the performance script to see the increased efficiency reinforced the importance of operations responsiveness. While most trade-offs focused on efficiency, using Dijkstra’s algorithm over BFS was a personal choice of functionality, the flexibility to add weighted hazards seemed to be a better fit for scalability and gameplay. As with each enhancement, there was challenges to work and learn through. Trying to add the hazards with weight created issues with the shortest path, this required reworking the shortest path function and distributing the weight directly. The GUI's role in visualizing the algorithms such as the 3 second path highlights, bridged data structures to user experience. Security considerations involved ensuring set operations avoided data leaks and validating path weights to prevent exploits. 

</div>

Course Outcomes

- **Collaborative Environments:** Clear docstrings and comments support team collaboration and peer review. The documentation is laid out in a way that explains design choices and creates an application that can be handed off for continued development.

- **Professional Communications:** GUI path visualization and performance metrics convey the algorithmic efficiency to stakeholders and users.

- **Computing Solutions:** Designed graph-based navigation with NetworkX and set inventory, evaluating trade-offs such as Dijkstra vs BFS and Sets vs List, aiming for optimal and beneficial performance.

- **Innovative Techniques:** Using NetworkX and sets for scalable navigation, with benchmarks ensuring industry-standard efficiency.

- **Security Mindset:** Ensured set operations and weighted paths prevent exploits which were validated by tests.

<!-- Highlighted Path Example -->
<div style="text-align:center; margin-bottom: 15px;">
  <img src="images/hpexample.png" alt="Highlighted Path Example Lost Lab" style="max-width:100%; border-radius:10px;">
</div>

Showcasing the highlighted path from Rec Room to Terrarium.

<!-- Weighted Path Example -->
<div style="text-align:center; margin-bottom: 15px;">
  <img src="images/weightedexample.png" alt="Weighted Path Example Lost Lab" style="max-width:100%; border-radius:10px;">
</div>

Weighted path example, showing that without the proper items, the shortest path from Cargo Hold to Lab requires you to go around rather than straight through Med Bay. 
