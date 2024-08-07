import uvicorn
from app import app
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True,timeout_keep_alive=60)
# command to start app
# uvicorn main:app  --reload
# postman collection
# https://documenter.getpostman.com/view/16226090/2sA3rzKYJ1