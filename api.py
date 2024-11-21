#streamlit
from fastapi import FastAPI, HTTPException
from typing import Optional
import pymongo
import uvicorn

app = FastAPI()
client = pymongo.MongoClient("mongodb://127.0.0.1:27017")
db = client["PokemonDB"]
collections = ["Sets", "Decks", "Cards"]

@app.get("/")
async def root():
	return {(
    	"Welcome to the Pokemon TCG API!"
    	"This API allows you to get Cards, Decks and Sets information from PokemonTCG."
    	"Use the '/Cards/' endpoint with a GET request to get cards information."
		"Use the '/Decks/' endpoint with a GET request to get decks information."
		"Use the '/Sets/' endpoint with a GET request to get sets information."
	)}


@app.get("/cards")
async def results(name: Optional[str] = None, types: Optional[str] = None, skip: int = 0, limit: int = 10):
    """
    Get cards filtered by optional query parameters.
    **QUERY**
    - **name**: Optional query parameter to filter cards by name.
    - **types**: Optional query parameter to filter cards by a specific type.
    - **skip**: Defines how much documents you want to skip the visualization. (default = 0)
    - **limit**: Defines the limit of records that will be returned, with max value of 10. (default = 10). 
    **PATH**
    - **id**: ID of the card you want to retrieve.
    """
    
    if limit > 10:
        raise HTTPException(status_code=400, detail="Limit not allowed, please provide a limit equal or under 10")


    query = {}

    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    if types:
        query["types"] = {"$regex": types, "$options": "i"}
        

    result = list(db.CardsCollection.find(query).skip(skip).limit(limit)) 

    if not result:
        raise HTTPException(status_code=404, detail="No decks found for the matching search")

    # Change _id type for each document
    for item in result:
        item["_id"] = str(item["_id"])  
        

    return result


@app.get("/cards/{id}")
def results(id: str):
    """
    Get cards filtered by ID Path parameter.
    - **id**: ID of the card you want to retrieve.
    """

    result = list(db.CardsCollection.find({"id": id})) 

    if not result:
        raise HTTPException(status_code=404, detail="No cards found for the matching ID")
    
    # Change _id type for each document
    for item in result:
        item["_id"] = str(item["_id"])  
    
    return result


@app.get("/decks")
def results(name: Optional[str] = None, card_name: Optional[str] = None, types: Optional[str] = None):
    """
    Get decks filtered by optional query parameters.
    - **name**: Optional query parameter to filter decks by name.
    - **card_name**: Optional query parameter to filter decks that contains a specific card by its name.
    - **types**: Optional query parameter to filter decks by a specific type or types.
    """

    query = {}

    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    if card_name:
        query["cards.name"] = {"$regex": card_name, "$options": "i"}
    if types:
        query["types"] = {"$in": types.split(",")}
        

    result = list(db.DecksCollection.find(query)) 

    if not result:
        raise HTTPException(status_code=404, detail="No decks found for the matching search")

    # Change _id type for each document
    for item in result:
        item["_id"] = str(item["_id"])  
        

    return result

@app.get("/decks/{id}")
def results(id: str):
    """
    Get decks filtered by ID Path parameter.
    - **id**: ID of the deck you want to retrieve.
    """

    result = list(db.DecksCollection.find({"id": id})) 

    if not result:
        raise HTTPException(status_code=404, detail="No cards found for the matching ID")
    
    # Change _id type for each document
    for item in result:
        item["_id"] = str(item["_id"])  
    
    return result

@app.get("/sets")
def results(name: Optional[str] = None,	series: Optional[str] = None):
    """
    Get sets filtered by optional query parameters (name and/or series).
    - **name**: Optional query parameter to filter sets by name.
    - **series**: Optional query parameter to filter sets by series.
    """

    query = {}

    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    if series:
        query["series"] = {"$regex": series, "$options": "i"}
        

    result = list(db.SetsCollection.find(query)) 

    if not result:
        raise HTTPException(status_code=404, detail="No sets found for the matching search")

    # Change _id type for each document
    for item in result:
        item["_id"] = str(item["_id"])  
        

    return result

@app.get("/sets/{id}")
def results(id: str):
    """
    Get sets filtered by ID Path parameter.
    - **id**: ID of the deck you want to retrieve.
    """

    result = list(db.SetsCollection.find({"id": id})) 

    if not result:
        raise HTTPException(status_code=404, detail="No cards found for the matching ID")
    
    # Change _id type for each document
    for item in result:
        item["_id"] = str(item["_id"])  
    
    return result


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

