from aiohttp import web
from Mosels import Base, engine, Session
from service import Advertisement

app = web.Application()


async def app_context(app):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


@web.middleware
async def session_middleware(request: web.Request, handler):
    async with Session() as session:
        request["session"] = session
        response = await handler(request)
        return response

app.middlewares.append(session_middleware)
app.cleanup_ctx.append(app_context)


app.cleanup_ctx.append(app_context)
app.add_routes([
    web.get("/advertisement/{advertisement_id:\d+}/", Advertisement),
    web.post("/advertisement/", Advertisement),
    web.delete("/advertisement/{advertisement_id:\d+}/", Advertisement)
])


if __name__ == '__main__':
    web.run_app(app, host='127.0.0.1', port=8080)
    app.run()

