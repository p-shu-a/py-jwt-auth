### Python Version of the JWT auth API.
It will do the same thing.
Main libs: python, fastapi, postgres
The purpose of this project is to be able to compare and contrast the same code in python vs Go-lang
The DB schema lives in the go-lang project repo

#### TODO:
- remove sql alchemy and replace with fastAPI's SqlModel
    - or not!!! figured i'd remove the pydantic model and let the sqlmodel remplace the declartive base and do all the work...
    - well turns out, it no longer validates unauthorized keys coming in the request body, which is no help
    - thus, i had to include a pydantic model after all. i think all the work i did to remove sqlalchemy and replace it with sqlmodel didn't really pan out. 
    - sqlalchemy can't really be replaced. the async capabilities, postgres dialects all belong to that package. not sqlmodel. now...

#### WHAT DID WE LEARN??
- Python allows for you to play is fast and loose.
    - which means you easily get away with avoiding abiding by best practices
    - compared to the go-lang version, the core logic could be written in half the time.
    - but what I gained in speed initially, i gave back eventually. implimenting the DB, fixing tests, etc.
- Where I began:
    - three handler functions: register, login, secret
    - register: registering meant saving a user to a dictionary
    - login: check if user is in dict, validate password, return jwt
    - if user has JWT, and JWT is valid, allow access to /secret endpoint
- All That was easy enough, fairly uncomplicated python code.
- Quite liked writing a custom decorator. great way to extend a function's ability and force behaviour
- the bcrypt and JWT apis werent to different from the go version.
    - wondering which jwt/bcrypt library to install via pip was another matter. lots of options, too many. i used PyJWT
    - specific to jwt lib, there was no differentiating of registerd claims, everything could be all custom.
- I prefered Go's `http` lib's `http.Error` syntax. being able to define the structured responses was quite easy with go
    - If i had to define custom responses (hell, even changing the key from "details" to "message"), i'd need to define a custom exception
    - though, i could define an ResponseItem (pydantic model) and return that...
- Defining a `BaseModel` with pydantic is really awesome. great way to enforce types and way to outsource error checking
- using `uvicorn` and having the app reload with ever cmd+s  is very convenient
- using fastapis `@router.post("/foo",status_code=201)` decorator is a great way to limit methods on a handler and set default status_codes.
- If you want to stick with the defaults, returning responses was quite easy
- testing with Pytest is brain-dead easy
- Untangeling/modularizing the code was a bit of a mess
    - The main thing i don't like is the import statement bloat that gets added

#### Things that are awful:
- pyton dependencies and imports
    - really difficult to keep track of what needs to be installed
    - i did pip installs on the whole machine, no venv used :facepalm:
    - in a ~real~ app, this would be unacceptable, i can see myself in dependancy hell
- DB related ORM bullshit really adds to the mess of models.
    - db integrations was deffs way easier with GO
- in fact, modularizing, and going from in-mem db to postgrest was all very easy in GO. So was swapping over the tests.
- It was a nightmare here. Really Not straight forward.
- once again, the imports and dependencies with same names, but inablity to interoperate. wtf...
- In general, as this project evolved, i found it more frustrating to work on.
    - knowledge of python didn't matter, felt that i was busy figuring out the libs
    - documentation accessible via intellisense was fukin brutal. online wasn't too much better
    - chatGPT was shitting the bed also. suffered serious performance degradation. (read below)
    - debugging the test-harness was a PITA.
    - because python isn't async by default like go is, you have to dilligently add async/await.
        - If you miss putting async/await in front of a function or return, things will not work as expected.
- Naming hell: if you're working on an API, its probably true that the libs will also have functions, vars, etc named API. don't add to the mess, use better names
- scopes are really be a mess:
    - async loop_scope vs fixture scopes can get all tangled up. 
    - scope= is for pytest fixtures 
        - controls how often the fixture is created
        - options are: module, session, function, and class
    - loop_scope= is for pytest-asyncio
        - controls event-loop persistance across tests
        - options are: session and function
    - this can really be a mother fucker...


#### Notes on chatGPT
- I used ChatGPT(4o) to help me with the app, and I gotta say, it shit the bed.
- By the time I quit using chatgpt for help, it was giving me shit. (Literally: "your variable is name override, change it to _override")
- I think there might be two reasons for this:
    1. Used just one chat window to do all the work. probably was hitting the context limit of a chat and the performance degraded severely. though, i gotta say i opened a new window and its help (with debugging, db realted test setup) was useless there to. which leads me to believe...
    2. i think with python, it might be a classic case of GIGO. garbage in, garbage out. its probably trained on TOOO much. Python can be a wild west, with thousand ways to skin the cat. I wonder if this could be true for interpreted langs in general. i used chatGPT for the same project in GO last week, and it was super helpful. complimentary to the docs. My hypothesis is that: compiled and statically-typed langs will be better generated through chatGPT precisely because it is a compiled and statically typed.

#### Questions:
- what are tags in fastAPI
- in an annotation like this, what does Header() mean? "x-token exists in header?":
    `x_token: Annotated[str, Header()]`
- cut over from sql alchemy to sql model


#### More learnings:
- if you're testing async infra, your tests should also be async
    - just like function which call async func should be async (and vice versa)
- We're making heavy use of dependancy injection here.
    - FastAPI's "Depends()" in the handler sig
    - tests "silently" injecting dependencies via fixtures
- I gotta say, i don't really like the AutoMagic of the frameworks
    - the clever "we'll do it for you" can be tricky to troubleshoot once you start adding on complexity
- SQL model was useless for me, just use sqlalchemy, its not much more complex.
- Under standing of eventloop scopes is esential!
    - implement them correctly, or fixing will be a pain
    - in my case, with testing, because the scoopes were poorly defined:
        - dependiencies were not overwritten, and thus incorretcly injected.
            - prod db session were to be overwritten by test db sessions
        - this resulted in tests happening in prod db
    - fixture loops != async loops
- as usual, test setups never fail to impress. Amazing that you can test an app without having it running.
- For some of these libraries, You can always tell what a function returns.
    - Sometimes you can tell when the documentation, which is available through IntelliSense, mentioned it
    - otherwise good luck. enforcement of return types, another point for statically typed langs
- Generators are very interesting
    - checkout the comments in conftest.py for more notes. trust me they're worth it!