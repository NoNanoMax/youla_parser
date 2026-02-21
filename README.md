# Youla parser

---- 

API for parsing parsing ads from websites (optionally ads of used cars)
How it works:
1) Iterate through main page and find all links with ads
For each ad:
2) Parse description and meta 
3) Iterate through photos in ad and save 

![alt text](docs/vis.gif)

----

#### How to run

```sudo docker compose up --build -d```

----

#### How to use

You can find all information in api-docs