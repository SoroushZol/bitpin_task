# **Django Blog API Documentation**

## **Project Components**

### **1. Main Project: `bitpin_task`**
- Contains project-level configurations.
- Key files:
  - `settings.py`: Configurations for database, middleware, installed apps, etc.
  - `urls.py`: Includes app-level URLs for routing.
  - `celery.py`: Configures Celery for asynchronous task handling.
  - `asgi.py` and `wsgi.py`: Entrypoints for deployment.

### **2. Django App: `blog`**
- Contains the main functionality for blog posts and scoring.
- Key files:
  - `models.py`: Defines the database models for blog posts and scores.
  - `views.py`: Handles API requests and responses via ViewSets.
  - `serializers.py`: Handles data serialization for blog posts and scores.
  - `urls.py`: Maps URL patterns to the respective views.
  - `tasks.py`: Handles background tasks (e.g., asynchronous operations).
  - `filters.py`: Adds filtering logic for APIs.
  - `pagination.py`: Manages pagination for list APIs.
-  Testing:
   - `tests/`: Unit tests for validating functionality.
- Migrations:
  - `migrations/`: Tracks database schema changes.
- Redis Integration:
  - `redis_client.py`: Provides Redis support for caching or task brokering.

---

## **APIs**

### **Base Path**: `/blog/`

### **1. Blog Post Management**
- **GET `/blog/post/`**: Retrieve a list of all blog posts.
- **GET `/blog/post/<id>/`**: Retrieve details of a specific blog post by its ID.

### **2. Scoring System**
- **POST `/blog/score/`**: Add a new score to a blog post.
- **GET `/blog/score/<id>/`**: Retrieve details of a specific score by its ID.
- **PUT `/blog/score/<id>/`**: Update a specific score by its ID.

---

## **Technology Stack**
- **Framework**: Django
- **Database**: MySQL (By Default)
- **Caching**: No caching implemented due to data volatility.
- **Task Queue**: Celery for background task management with Redis as the broker.
- **API Design**: Follows RESTful principles using Django REST Framework.
- **Authentication**: JWT (JSON Web Tokens) for user authentication.
---

## **How to Run the Project**
1. Clone the repository and navigate to the project directory.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Apply migrations:
   ```bash
   python manage.py migrate
   ```
4. Run the development server:
   ```bash
   python manage.py runserver
   ```
5. Access the API at: `http://localhost:8000/blog/`

---

## **Enhancement Strategy**

### **Challenge 1: Handling High Traffic**
The server needed to handle approximately \(1000\) requests per second from users adding scores to blog posts. Each new score update required recalculating the average score and score count for the respective post. Querying and recalculating these values directly from the database for each request would have caused significant latency and load.

**Solution:** To optimize performance, two additional columns, `average_score` and `score_count`, were added to the `BlogPost` table. These columns store the aggregated values and eliminate the need to retrieve all related scores and recalculate the average and count during each request. This optimization significantly reduced database queries and improved response times.

### **Challenge 2: Mitigating Sudden Changes in Average Scores**
Short-term emotional bursts of user activity could lead to drastic changes in a blog post's average score. To ensure that these fluctuations did not disproportionately affect the main average score, a **rolling average (moving average)** method was implemented.

**Solution:**
1. Incoming scores are grouped into time-based windows, each representing \(2\)-minute intervals.
2. For each window, the average score is calculated independently.
3. The rolling average is then computed over these windows, providing a smoothed value that reflects long-term trends without being overly influenced by short-term anomalies.

**Example Calculation:**
- Consider \(4\) chunks of scores, each representing \(2\)-minute intervals:
  \[
  (4, 3, 2, 5), \quad (4, 3, 1), \quad (0, 1, 0, 0, 0, 1, 1, 1, 0, 1), \quad (2, 3)
  \]
- The average scores for each chunk are:
  \[
  3.5, \quad 2.66, \quad 0.5, \quad 2.5
  \]
- The overall rolling average becomes:
  \[
  \frac{3.5 + 2.66 + 0.5 + 2.5}{4} = 2.29
  \]
- In contrast, a simple average of all scores directly would yield \(1.68\), which does not account for the anomaly in the third chunk.

#### **Implementation Strategy:**
1. All new scores are saved in the `Score` table in the MySQL database and pushed to Redis for temporary storage.
2. Every \(2\) minutes, a Celery task retrieves the recent scores from Redis, calculates their average, and updates the `average_score` and `score_count` columns in the database.
3. The rolling average algorithm is applied during this process to ensure the averages remain stable and reflective of long-term trends.

---

# **Possible Questions**

## **1. Why 2 minutes?**
The \(2\)-minute interval is a hyperparameter that was chosen as a balance between real-time responsiveness and system performance. It can be fine-tuned based on real-world usage and server capacity. Shorter intervals may provide more frequent updates but increase server load, while longer intervals may reduce load at the cost of slightly delayed updates.

---

## **2. Does this method cause a \(2\)-minute (or \(n\)-minute) delay for users to see updated average scores and counts?**
No, the system ensures users see up-to-date average scores and counts. This is achieved by combining the following during serialization in the `Django` `BlogPost` serializer:
- The `average_score` and `score_count` fields stored in the database.
- The latest scores from Redis, which hold recent updates not yet written to the database.

This approach ensures users receive the most accurate and current data without waiting for the \(2\)-minute Celery task to complete.

---

## **3. Could there be discrepancies in the long term between the real average score and the calculated one, especially when users update their scores?**
Yes, slight discrepancies can arise over time, particularly if users frequently update their scores. To minimize these discrepancies, only the difference between the new score and the old score is added to Redis during score update scenarios. This reduces the impact of outdated scores as much as possible.

To further address this, an additional Celery task runs once daily during off-peak hours (e.g., at night). This task recalculates the `average_score` and `score_count` fields using the complete set of scores stored in the database.

The task applies the same rolling average (moving average) method to maintain consistency and correct any discrepancies, ensuring the accuracy of the calculated values over the long term.
