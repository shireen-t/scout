import uvicorn
from fastapi import FastAPI,  HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
import re
from scout import scout

app = FastAPI()

#cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)


#Home route
@app.get("/")
def home():
	content = "<html><head><title>Welcome to Scout API </title></head><body><p>Welcome to the Scout Crawler API. Please check the <a href='https://github.com/IDayanandJagtap/scout'>documentation</a> for more details.<p></body></html>"

	return HTMLResponse(content)


# Scout route
@app.get("/scout/{cas_or_name}")
async def run_scout(cas_or_name: str):
	if cas_or_name is None:
		raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
		                    detail="No input provided.")

	# identify cas or name
	cas_pattern = r'^\d{2,7}-\d{2}-\d$'
	match = re.match(cas_pattern, cas_or_name)

	try:
		if match:
			response = await scout(cas=cas_or_name, name=None)
		else:
			response = await scout(cas=None, name=cas_or_name)

		return JSONResponse(status_code=HTTP_200_OK, content=response)
	except Exception as e:
		return JSONResponse(status_code=HTTP_500_INTERNAL_SERVER_ERROR,
		                    content={"error": str(e)})

# static file serving
# Mount the static files directory
app.mount("/verified", StaticFiles(directory="verified"), name="verified")
app.mount("/unverified",
          StaticFiles(directory="unverified"),
          name="unverified")

# Start when script is called
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)