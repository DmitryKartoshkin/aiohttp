from aiohttp import web
from Mosels import Advert, Session
from ValidModels import validation_date, ValidAdvertisement
import json


async def get_advertisement(id_: int, session: Session):
    """Функция проверяет существует ли объявление в БД по указанному ID"""
    advertisement = await session.get(Advert, id_)
    if advertisement is None:
        raise web.HTTPNotFound(text=json.dumps({
            "error": 404,
            "massenge": "Advertisement not found"}),
            content_type="application/json"
        )
    return advertisement


class Advertisement(web.View):
    async def get(self):
        advertisement = await get_advertisement(
            int(self.request.match_info['advertisement_id']),
            self.request["session"]
        )
        return web.json_response({
            "id": advertisement.id, 'heading': advertisement.heading,
            'description': advertisement.description,
            'owner': advertisement.owner,
            'date_create': advertisement.date_creat.isoformat()
        })

    async def post(self):
        json_data = await self.request.json()
        json_data = validation_date(json_data, ValidAdvertisement)
        advertisement = Advert(**json_data)
        self. request["session"].add(advertisement)
        await self. request["session"].commit()
        return web.json_response({"id": advertisement.id})

    async def delete(self):
        advertisement = await get_advertisement(
            int(self.request.match_info['advertisement_id']),
            self.request["session"]
        )
        await self.request["session"].delete(advertisement)
        await self.request["session"].commit()
        return web.json_response({self.request.match_info['advertisement_id']: "Удален из базы"})