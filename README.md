# Research-Data-Explorer
ReDaX is a web application that serves as a reference database for exploring and documenting research datasets. Users can add metadata, browse and search datasets, and leave comments to suggest use cases or evaluate the quality and usefulness of the data.

* The user can create an account and log into the application.
* The user can add metadata for datasets to the application. Additionally, the user can edit and delete the metadata they have added.
* The user can view the metadata for the datasets added to the application. The user can see both the information they have added and the information added by other users.
* The user can search for datasets using keywords or other criteria. The user can search for both the datasets they have added and those added by other users. **Partyally implemented**
* The application has user pages that display statistics for each user and the datasets added by the user. **Not yet implemented**
* The user can select one or more classifications for the metadata (e.g., data access, data type, scientific field). Possible classifications are stored in the database. **Not yet implemented**
* The user can add comments to the metadata of their own datasets as well as those added by other users. Comments can describe, for example, the use cases of the data or assessments of the data quality. **Not yet implemented**

## How to Run the Application
1. clone the repository
2. create and activate a virtual environment: python3 -m venv venv
source venv/bin/activate
3. install flask library: pip install flask
4. create the database: sqlite3 database.db < schema.sql
5. run the application: flask run

