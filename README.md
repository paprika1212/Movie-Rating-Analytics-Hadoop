# 🎬 Movie Rating Analytics - Big Data Project

**Course:** CSBB 422 - Big Data Analytics  
**Project:** #2 Movie Rating Analysis  
**Tech Stack:** Hadoop, Apache Spark, Python (Streamlit)

---

## 📖 Project Overview
This project implements a distributed Big Data pipeline to analyze the **MovieLens 100k dataset**. The system calculates the average rating for every movie, filters for popularity, and visualizes the results on an interactive dashboard.

The solution is deployed on a **3-Node Hadoop Cluster** (1 Master, 2 Workers) using **YARN** for resource management and **Spark** for in-memory processing.

## 👥 Group Members
* **Aadrika Singh** - 221210001
* **Anandita Sharma** - 221210018
* **Gracy Gupta** - 221210042
* **Kashika** - 221210057

---

## 🏗️ System Architecture
We constructed a fully distributed cluster using Oracle VirtualBox running Ubuntu 20.04 LTS.

| Node Name | Role | IP Address | Configuration |
| :--- | :--- | :--- | :--- |
| **Master** | NameNode, ResourceManager | `192.168.0.205` | 4GB RAM, 2 Cores |
| **Worker1** | DataNode, NodeManager | `192.168.0.208` | 2GB RAM, 1 Core |
| **Worker2** | DataNode, NodeManager | `192.168.0.84` | 2GB RAM, 1 Core |

### 🛠 Technologies Used
* **Storage:** Hadoop HDFS (Replication Factor: 2)
* **Processing:** Apache Spark 3.5.0 (PySpark)
* **Visualization:** Streamlit & Altair
* **Coordination:** SSH Passwordless Login

---

## ⚙️ Execution Steps (How we built it)

### Phase 1: Infrastructure Setup
1.  **Virtualization:** Created a Master Node in VirtualBox using **Bridged Adapter** networking to allow real IP assignment.
2.  **Cloning:** Cloned the Master to create two Worker nodes, ensuring unique MAC addresses were generated to prevent network conflicts.
3.  **Network Configuration:**
    * Assigned static hostnames (`master`, `worker1`, `worker2`).
    * Mapped IP addresses in the `/etc/hosts` file on all three nodes to enable communication.
4.  **SSH Access:** Generated RSA keys on the Master and distributed them to all workers (`ssh-copy-id`) to allow **passwordless** control of the cluster.

### Phase 2: Hadoop & Spark Configuration
1.  **Installation:** Installed Java 8 (OpenJDK), Hadoop 3.3.6, and Spark 3.5.0.
2.  **Configuration:**
    * Configured `core-site.xml` (HDFS entry point).
    * Configured `hdfs-site.xml` (Replication = 2).
    * Configured `yarn-site.xml` and `mapred-site.xml` for resource management.
    * Updated `workers` file to register Worker1 and Worker2.
3.  **Synchronization:** Used `scp` to send the configured Hadoop setup from Master to both Workers, ensuring identical environments.

### Phase 3: Deployment & Analysis
1.  **Formatting:** Formatted the HDFS NameNode to initialize the storage system.
2.  **Startup:** Launched the cluster using `start-dfs.sh` and `start-yarn.sh`.
3.  **Data Ingestion:** Downloaded the MovieLens dataset and uploaded `u.data` and `u.item` to HDFS `/input` directory.
4.  **Analysis:** Wrote a PySpark script (`movie_analysis.py`) to aggregate ratings and export results to CSV.
5.  **Visualization:** Built a `app.py` dashboard using Streamlit to visualize the Top 20 movies and rating distributions.

---

## Screenshots 
<img width="1836" height="907" alt="Screenshot from 2025-12-02 00-19-48" src="https://github.com/user-attachments/assets/b19dd2b5-5c43-4639-af27-9be5330f0d03" />
<img width="1836" height="907" alt="Screenshot from 2025-12-02 00-19-55" src="https://github.com/user-attachments/assets/4e26f984-9842-4c81-9481-524457ec66cb" />
<img width="1836" height="907" alt="Screenshot from 2025-12-02 00-20-08" src="https://github.com/user-attachments/assets/62a14239-44e0-4040-89cc-6a7061101f33" />
<img width="709" height="746" alt="Screenshot from 2025-12-02 00-23-28" src="https://github.com/user-attachments/assets/d8c89786-3768-4ac8-9b8b-7520b099b839" />
<img width="1081" height="741" alt="Screenshot from 2025-12-02 00-23-58" src="https://github.com/user-attachments/assets/e500ed6d-56a4-4547-8a23-ffe33c1ede08" />
<img width="1061" height="576" alt="Screenshot from 2025-12-02 00-24-16" src="https://github.com/user-attachments/assets/a198643c-b449-4fc8-bb4a-b7af64491ba0" />


---

## 🚀 How to Run This Project

### 1. Start the Cluster (On Master)
```bash
start-dfs.sh
start-yarn.sh
