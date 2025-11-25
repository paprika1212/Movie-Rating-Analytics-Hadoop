# Movie Rating Analysis - Big Data Analytics Project

**Course:** CSBB 422 - Big Data Analytics  
[cite_start]**Project ID:** 2 (Movie Rating Analysis) [cite: 2]  
[cite_start]**Submission Date:** November 25, 2025 

## 👥 Group Members
* **Aadrika Singh** - 221210001
* **Anandita Sharma** - 221210018
* **Gracy Gupta** - 221210042
* **Kashika** - 221210057

---

## 📖 Project Description
This project analyzes the MovieLens dataset to identify average ratings per movie and trends using a distributed big data architecture. [cite_start]The system is built on a **Hadoop Multi-Node Cluster** (1 Master, 2 Workers) and utilizes **Apache Spark** for processing and **Streamlit** for the frontend dashboard[cite: 2, 22].

## 🛠 Tech Stack
* **Hadoop (HDFS/YARN):** Distributed storage and resource management.
* **Apache Spark (PySpark):** In-memory data processing.
* **Python & Streamlit:** Data visualization and User Interface.
* **Environment:** Ubuntu 24.04.3 LTS (VirtualBox).

## [cite_start]⚙️ Cluster Setup [cite: 19, 21]
* **Master Node:** NameNode, ResourceManager
* **Worker Node 1:** DataNode, NodeManager
* **Worker Node 2:** DataNode, NodeManager

## 🚀 Execution Instructions
1.  **Start Cluster:** `start-all.sh`
2.  **Submit Job:** `spark-submit src/movie_analysis.py`
3.  **Launch UI:** `streamlit run src/app.py`

## 📂 Directory Structure
* `src/`: Source code for Spark jobs and UI.
* `config/`: Hadoop configuration files used in the cluster.
* `screenshots/`: Proof of execution and cluster status.