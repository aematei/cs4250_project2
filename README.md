# CS 4250 – Assignment 2 Summary

**Course:** Web Search and Recommender Systems  
**Assignment Title:** Retrieval Models & PageRank  
**Due Date:** May 9, 2025  
**Type:** Group Project (same groups as before)  

---

## 🔧 Project Parts

### Part 1: Crawling and Indexing
- Perform a new crawl of **at least 500 pages**.
- Create a **simple inverted index** to map terms to documents.

### Part 2: Simple Retrieval
- Implement a **basic Boolean retrieval system**.
  - No need to support complex operators (e.g., `OR`, `NOT`).
  - Input queries via command line:
    ```
    > Please enter your query: tropical fish  
    > Relevant results are: doc12, doc24, doc45
    ```
  - No GUI required.

### Part 3: Improved Retrieval
- Implement an **advanced retrieval model**, such as:
  - Ranked Boolean
  - Vector Space Model
  - BM25

### Part 4: PageRank
- Compute **PageRank scores** for the pages you crawled.
- You may need to recrawl to ensure enough link data.

### Part 5: Combine
- Combine your retrieval model with PageRank.
  - Example: Multiply retrieval score × PageRank score.

---

## 📦 Deliverables

1. **Code**
   - All source code used to implement the project.

2. **Report (PDF, max 5 pages)** including:
   - Main components of the system.
   - Challenges faced during development.
   - Top 100 most important pages (by PageRank), with their scores.
   - Search results and performance comparison for **3 queries** using different models.
   - Discussion on how PageRank influenced the rankings.
   - Contributions from each team member.

---

## 📅 Deadline

**Submit by:** May 9, 2025
